import json
from datetime import datetime, timedelta
from utils import is_user_active, active_window_details, processes_exes, get_window_title_by_pid
from config import inactivity_threshold_seconds, usage_data_folder, check_app_running
from aggregate import main as aggregate_data
import threading

check_app_running()

inactive = False


def get_current_date():
    return datetime.now().strftime("%d-%m-%Y")


usage_data_file = f"{usage_data_folder}/{get_current_date()}.json"
last_write_time = datetime.now()
last_update_time = datetime.now()
last_date = datetime.now().date()

try:
    with open(usage_data_file, 'r') as file:
        usage_data = json.load(file)
except FileNotFoundError:
    usage_data = {}


def update_usage_data():
    global usage_data, last_update_time, inactive
    if datetime.now() - last_update_time > timedelta(seconds=5):
        last_update_time = datetime.now() - timedelta(seconds=1)
    process_name, _, _, window_title, command, success = active_window_details()
    if not success:
        return
    if is_user_active():
        inactive = False
        if process_name in usage_data:
            if window_title in usage_data[process_name]:
                usage_data[process_name][window_title] += (datetime.now() - last_update_time).total_seconds()
            else:
                usage_data[process_name][window_title] = (datetime.now() - last_update_time).total_seconds()
        else:
            usage_data[process_name] = {window_title: (datetime.now() - last_update_time).total_seconds()}
    elif not inactive:
        inactive = True
        if process_name in usage_data and window_title in usage_data[process_name]:
            usage_data[process_name][window_title] -= inactivity_threshold_seconds
    last_update_time = datetime.now()


def background_collect():
    pass


print("Tracking usage activity...")
while True:
    update_usage_data()
    if datetime.now() - last_write_time > timedelta(seconds=1):
        with open(usage_data_file, 'w') as file:
            json.dump(usage_data, file, indent=4)
            last_write_time = datetime.now()
    if datetime.now().date() != last_date:
        print("New day, aggregating data")
        with open(usage_data_file, 'w') as file:
            json.dump(usage_data, file, indent=4)
        last_date = datetime.now().date()
        usage_data = {}
        aggregate_data()
    usage_data_file = f"{usage_data_folder}/{get_current_date()}.json"
