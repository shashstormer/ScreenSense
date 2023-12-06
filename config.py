import os
import psutil

inactivity_threshold_seconds = 300
usage_data_folder = "usage_data"
aggregate_data_folder = "summary"
more_precise_data_folder = "precise_data"
os.makedirs(usage_data_folder, exist_ok=True)
exclude_from_total_time = ["LockApp.exe"]


def check_app_running():
    try:
        with open("pid.txt") as f:
            pid = int(f.read())
            try:
                psutil.Process(pid)
                print("Already running")
                exit(0)
            except psutil.NoSuchProcess:
                pass
    except FileNotFoundError:
        pass
    with open("pid.txt", "w") as f:
        f.write(str(os.getpid()))
