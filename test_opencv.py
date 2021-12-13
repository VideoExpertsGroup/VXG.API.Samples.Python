"""Test for resize images from VXG Server use opencv."""
import io
import os
import cv2
import requests
import argparse
from datetime import datetime, timedelta
from urllib.parse import urlencode
import numpy as np


def converted_image(image, network_size):
    """
    :param image: source image
    :return: resized image
    """
    try:
        return cv2.resize(image, network_size)
    except Exception as ex:
        raise Exception(f'Exception converted_image: {ex}')

def get_images(token: str, period: int) -> list:
    """Get images from VXG Cloud."""
    try:
        headers = {
            'accept': 'application/json',
            'Authorization': 'SI %s' % token,
        }
        uri = "http://web.skyvr.videoexpertsgroup.com"
        end = datetime.utcnow()
        start = end - timedelta(seconds=period)
        origin = 'generated_from_live'
        query = [
            ('start', start),  # TODO start.isoformat()
            ('end', end),  # TODO end.isoformat()
            ('origin', origin),
            ('order_by', '-time')
        ]
        url = '%s/api/v2/storage/thumbnails/?%s' % (uri, urlencode(query,
                                                                   safe=','))
        if not os.path.exists('images'):
            os.makedirs('images')

        resp = requests.get(url=url, headers=headers, timeout=10).json()
        return resp.get('objects', [])
    except Exception:
        return []


def resize_and_save_image(image, img_id):
    cv2.imwrite(f"images/image-{img_id}-original.jpg", image)
    conv_image = converted_image(  # resize in 4 times
        image, tuple(int(v / 2) for v in image.shape[-2::-1]))
    cv2.imwrite(f"images/image-{img_id}-transform.jpg", conv_image)


def save_image_with_pedestrians(image, img_id, pedestrians):
    for (x, y, w, h) in pedestrians:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(image, 'Human', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2)
    cv2.imwrite(f"images/image-{img_id}-original.jpg", image)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Group token', required=True)
    parser.add_argument('-p', '--period', type=int, help='Perod time',
                        default=3600)
    parser.add_argument('-f', '--file', help='Cascade model file',
                        default='Samples/haarcascade_fullbody.xml')
    param = parser.parse_args()

    pedestrian_tracker = cv2.CascadeClassifier(param.file)

    for obj in get_images(token=param.token, period=param.period):
        img_resp = requests.get(obj['url'], timeout=10)
        img = cv2.imdecode(
            np.frombuffer(io.BytesIO(img_resp.content).read(), np.uint8),
            cv2.IMREAD_COLOR
        )
        # resize_and_save_image(image=img, img_id=obj['id'])
        # convert color image to grey image
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pedestrians = pedestrian_tracker.detectMultiScale(gray_img, 1.01)
        print(pedestrians)
        if len(pedestrians):
            save_image_with_pedestrians(image=img, img_id=obj['id'],
                                        pedestrians=pedestrians)


if __name__ == '__main__':
    main()