# coding:utf-8

#import maa
from maa.tasker import Tasker
from maa.toolkit import Toolkit, AdbDevice
from maa.resource import Resource
from maa.controller import AdbController

from pathlib import Path

from time import time

from code import interact

# for register decorator
resource = Resource()


def mlw_run_pipeline_with_timeout(tasker: Tasker, entry: str, pipeline_override: dict = {}, timeout: int = 10) -> tuple[bool, object]:
    """Run a pipeline task with a timeout.

    Args:
        tasker (Tasker): The Tasker instance to use.
        entry (str): The pipeline entry to run.
        pipeline_override (dict, optional): The pipeline override. Defaults to {}.
        timeout (int, optional): The timeout in seconds. Defaults to 10.

    Returns:
        tuple[bool, object]: A tuple of a boolean indicating whether the task was completed successfully,
            and the job result if the task was completed.
    """
    time_start = time()
    job = tasker.post_task(entry, pipeline_override)
    while (time() - time_start) < timeout:
        if job.done:
            return True, job.get()
    tasker.post_stop()
    return False, job.get()

def main():
    # maa.toolkit.Toolkit.pi_run_cli("./assets/resource/base", "./assets/cache", False)
    user_path = "./assets/cache"
    resource_path = "./assets/resource/base"

    Toolkit.init_option(user_path)

    res_job = resource.post_bundle(resource_path)
    res_job.wait()

    adb_device = AdbDevice(
        name = "MuMu12-test",
        adb_path = Path("C:/Program Files/Netease/MuMu Player 12/shell/adb.exe"),
        address = "127.0.0.1:16416",
        screencap_methods = 71,     # 64 4 2 1
        input_methods = 4,         # DON'T USE 8 On Mumu
        config = {'extras': {'mumu': {'enable': True, 'index': 1, 'path': 'C:/Program Files/Netease/MuMu Player 12'}}},
    )
    controller = AdbController(
        adb_path=adb_device.adb_path,
        address=adb_device.address,
        screencap_methods=adb_device.screencap_methods,
        input_methods=adb_device.input_methods,
        config=adb_device.config,
    )
    controller.post_connection().wait()

    tasker = Tasker()
    # tasker = Tasker(notification_handler=MyNotificationHandler())
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Failed to init MAA.")
        exit()

    #task_detail = tasker.post_task("Common_One_Time_Runner",pipeline_override={"Common_One_Time_Runner":{"next":["Peek_OCR"]}}).wait().get()
    b1, r1 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_One_Time_Runner", pipeline_override={})
    #b2, r2 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_One_Time_Runner", pipeline_override={"Common_One_Time_Runner":{"next":["Common_One_Time_Runner"]}})
    b2, r2 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="battle_difficulty_goto_lunatic", pipeline_override={})
    print(b1)
    print(r1)
    print(b2)
    print(r2)

    interact(local=locals())
    #print(repr(task_detail))
    



# IN: choose difficulty (easy hard lunatic)
# IN: battle script
def play_eternalbattle():
    # TODO: add a function to play eternal battle
    # Scene01: We start from the menu of eternal battle: choose desired difficulty (easy hard lunatic) and then enter the prepare screen
    # Actions: 1. Make sure we are in the menu, 2. Check difficulty, 3. Select difficulty, 4. Enter the prepare screen
    # DONE: select difficulty

    # Scene02: In the prepare screen: We assume the parties are correctly saved. Confirm the parties and then click the start button, or click start if in interupted state
    # Actions: 1. Make sure we are in the prepare screen, 2. Check if in interupted state (search for area), 3. Click the confirm button, 4. Click the start button
    # DONE: pipelines for Scene02

    # Scene03: In the game: First leave Full Auto mode if we are in it, then restart battle. 
    # Actions: 1. Check Full Auto Button, 2. Click Full Auto Button, 3. Restart battle 
    # DONE: implement full auto & restart battle

    # Scene04: In the game: Do the battle actions according to our battle script.
    # Actions: 1. Make sure we are in the game, 2. implement battle script 3. implement battle actions
    # TODO: battle script
    # DONE: battle actions: 1. fs(2|3) Focus Shot, 2. ss(2|3) Spread Shot, 3. sw Switch, 4. ba(2|3) Back, 5. sc(1-5) Spell Card, 6. sk(1-9) Skill, 
    # 7. en(2|3)(1-2|3) Enemy Target, 8. bo(1-3|m) Boost, 9. gr(1-3|m) Graze

    # Scene05: Get Reward and next:
    # DONE: pipelines for victory

    # Scene06: Game Over
    # DONE: tap next on failure

    # Scene07: Low Yaruki confirm
    # DONE: tap confirm when Yaruki is empty on start battle

    pass


if __name__ == "__main__":
    main()