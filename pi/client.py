import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

# CONFIG
WATCH_FOLDER = os.getenv('WATCH_DIR')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
API_KEY = os.getenv('API_KEY')


class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"New file detected: {file_path}")

            try:
                with open(file_path, "rb") as f:
                    files = [("files", (os.path.basename(file_path), f))]
                    headers = {"x-api-key": API_KEY}

                    response = requests.post(ENDPOINT_URL,
                                             files=files,
                                             headers=headers)

                if response.status_code == 200:
                    print(
                        f"File {file_path} uploaded successfully. Deleting...")
                    os.remove(file_path)
                else:
                    print(
                        f"Upload failed for {file_path}. Status: {response.status_code}, Response: {response.text}"
                    )

            except Exception as e:
                print(f"Error handling {file_path}: {e}")


if __name__ == '__main__':
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    print(f'Watching folder: {WATCH_FOLDER}')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
