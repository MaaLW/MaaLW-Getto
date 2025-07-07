# coding:utf-8

from pathlib import Path
import json
from time import sleep
from queue import PriorityQueue
import threading

from app.config import config
from app.utils.maafw import Toolkit, AdbDevice
from app.utils.maafw.maafw import maafw
from app.utils.logger import logger
from app.player import Player, PlayerFactory
from app.ui.cmd02 import UserInterface02
from app.core import CoreDummy02

def main():
    # StartUp()
    adb_device_info = config["adb_device"]

    if not Toolkit.init_option(maafw.user_path):
        logger.error("Failed to init MaaToolkit.")

    if not maafw.load_resource(maafw.resource_path):
        logger.error("Failed to load resource.")

    adb_device = AdbDevice(
        name = adb_device_info.get("name"),
        adb_path = Path(adb_device_info.get("adb_path")),
        address = adb_device_info.get("address"),
        screencap_methods = adb_device_info.getint("screencap_methods"),     # 64 4 2 1
        input_methods = adb_device_info.getint("input_methods"),         # DON'T USE 8 On Mumu
        config = json.loads(adb_device_info.get("config"))
    )

    if not maafw.connect_adb_device(adb_device):
        logger.error("Failed to connect adb device.")

    if not maafw.bind_tasker():
        logger.error("Failed to init MaaFramework.")
        exit()

    core = CoreDummy02()
    
    def run_user_interface():
        ui = UserInterface02(core=core)
        ui.onecmd("start")
        ui.cmdloop()
    ui_thread = threading.Thread(target=run_user_interface)
    ui_thread.start()

    try:
        ui_thread.join()
    except KeyboardInterrupt:
        print("Main thread interrupted.")
    finally:
        ui_thread.join()
        pass
    return


if __name__ == "__main__":
    main()