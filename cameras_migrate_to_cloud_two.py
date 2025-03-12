import argparse
import re
import os
import logging
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
from typing import Any, Dict
from enum import Enum

import requests

# python3 ./create_gateway_channels_from_csv.py --gateway_ip 3.80.125.65 --vms_url https://web.vxg-dev.vxg-dev.cloud-vms.com --uplink_url http://dev-api.proxy.cloud-vms.com/uplink_camera/ --license_key DINDON --csv_path ./example_csv/gateway_bulk_add.csv --gateway_id EC20A411-536F-C726-D3D2-D6AA818F14B8
# def print_error(name: str, args: list, kwargs: dict, ex: Exception):
#         logging.error("%s, args: %s, kwargs: %s. Error: %s", name, args, kwargs, ex)


# def print_exc_error(func):
#     def wrap_exception(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as ex:  # pylint: disable=broad-except
#             print_error(name=func.__qualname__, args=args, kwargs=kwargs, ex=ex)
#             return None, None

#     return wrap_exception


def get_co_headers(lkey: str) -> Dict[str, str]:
    return {
        "accept": "application/json",
        "Authorization": f"LKey {lkey}",
        "Content-Type": "application/json",
    }


def get_ct_headers(token) -> Dict[str, str]:
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def get_cloud_two_auth(email: str, password: str, endpoint: str) -> dict:
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
    logging.info("Received company ID: %s", resp["session"]["company"]["id"])
    return {
        "access_token": resp["accessToken"],
        "company_id": resp["session"]["company"]["id"]
    }


def add_lkey_to_cloud_two(
        auth_token: str,
        company_id: str,
        endpoint: str,
        co_endpoint: str,
        lkey: str
):
    headers = get_ct_headers(token=auth_token)
    api_endpoint = f"https://{endpoint}/v1/company/{company_id}/auth"
    data = {
        "lKey": lkey,
        "endpoint": f"https://{co_endpoint}/"
    }
    company_request = requests.patch(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )

    if company_request.status_code != 200:
        logging.error("Failed to add LKey to company.")


def create_cloud_two_site(auth_token: str, endpoint: str) -> int:
    '''
    :param auth_token: str of cloudtwo auth token
    :return id: int of site id created
    '''
    headers = get_ct_headers(token=auth_token)
    data = {
        "site": [
            {"name": "cloudone"}
        ],
        "location": {
            "city": "Toronto",
            "state": "Ontario",
            "country": "Canada",
            "address": "3080 Yonge St, Toronto, ON M4N 2K4, Canada",
            "latitude": 43.72528319999999,
            "longitude": -79.4025985
        }
    }
    api_endpoint = f"https://{endpoint}/v1/site"
    site_request = requests.post(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )
    if site_request.status_code != 200:
        logging.error("Failed to create site.")
        return 0
    resp = site_request.json()
    logging.info("Created site %d", resp["location"]["id"])
    return resp["location"]["id"]


def get_channel_group_id_for_site(site_id: int, endpoint: str, lkey: str) -> int:
    '''
    Get channel_group id with name = Site<ID>
    '''
    site = f"Site{site_id}"
    headers = get_co_headers(lkey=lkey)
    api_endpoint = f"https://{endpoint}/api/v3/channel_groups/?limit=1000"
    # Fetch group channels
    cg_request = requests.get(
        url=api_endpoint,
        headers=headers,
        timeout=10
    )
    if cg_request.status_code != 200:
        logging.error("Failed to get channel groups.")
        return 0
    for channel_group in cg_request.json()["objects"]:
        if channel_group["name"] == site:
            logging.info(
                "Successfully got channel group ID: %d.",
                channel_group["id"]
            )
            return channel_group["id"]
    logging.error("Site not found in Channel Groups.")
    return 0


