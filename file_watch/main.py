"""
Created by MBET, 04-Dec-2020

Source:
http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
"""
import os
import sys
import queue
import threading
import time
import logging
from pathlib import Path

import win32net
import win32file
import win32con
import win32netcon
import win32wnet

from file_watch.handle_gef import post_gef_file

logging.basicConfig(
    filename='../file-events.log',
    format='%(asctime)s %(message)s',
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

ACTIONS = {
    1: "Created",
    2: "Deleted",
    3: "Updated",
    4: "Renamed from something",
    5: "Renamed to something",
}

data = {
    "remote": r"\\10.64.32.80\sgput-data",
    "local": "T:",
    "username": os.environ['BOKA_USER'],
    "password": os.environ['BOKA_PWD'],
}

resume = 0
while True:
    (_drives, total, resume) = win32net.NetUseEnum(None, 0, resume)
    for drive in _drives:
        if drive["local"] == "T:":
            try:
                logging.info(f"{drive['local']} mapped to {drive['remote']}")
                if not os.access(drive["local"], os.R_OK):
                    logging.info(f"{drive['local']} not accessible, deleting and remapping drive")
                    os.system("cmd /c net use T: /delete")
                    win32wnet.WNetAddConnection2(
                        win32netcon.RESOURCETYPE_DISK,
                        data["local"],
                        data["remote"],
                        None,
                        data["username"],
                        data["password"],
                        0,
                    )
            finally:
                logging.info(f"{drive['local']} is accessible. Happy watching.")
    if not resume:
        break


def watch_path(path_to_watch, include_subdirectories=True):
    FILE_LIST_DIRECTORY = 0x0001
    h_dir = win32file.CreateFile(
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None,
    )
    while True:
        results = win32file.ReadDirectoryChangesW(
            h_dir,
            1024,
            include_subdirectories,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME
            | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
            | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
            | win32con.FILE_NOTIFY_CHANGE_SIZE
            | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
            | win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None,
        )

        for action, file in results:
            file_name, file_extention = os.path.splitext(file)
            full_filename = os.path.join(path_to_watch, file)
            if not os.path.exists(full_filename):
                file_type = "<deleted>"
            elif os.path.isdir(full_filename):
                file_type = "folder"
            else:
                file_type = "file"
            if action == 1 and file_extention.lower() in [".gef", ".ags"]:
                logging.info(full_filename + ACTIONS.get(action, "Unknown"))
                if file_extention.lower() == ".gef":
                    r = post_gef_file(Path(full_filename))
                    data = r.json()
                    if r.status_code == 409:
                        logging.info(data['detail'])
                    elif r.status_code == 200:
                        logging.info(data['message'])
                    else:
                        logging.info("failed")
                if file_extention.lower() == ".ags":
                    pass
                yield (file_type, full_filename, ACTIONS.get(action, "Unknown"))


class Watcher(threading.Thread):
    def __init__(self, path_to_watch, results_queue, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self.path_to_watch = path_to_watch
        self.results_queue = results_queue
        self.start()

    def run(self):
        for result in watch_path(self.path_to_watch):
            self.results_queue.put(result)


if __name__ == "__main__":
    PATH_TO_WATCH = [
        r"T:\08_General\Tekong_Project\0.1 Soil Investigation\(001) Progress Report"
    ]

    try:
        path_to_watch = sys.argv[1].split(",") or PATH_TO_WATCH
    except:
        path_to_watch = PATH_TO_WATCH

    path_to_watch = [os.path.abspath(p) for p in path_to_watch]

    logging.info(f"Watching {', '.join(path_to_watch)}")

    files_changed = queue.Queue()

    for p in path_to_watch:
        Watcher(p, files_changed)

    while True:
        try:
            file_type, filename, action = files_changed.get_nowait()
        except queue.Empty:
            pass
        time.sleep(1)
