# coding:utf-8

from dataclasses import asdict
from pathlib import Path
import json
from time import sleep, time
from dataclasses import dataclass
from random import randint, random
from logging import NOTSET, DEBUG

from code import interact

from app.utils.logger import logger
from app.utils.maafw import Context, CustomAction, Toolkit, AdbDevice
from app.utils.maafw.maafw import maafw
from app.config import config

logger.setLevel(DEBUG)

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

    b, td = maafw.run_ppl("PipelineLab20250427_Entry_01")
    print(b, td)
    print("td.status.succeeded: ", td.status.succeeded)
    print("td.status.done: ", td.status.done)
    print("td.status.failed: ",td.status.failed)
    print("td.status.pending: ", td.status.pending)
    print("td.status.running: ", td.status.running)
    b, td = maafw.run_ppl("PipelineLab20250427_Entry_02")
    print(b, td)
    print("td.status.succeeded: ", td.status.succeeded)
    print("td.status.done: ", td.status.done)
    print("td.status.failed: ",td.status.failed)
    print("td.status.pending: ", td.status.pending)
    print("td.status.running: ", td.status.running)
    
    b, td = maafw.run_ppl("PipelineLab20250426_NeverHitNode", timeout=30)
    print(b, td)
    print("td.status.succeeded: ", td.status.succeeded)
    print("td.status.done: ", td.status.done)
    print("td.status.failed: ",td.status.failed)
    print("td.status.pending: ", td.status.pending)
    print("td.status.running: ", td.status.running)
    try: print(td.nodes.pop().name)
    except: pass
    
    return

    from app.player import Player, ErrandPlayer, EternalBattlePlayer

    player = ErrandPlayer(tasker=maafw.tasker)
    command_str = ""
    # Main Loop
    while True:
        # get input
        command = input("Getto > ")
        match command.split():
            case ["exit" | "quit", *rest]:
                break
            case ["stop"]:
                if isinstance(player, Player) and player.is_alive(): player.stop()
            case ["force", "stop"]:
                if isinstance(player, Player) and player.is_alive(): player.force_stop()
            case ["start", *rest]:
                if player.is_alive():
                    logger.warning("%s is already running", player)
                elif rest == []:
                    player = ErrandPlayer(tasker=maafw.tasker)
                    player.start()
                elif rest[0].isdecimal():
                    player = ErrandPlayer(tasker=maafw.tasker)
                    player.start()
                else:
                    logger.warning("unknown command")
            case []:
                pass
            case _:
                logger.warning("unknown command")
        sleep(0.1)


    return
    td = maafw.tasker.post_task("1",{"1": {"recognition": "custom", "custom_recognition": "ErrandRecoTestBench"}}).wait().get()
    print(td)
    import jsons
    from app.utils.custom.errand import Errand
    from app.utils.datetime import datetime

    return

    td = maafw.tasker.post_task("1",{"1": {"recognition": "custom", "custom_recognition": "ErrandReco"}}).wait().get()
    print(td)
    import jsons
    from app.utils.custom.errand import Errand
    from app.utils.datetime import datetime
    
    l1 = jsons.load(td.nodes[0].recognition.best_result.detail, cls=list[list[Errand],list[Errand]])
    for e in l1[0]+l1[1]:
        print(e)
    return


    td = maafw.tasker.post_task("1",{"1": {"recognition": "custom", "custom_recognition": "ErrandRecoTest1"}}).wait().get()
    #job = maafw.tasker.post_task("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_test").wait().get()
    print(td)
    import jsons
    from app.utils.custom.errand import Errand
    from app.utils.datetime import datetime
    
    l1 = jsons.load(td.nodes[0].recognition.best_result.detail, cls=list[list[Errand],list[Errand]])
    td1 = datetime.now() - l1[0][0].datetime_reco
    print(td1)
    print(datetime.now().tzinfo); print(l1[0][0].datetime_reco.tzinfo)
    print(datetime.now().tzinfo == l1[0][0].datetime_reco.tzinfo)
    for e in l1[0]+l1[1]:
        print(e)
    return
    

    return


    # scroll exchange shop
    while True:
        td = maafw.tasker.post_task("1",{"1": {"action": "custom", "custom_action": "HorizontalSwipe", "target": [80+185*4, 620, 20, 20], 
                                      "custom_action_param": {"delta_x": -185*4, "xxx": 0.5}}}).wait().get()   
        td = maafw.tasker.post_task("1",{"1": {"action": "custom", "custom_action": "HorizontalSwipe", "target": [80, 620, 20, 20], 
                                      "custom_action_param": {"delta_x": 185*4}}}).wait().get()
     
    return

    # scroll vsSpirit Tower tags
    while True:
        td = maafw.tasker.post_task("1",{"1": {"action": "custom", "custom_action": "VerticalSwipe", "target": [1000, 550, 20, 20], 
                                      "custom_action_param": {"delta_y": -400, "hold_time": 0.5}}}).wait().get()
        td = maafw.tasker.post_task("1",{"1": {"action": "custom", "custom_action": "VerticalSwipe", "target": [1000, 300, 20, 20], 
                                      "custom_action_param": {"delta_y": 400, "hold_time": 0.6}}}).wait().get()


    #interact(local=locals())
    #print(repr(task_detail))
    


if __name__ == "__main__":
    main()