def get_cloud_one_channels(lkey: str, endpoint: str) -> list[int]:
    channels = []
    headers = get_co_headers(lkey=lkey)
    api_endpoint = f"https://{endpoint}/api/v3/channels/?limit=1000"
    # Fetch group channels
    channel_request = requests.get(
        url=api_endpoint,
        headers=headers,
        timeout=10
    )
    if channel_request.status_code != 200:
        logging.error("Failed to get channels: %s", channel_request.text)
        return []

    resp = channel_request.json()

    # Build list of channels
    for channel in resp["objects"]:
        channels.append(channel["id"])

    # Get additional channels if account has >1000 channels
    while resp["meta"]["next"]:
        api_endpoint = f"https://{endpoint}{resp['meta']['next']}"
        channel_request = requests.get(
            url=api_endpoint,
            headers=headers,
            timeout=10
        )
        if channel_request.status_code != 200:
            logging.error("Failed to get channels: %s", channel_request.text)
            return []

        resp = channel_request.json()

        # Build list of channels
        for channel in resp["objects"]:
            channels.append(channel["id"])

    logging.info("Successfully got all channels: %s", str(channels))
    return channels


def add_channels_to_site(cg_id: int, channels: list[int], lkey: str, endpoint: str) -> str:
    '''
    return: token from channel_group
    '''
    headers = get_co_headers(lkey=lkey)
    api_endpoint = f"https://{endpoint}/api/v3/channel_groups/{cg_id}/"
    data = {
        "channels": channels
    }
    cg_request = requests.put(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )

    if cg_request.status_code != 200:
        logging.error("Failed to update channel group: %s", cg_request.text)
        return ""
    
    resp = cg_request.json()
    logging.info("Successfully added channels to channel group.")
    return resp["token"]


def update_site_group_token(auth_token: str, group_token: str, site_id: int, endpoint: str):
    headers = get_ct_headers(token=auth_token)
    api_endpoint = f"https://{endpoint}/v1/site/{site_id}"
    data = {
        "groupToken": group_token
    }
    site_request = requests.patch(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )

    if site_request.status_code != 200:
        logging.error("Failed to update group token for size.")
        return
    
    logging.info("Successfully updated site group token.")


def update_channel_meta(ch_id: int, lkey: str, endpoint: str, site_id: int):
    # { "data": "NOPLAN", "tag": "planId"}
    # { "data": "siteId", "tag": str(site_id)}
    # { "data": str(siteId), "tag": "siteId"}
    headers = get_co_headers(lkey=lkey)
    api_endpoint = f"https://{endpoint}/api/v3/channels/{ch_id}/meta/"

    data = {
        "data": "NOPLAN",
        "tag": "planId"
    }
    cg_request = requests.post(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )
    if cg_request.status_code != 201:
        # 400 indicates tag already exists, update it
        if cg_request.status_code == 400:
            meta_api_endpoint = f"{api_endpoint}planId/"
            meta_data = {
                "data": "NOPLAN"
            }
            update_req = requests.put(
                url=meta_api_endpoint,
                headers=headers,
                json=meta_data,
                timeout=10
            )
            if update_req.status_code != 200:
                logging.error("Failed to update channel group meta: %s", update_req.text)
                return
        else:
            logging.error("Failed to update channel group meta: %s", cg_request.text)
            return

    data = {
        "data": "siteId",
        "tag": str(site_id)
    }
    cg_request = requests.post(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )
    if cg_request.status_code != 201:
        # 400 indicates tag already exists, update it
        if cg_request.status_code == 400:
            meta_api_endpoint = f"{api_endpoint}{str(site_id)}/"
            meta_data = {
                "data": "siteId"
            }
            update_req = requests.put(
                url=meta_api_endpoint,
                headers=headers,
                json=meta_data,
                timeout=10
            )
            if update_req.status_code != 200:
                logging.error("Failed to update channel group meta: %s", update_req.text)
                return
        else:
            logging.error("Failed to update channel group meta: %s", cg_request.text)
            return

    data = {
        "data": str(site_id),
        "tag": "siteId"
    }
    cg_request = requests.post(
        url=api_endpoint,
        headers=headers,
        json=data,
        timeout=10
    )
    if cg_request.status_code != 201:
        # 400 indicates tag already exists, update it
        if cg_request.status_code == 400:
            meta_api_endpoint = f"{api_endpoint}siteId/"
            meta_data = {
                "data": str(site_id)
            }
            update_req = requests.put(
                url=meta_api_endpoint,
                headers=headers,
                json=meta_data,
                timeout=10
            )
            if update_req.status_code != 200:
                logging.error("Failed to update channel group meta: %s", update_req.text)
                return
        else:
            logging.error("Failed to update channel group meta: %s", cg_request.text)
            return

    logging.info("Successfully updated channel %s meta.", str(ch_id))


