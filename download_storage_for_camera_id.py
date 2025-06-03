import argparse
import requests
import json
import os
from urllib.parse import urlparse, unquote


def request_storage_api(args):
    api_endpoint = f"https://{args.endpoint}"
    path = "/api/v2/storage/data/"
    headers = {
        "Authorization": f"LKey {args.token}"
    }

    # print(f"Requesting storage API: {api_endpoint}{path}")
    # print(f"Camera ID: {args.camera_id}, Start: {args.start}, End: {args.end}")
    # print(f"Headers: {headers}")

    response = requests.get(
        url=f"{api_endpoint}{path}",
        headers=headers,
        params={
            "camid": args.camera_id,
            "start": args.start,
            "end": args.end,
            "order_by": "time",
        },
        timeout=30,
    )
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(
            f"Error with API request: {response.status_code}, {response.text}"
        )


def download_video_segment(url, save_dir="."):
    try:
        # Parse filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        filename = unquote(filename)  # Decodes %20, etc.

        # Full local path to save the file
        local_path = os.path.join(save_dir, filename)
        print(f"Downloading {url} → {local_path}")

        # Stream download to avoid loading whole file in memory
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"Saved: {local_path}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Uses V2 storage API to download video for a camera.")
    parser.add_argument(
        "--camera_id",
        type=int,
        required=True,
        help="The camera ID to download clips for. This is the ID of the camera in the V2 storage API.",
    )
    parser.add_argument(
        "--start",
        type=str,
        required=True,
        help="The start time for the clips to download (format: YYYY-MM-DDTHH:MM:SS).",
    )
    parser.add_argument(
        "--end",
        type=str,
        required=True,
        help="The end time for the clips to download (format: YYYY-MM-DDTHH:MM:SS).",
    )
    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="The channel access token for the camera.",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        help="The API endpoint for the storage service.",
        required=True
    )
    return parser.parse_args()


def main():
    args = parse_args()
    resp = request_storage_api(args)

    if len(resp["objects"]) == 0:
        print("No video segments found for given time range.")
    else:
        for segement in resp["objects"]:
            download_video_segment(segement["url"])


if __name__ == "__main__":
    main()
