import argparse
import re
import os
import logging
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
from typing import Any, Dict
from enum import Enum

import requests


@dataclass
class ChannelParams:
    name: str
    timezone: str
    ip: str
    user: str
    password: str
    rtsp: int
    http: int


def parse_line(line: str) -> ChannelParams:
    """
    Parse line from CSV file and create Channel object
    line format: name,location,group,user,password,serial,mac
        param[0] - Camera name
        param[1] - Timezone
        param[2] - Local IP
        param[3] - Username
        param[4] - Password
        param[5] - HTTP Port
        param[6] - RTSP Port
    """
    line = line.replace('\n', '')
    param = line.split(",")

    return ChannelParams(
        name=param[0],
        timezone=param[1],
        ip=param[2],
        user=param[3],
        password=param[4],
        http=int(param[5]),
        rtsp=int(param[6])
    )


def get_headers(token: str) -> Dict[str, str]:
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def get_cloud_two_info(email: str, password: str, endpoint: str):
    api_endpoint = f"https://{endpoint}/v1/auth"
    data = {
        "email": email,
        "password": password
    }
    auth_request = requests.post(
        url=api_endpoint,
        json=data,
        timeout=10
    )
    if auth_request.status_code != 200:
        logging.error("Failed to fetch auth token for %s/%s", email, password)
        return {}
    resp = auth_request.json()
    logging.info("Received access token: %s", resp["accessToken"])
    logging.info("Received VMS Endpoint: %s", resp["session"]["company"]["endpoint"])
    # logging.info("Received VMS LKey: %s", resp["session"]["company"]["lKey"])
    return {
        "access_token": resp["accessToken"],
        "vms_endpoint": resp["session"]["company"]["endpoint"],
        # "lkey": resp["session"]["company"]["lKey"]
    }


def get_gateway_info(endpoint: str, auth_token: str, guid: str, mac=None):
    # /v1/gateway
    api_endpoint = f"https://{endpoint}/v1/gateway?params=%7B%22include_meta%22%3A%20true%7D"

    gw_request = requests.get(
        url=api_endpoint,
        headers=get_headers(token=auth_token),
        timeout=10
    )

    if gw_request.status_code != 200:
        logging.error("Failed to request gateways.")
        return {}

    # gateway = {}
    for curr_gateway in gw_request.json()["objects"]:
        if guid and not mac and guid == curr_gateway["meta"]["gateway_id"]:
            # gateway = curr_gateway
            return curr_gateway
        elif guid and mac and "gateway_mac" in curr_gateway["meta"]:
            if (
                guid == curr_gateway["meta"]["gateway_id"] and
                mac == curr_gateway["meta"]["gateway_mac"]
            ):
                return curr_gateway
    return {}


def add_camera_to_gw(endpoint, auth_token, channel_params: ChannelParams, gateway: Dict):
    api_endpoint = f"https://{endpoint}/v1/gateway/{gateway['id']}/camera"

    body = {
        "name": channel_params.name,
        "timezone": channel_params.timezone,
        "meta": {
            "siteId": gateway["meta"]["siteId"],
            gateway["meta"]["siteId"]: "siteId"
        },
        "url": channel_params.ip,
        "http": channel_params.http,
        "rtsp": channel_params.rtsp,
        "username": channel_params.user,
        "password": channel_params.password
    }

    if "openwrt" in gateway["meta"]:
        body["guuid"] = ""
        body["serialNumber"] = gateway["meta"]["gateway_id"]
    else:
        body["guuid"] = gateway["meta"]["gateway_id"]

    gw_request = requests.post(
        url=api_endpoint,
        headers=get_headers(token=auth_token),
        json=body,
        timeout=10
    )

    if gw_request.status_code != 201:
        logging.error(
            f"Failed to add camera. Name: {channel_params.name}, IP: {channel_params.ip}"
        )
    else:
        logging.info(
            f"Successfully added camera with ID {gw_request.json()['id']}"
        )


def main():
    logging.basicConfig(
        format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
        level=os.environ.get("LOGGING", "INFO"),
    )

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--email", help="Email for cloudtwo account", required=True)
    parser.add_argument("--password", help="Password for cloudtwo account", required=True)
    parser.add_argument("--csv", help="Path to CSV file", required=True)
    parser.add_argument("--endpoint", help="Cloudtwo API endpoint", required=True)
    parser.add_argument("--guid", help="Unique ID of docker gateway", default=None)
    parser.add_argument("--serial", help="Serial number of Openwrt gateway", default=None)
    parser.add_argument("--mac", help="MAC Address of Openwrt gateway", default=None)
    args = parser.parse_args()

    # Get Cloud Two info
    c2_dict = get_cloud_two_info(
        email=args.email,
        password=args.password,
        endpoint=args.endpoint
    )

    if not c2_dict:
        raise Exception("No auth_token.")
    else:
        auth_token = c2_dict["access_token"]

    if not args.mac and not args.serial and args.guid:
        gateway = get_gateway_info(
            endpoint=args.endpoint,
            auth_token=auth_token,
            guid=args.guid
        )
    elif not args.guid and args.mac and args.serial:
        gateway = get_gateway_info(
            endpoint=args.endpoint,
            auth_token=auth_token,
            guid=args.serial,
            mac=args.mac
        )
    else:
        raise Exception("Invalid combination of gateway values.")

    if not gateway:
        raise Exception("Gateway not found.")

    with (
        open(args.csv, "r", encoding="utf-8") as file,
    ):
        lines = file.readlines()
        for line in lines:
            channel_params = parse_line(line)
            logging.info(f"Channel_params: {channel_params}")

            add_camera_to_gw(
                endpoint=args.endpoint,
                auth_token=auth_token,
                channel_params=channel_params,
                gateway=gateway
            )


if __name__ == "__main__":
    main()