def main():
    '''
    Required params
        co_endpoint: cloudone api endpoint
        ct_endpoint: cloudtwo api endpoint
        email: cloudtwo email
        password: cloudtwo password
        lkey: cloudone LKey token
    Optional params
        cameras: string of cam_ids to manually add
    '''
    logging.basicConfig(
        format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
        level=os.environ.get("LOGGING", "INFO"),
    )

    parser = argparse.ArgumentParser(description="")

    # Add arguments
    parser.add_argument(
        "--co_endpoint",
        help="URL to Cloudone API for example https://vms.com",
        required=True
    )
    parser.add_argument(
        "--ct_endpoint",
        help="URL to Cloudone API for example https://vms.com",
        required=True
    )
    parser.add_argument(
        "--lkey",
        help="License key for the API V3",
        required=True
    )
    parser.add_argument(
        "--password",
        help="Password for cloudtwo account",
        required=True
    )
    parser.add_argument(
        "--email",
        help="Email for cloudtwo account",
        required=True
    )
    parser.add_argument(
        "--cameras",
        help="List of cameras IDs to move. Example: 123,124,125",
        default=""
    )

    args = parser.parse_args()

    if args.cameras != "":
        # Parse list
        try:
            channels = []
            cameras = args.cameras.split(",")
            for cam in cameras:
                channels.append(int(cam))
        except Exception as e:
            logging.error("Error parsing provided camera IDs.")
            raise Exception(e)
    else:
        # No list provided so we must fetch channels
        channels = get_cloud_one_channels(lkey=args.lkey, endpoint=args.co_endpoint)

    if not channels:
        raise Exception("No channels found.")

    auth_dict = get_cloud_two_auth(
        email=args.email,
        password=args.password,
        endpoint=args.ct_endpoint
    )

    if auth_dict:
        auth_token = auth_dict["access_token"]
        company_id = auth_dict["company_id"]
    else:
        raise Exception("No auth_token or company_id found.")

    add_lkey_to_cloud_two(
        auth_token=auth_token,
        company_id=company_id,
        endpoint=args.ct_endpoint,
        co_endpoint=args.co_endpoint,
        lkey=args.lkey
    )

    site_id = create_cloud_two_site(
        auth_token=auth_token,
        endpoint=args.ct_endpoint
    )

    if not site_id:
        raise Exception("No site id created.")
    
    cg_id = get_channel_group_id_for_site(
        site_id=site_id,
        endpoint=args.co_endpoint,
        lkey=args.lkey
    )

    if not cg_id:
        raise Exception("No channel group found.")

    group_token = add_channels_to_site(
        cg_id=cg_id,
        channels=channels,
        lkey=args.lkey,
        endpoint=args.co_endpoint
    )

    if not group_token:
        raise Exception("No channel group token found.")
    
    update_site_group_token(
        auth_token=auth_token,
        group_token=group_token,
        site_id=site_id,
        endpoint=args.ct_endpoint
    )

    for channel in channels:
        update_channel_meta(
            ch_id=channel,
            lkey=args.lkey,
            endpoint=args.co_endpoint,
            site_id=site_id
        )

    logging.info("Migration completed.")


if __name__ == "__main__":
    main()
