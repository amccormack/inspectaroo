import argparse
import boto3
import json
import tempfile
import subprocess
from signal import signal, SIGINT, SIGTERM

# Most code inspired from https://perandrestromhaug.com/posts/writing-an-sqs-consumer-in-python/

OUTPUT_PREFIX="exifdata/"

class SignalHandler:
    def __init__(self):
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, signal, frame):
        print(f"handling signal {signal}, exiting gracefully")
        self.received_signal = True

def inspector_loop(queue_name):
    sqs = boto3.resource("sqs")
    sqs_queue = sqs.get_queue_by_name(QueueName=queue_name)
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        messages = sqs_queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=1)
        for message in messages:
            try:
                process_message(message.body)
            except Exception as e:
                print(f"exception while processing message: {repr(e)}")
                # Delete the message even if we had an error
                # continue 
            message.delete()        

def process_message(message_body: str):
    records = json.loads(message_body).get('Records', [])
    for record in records:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(bucket, key)

def process_file(bucket, key):
    s3 = boto3.client("s3")
    with tempfile.NamedTemporaryFile() as fp:
        s3.download_fileobj(bucket, key, fp)
        print("fp name", fp.name)
        try:
            output = subprocess.check_output(["/usr/bin/exiftool", "-j", fp.name])
        except subprocess.CalledProcessError as e:
            output = force_json(e.output)
    
    noprefix_key = '/'.join(key.split('/')[1:])
    outkey = OUTPUT_PREFIX + noprefix_key + '.exif.json'

    s3.put_object(Body=output, Bucket=bucket, Key=outkey)
    
        

def force_json(s: str) -> bytes:
    try: 
        return json.dumps(json.loads(s)).encode("utf-8")
    except Exception as e:
        return [{"Error":"unknown"}]

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    serve_parser = subparsers.add_parser('serve', help='run the inspector server and listen for sqs notifications')
    serve_parser.add_argument("queue_name")
    serve_parser.set_defaults(func='serve_parser')

    process_file_parser = subparsers.add_parser('process_file', help='Download a file and process it')
    process_file_parser.add_argument("bucket")
    process_file_parser.add_argument("key")
    process_file_parser.set_defaults(func='process_file')

    args = parser.parse_args()
    if 'func' not in args:
        parser.error("Must specify a subparser")
    if args.func == 'serve_parser':
        inspector_loop(args.queue_name)
    if args.func == 'process_file':
        process_file(args.bucket, args.key)
    
if __name__ == '__main__':
    main()