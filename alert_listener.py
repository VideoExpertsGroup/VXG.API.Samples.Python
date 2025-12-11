from time import sleep
from stomp import Connection
import json
import argparse

# This is a sample listener that connects to an ActiveMQ broker and listens for messages on a specific topic.
# Update the host, port, username, and password as needed.
host = ''
port = 61614
username = 'amq'
password = ''
topic = '/topic/alarm-queue-ecs'


class CustomListener(object):
    def __init__(self, cameras=None, alerts=None):
        self.cameras = cameras
        self.alerts = alerts

    def on_error(self, frame):
        print('ERROR: ' + str(frame))

    def on_message(self, frame):
        # parse frame's body to python dictionary
        message = json.loads(frame.body)
        # print('Received message: %s' % message)
        self.filter_message(message)

    def filter_message(self, message):
        camera_matches = (
            True if self.cameras is None else message["camera_id"] in self.cameras
        )
        
        alert_matches = (
            True if self.alerts is None else bool(set(message["alert_rule_ids"]) & set(self.alerts))
        )

        if camera_matches and alert_matches:
            self.print_message(message)

    def print_message(self, message):
        # You can change the logic to handle the message as needed
        print(f"Received message:\n    Alert Rule Name: {message['alert_rule_name']}\n    Alert ID: {message['id']}\n    Event ID: {message['event_id']}\n    Camera ID: {message['camera_id']}\n    Camera Name: {message['camera_name']}\n    Event Type: {message['event']}\n    Time: {message['time']}\n    Image: {message['thumb']['url']}\n    Alert Meta: {message['meta']}\n    Alert Rule IDs: {message['alert_rule_ids']}")


def validate_args(camera_id, alert_id):
    # Split comma-separated values and convert to integers
    if camera_id:
        camera_ids = [int(cid.strip()) for cid in camera_id.split(',')]
    else:
        camera_ids = None

    if alert_id:
        alert_ids = [int(eid.strip()) for eid in alert_id.split(',')]
    else:
        alert_ids = None

    return camera_ids, alert_ids


def main(conn: Connection, cameras=None, alerts=None):
    conn.set_ssl(for_hosts=[(host, port)])

    print('Setting up listener...')
    conn.set_listener('', CustomListener(cameras=cameras, alerts=alerts))

    print('Connecting to the broker...')
    conn.connect(username, password, wait=True)

    print(f'Subscribing to topic: {topic}')
    conn.subscribe(topic, 'a_client_id')

    # An endless loop... Just press Ctrl+C to interrupt it
    print("Listening for messages...")
    while True:
        sleep(2)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--camera_id",
            help="Camera ID(s), comma-separated if multiple",
            type=str,
            required=False,
            default=None
        )

        parser.add_argument(
            "--alert_id",
            help="alert ID(s), comma-separated if multiple",
            type=str,
            required=False,
            default=None
        )

        args = parser.parse_args()
        cameras, alerts = validate_args(args.camera_id, args.alert_id)
        if not cameras:
            print("No camera IDs provided, listening to all cameras.")
        if not alerts:
            print("No alert IDs provided, listening to all alerts.")

        print(f"Listening for messages on topic '{topic}'.")
        connection = Connection(host_and_ports=[(host, port)])
        main(conn=connection, cameras=cameras, alerts=alerts)
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...")
    finally:
        # Ensure the connection is closed gracefully
        connection.disconnect()
