# coding:utf-8

from dataclasses import asdict
from pathlib import Path
import json
from time import sleep, time

from code import interact

#import maa
from maa.tasker import Tasker
from maa.toolkit import Toolkit, AdbDevice
from maa.resource import Resource
from maa.controller import AdbController

from app.player.eternal_battle_player import Player, EternalBattlePlayer


# for register decorator
resource = Resource()


def main():
    user_path = "./assets/cache"
    resource_path = "./assets/resource/base"

    with open('./MLW-config.json', 'r', encoding='UTF-8') as file:
        mlw_config = json.load(file)
        adb_device_info = mlw_config.get("adb_device")
        eternal_battle_record_info = mlw_config.get("eternal_battle_record")
    with open(eternal_battle_record_info.get("path"), 'r', encoding='UTF-8') as file:
        eternal_battle_record = json.load(file)

    Toolkit.init_option(user_path)

    res_job = resource.post_bundle(resource_path)
    res_job.wait()

    adb_device = AdbDevice(
        name = adb_device_info.get("name"),
        adb_path = Path(adb_device_info.get("adb_path")),
        address = adb_device_info.get("address"),
        screencap_methods = adb_device_info.get("screencap_methods"),     # 64 4 2 1
        input_methods = adb_device_info.get("input_methods"),         # DON'T USE 8 On Mumu
        config = adb_device_info.get("config")
    )
    controller = AdbController(**{k:v for k,v in asdict(adb_device).items() if not k == "name"})
    controller.post_connection().wait()

    tasker = Tasker()
    # tasker = Tasker(notification_handler=MyNotificationHandler())
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Failed to init MAA.")
        exit()

    # On Start, Start an EternalBattlePlayer by default for now. Will be removed later
    player = EternalBattlePlayer(tasker=tasker, recordfile=mlw_config.get("eternal_battle_record").get("path"))
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
                    print(player, "is already running")
                elif rest == []:
                    player = EternalBattlePlayer(tasker=tasker, recordfile=mlw_config.get("eternal_battle_record").get("path"))
                    player.start()
                elif rest[0].isdecimal():
                    player = EternalBattlePlayer(tasker=tasker, recordfile=mlw_config.get("eternal_battle_record").get("path"), repeat_times=int(rest[0]))
                    player.start()
                else:
                    print("unknown command")
            case []:
                pass
            case _:
                print("unknown command")
        sleep(0.1)

    #interact(local=locals())
    #print(repr(task_detail))
    




if __name__ == "__main__":
    main()