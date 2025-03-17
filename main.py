# coding:utf-8

from pathlib import Path
import json
from time import sleep

from app.config import config
from app.utils.maafw import maafw, Toolkit, AdbDevice
from app.utils.logger import logger
from app.player.eternal_battle_player import Player, EternalBattlePlayer

def main():

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
    #adb_device.input_methods = 2  # force to use minitouch
    #adb_device.input_methods = 4  # force to use maatouch
    if not maafw.connect_adb_device(adb_device):
        logger.error("Failed to connect adb device.")

    if not maafw.bind_tasker():
        logger.error("Failed to init MaaFramework.")
        exit()

    # On Start, Start an EternalBattlePlayer by default for now. Will be removed later
    player = EternalBattlePlayer(tasker=maafw.tasker, recordfile= config.get('lostword.eternal_battle_record', 'path'))
    player.start()

    command_str = ""
    # Main Loop
    while True:
        # get input
        command = input("Getto > ")
        match command.split():
            case ["exit" | "quit", *rest]:
                break
            case ["stop"]:
                player.post_stop()
            case ["force", "stop"]:
                player.force_stop()
            case ["start", *rest]:
                if player.is_alive():
                    logger.warning("%s is already running", player)
                elif rest == []:
                    player = EternalBattlePlayer(tasker=maafw.tasker, recordfile=config.get('lostword.eternal_battle_record', 'path'))
                    player.start()
                elif rest[0].isdecimal():
                    player = EternalBattlePlayer(tasker=maafw.tasker, recordfile=config.get('lostword.eternal_battle_record', 'path'), repeat_times=int(rest[0]))
                    player.start()
                else:
                    logger.warning("unknown command")
            case []:
                pass
            case _:
                logger.warning("unknown command")
        sleep(0.1)



if __name__ == "__main__":
    main()