# coding:utf-8

#import maa
from maa.tasker import Tasker
from maa.toolkit import Toolkit, AdbDevice
from maa.resource import Resource
from maa.controller import AdbController

from pathlib import Path
import json
from time import sleep, time

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
        sleep(0.2)
    tasker.post_stop()
    return False, job.get()

def replay_single_battle_action(tasker: Tasker, action: str) -> bool:
    #battle actions: 1. fs(2|3) Focus Shot, 2. ss(2|3) Spread Shot, 3. sw Switch, 4. ba(2) Back, 5. sc(1-5) Spell Card, 6. sk(1-9) Skill, 
    #               7. en(2|3)(1-2|3) Enemy Target, 8. bo(1-3|m) Boost, 9. gr(1-3|m) Graze
    if action[:2] == "fs":
        if action[-1] in "23":
            repeat_times = int(action[-1])
        else:
            repeat_times = 1
        for i in range(repeat_times):
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_focus_shot"]}})
            if not b_success:
                return False
            del (b_success, job)
    elif action[:2] == "ss":
        if action[-1] in "23":
            repeat_times = int(action[-1])
        else:
            repeat_times = 1
        for i in range(repeat_times):
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_spread_shot"]}})
            if not b_success:
                return False
            del (b_success, job)
    elif action[:2] == "sw":
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                                pipeline_override={"Common_Entrance":{"next":["battle_switch"]}})
        if not b_success:
            return False
        del (b_success, job)
    elif action[:2] == "ba":
        if action[-1] in "2":
            repeat_times = int(action[-1])
        else:
            repeat_times = 1
        for i in range(repeat_times):
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_back"]}})
            if not b_success:
                return False
            del (b_success, job)
    elif action[:2] == "sc":
        # first toggle spell card menu
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                pipeline_override={"Common_Entrance":{"next":["battle_spell_card_toggle_menu"]}})
        if not b_success:
            return False
        del (b_success, job)
        # then tap spell card
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                pipeline_override={"Common_Entrance":{"next":["battle_spell_card_tap_" + action]}})
        if not b_success:
            return False
        del (b_success, job)
    elif action[:2] == "sk":
        # first toggle skill menu
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                pipeline_override={"Common_Entrance":{"next":["battle_skill_toggle_menu"]}})
        if not b_success:
            return False
        del (b_success, job)
        # then tap skill and confirm
        for skill in list(action[2:]):
            entry = "battle_skill_tap_sk" + skill
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                                    pipeline_override={"Common_Entrance":{"next":[entry]}, 
                                                                       entry: {"next":["battle_skill_confirm"]}})
            if not b_success:
                return False
            del (b_success, job)
        # toggle skill menu
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                pipeline_override={"Common_Entrance":{"next":["battle_skill_toggle_menu"]}})
        if not b_success:
            return False
        del (b_success, job)
    elif action[:2] == "en":
        match action:
            case "en31" | "en21":
                entry = "battle_choose_enemy_en31"
            case "en32":
                entry = "battle_choose_enemy_en32"
            case "en33" | "en22":
                entry = "battle_choose_enemy_en33"
            case _:
                entry = "battle_choose_enemy_en32"
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                pipeline_override={"Common_Entrance":{"next":[entry]}})
        if not b_success:
            return False
        del (b_success, job)
    elif action[:2] == "bo":
        if action[-1] in "123":
            repeat_times = int(action[-1])
        else:
            repeat_times = 1
        for i in range(repeat_times):
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_boost_tap"]}})
            if not b_success:
                return False
            del (b_success, job)
    elif action[:2] == "gr":
        if action[-1] in "123":
            repeat_times = int(action[-1])
        else:
            repeat_times = 1
        for i in range(repeat_times):
            b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_graze_tap"]}})
            if not b_success:
                return False
            del (b_success, job)
    else:
        return False
    return True

def replay_battle_actions(tasker: Tasker, actions: list) -> bool:
    """Replay battle actions.

    Args:
        tasker (Tasker): The Tasker instance to use.
        actions (list): The battle actions to replay.
    """
    for line in actions:
        # Wait for waiting order state
        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=120, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_Flag_seen_turn_flag", "battle_Flag_seen_game_over"], 
                                                                                          "timeout":180000,
                                                                                          "interrupt":["Common_retry_on_network_timeout_dialog"]}})
        if not b_success:
            return False
        elif job.nodes[-1].name == "battle_Flag_seen_game_over":
            # Game Over. Leave
            return False
        del (b_success, job)
        # Replay one group of actions
        for act in line.split():
            # Replay action 
            if not replay_single_battle_action(tasker, act):
                # Failed to replay one action, exit
                return False
            pass
        pass
    return True

def replay_eternal_battle(tasker: Tasker, record: dict) -> bool:

    scene = 1.1
    while True:
        match scene:
            # Scene01: Start from the eternal battle menu: select the desired difficulty (easy, hard, lunatic) and navigate to the prepare screen
            # Actions: 1. Verify menu presence, 2. Determine current difficulty, 3. Choose the appropriate difficulty, 4. Proceed to the prepare screen
            # DONE: Implement difficulty selection
            case 1.1:
                # Verify eternal battle, difficulty, entrance presence    
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_at_entrance"]},
                                                                            "eternal_battle_Flag_at_entrance":{"next":["battle_Flag_get_difficulty"]},
                                                                            "battle_Flag_get_difficulty":{"next":["eternal_battle_Flag_seen_entrance"]}})
                if not b_success:
                    return False
                del (b_success, job)
                scene = 1.2
            case 1.2:
                # Choose difficulty
                difficulty = record.get("difficulty")
                match difficulty:
                    case "lunatic" | "hard" | "normal":
                        entry = "battle_difficulty_goto_" + difficulty
                    case _:
                        print("Error: 难度不是 lunatic hard normal 中的一个")
                        return False
                
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                                            pipeline_override={"Common_Entrance":{"next":[entry]}})
                if not b_success:
                    return False
                del (b_success, job)
                scene = 1.3
            case 1.3:   
                # Enter prepare screen
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_tap_entrance"]},
                                                                            "eternal_battle_tap_entrance":{"next": "eternal_battle_Flag_seen_entrance"},
                                                                            "eternal_battle_Flag_seen_entrance":{"inverse":True}})
                if not b_success:
                    return False
                del (b_success, job)
                scene = 2.1
            # Scene02: In the prepare screen: We assume the parties are correctly saved. Confirm the parties and then click the start button, or click start if in interrupted state
            # Actions: 1. Verify prepare screen presence, 2. Check if in interrupted state, 3. Click the confirm button, 4. Click the start button
            # DONE: pipelines for Scene02
            case 2.1: 
                # Verify prepare screen presence & check if in interrupted state
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=120, 
                                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_prepare_chars_01"], "timeout":180000, 
                                                                                                  "interrupt":["Common_retry_on_network_timeout_dialog"]},
                                                                            "eternal_battle_Flag_prepare_chars_01":{"next":["eternal_battle_Flag_prepare_chars_02"]},
                                                                            "eternal_battle_Flag_prepare_chars_02":{"next":["eternal_battle_Flag_seen_confirm_button", 
                                                                                                                            "eternal_battle_Flag_seen_start_button"]}})
                if not b_success:
                    return False
                match job.nodes[-1].name:
                    case "eternal_battle_Flag_seen_confirm_button":
                        b_start_from_interrupt = False
                    case "eternal_battle_Flag_seen_start_button":
                        b_start_from_interrupt = True
                    case _:
                        return False
                del (b_success, job)
                scene = 2.2
            case 2.2:
                # Find which area is next
                start_area = "area1"
                if b_start_from_interrupt:
                    b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_next_area_mark_at_2", "eternal_battle_Flag_next_area_mark_at_3",
                                                                                        "eternal_battle_Flag_next_area_mark_at_4", "eternal_battle_Flag_next_area_mark_at_5"]}})
                    if not b_success:
                        print("Error: 找不到下一个挑战的区域")
                        return False
                    start_area = "area" + job.nodes[-1].name[-1]
                    del (b_success, job)
                scene = 2.3
            case 2.3:
                # Tap confirm till seen start
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_start_button"], 
                                                                                                "interrupt":["eternal_battle_tap_confirm_button"]}})
                if not b_success:
                    return False
                del (b_success, job)
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_start_button"], 
                                                                                                "interrupt":["battle_confirm_on_not_enough_yaruki_dialog", 
                                                                                                             "eternal_battle_tap_start_button"]},
                                                                            "eternal_battle_Flag_seen_start_button":{"inverse":True, "threshold":0.7}})
                if not b_success:
                    return False
                del (b_success, job)
                scene = 3.1
            # Scene03: In the game: First leave Full Auto mode if we are in it, then restart battle. 
            # Actions: 1. Check Full Auto Button, 2. Click Full Auto Button, 3. Restart battle 
            # DONE: implement full auto & restart battle
            case 3.1:
                b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=60, 
                                                            pipeline_override={"Common_Entrance":{"timeout": 60000,
                                                                                                  "next":["battle_Flag_seen_full_auto_disabled",
                                                                                                          "battle_Flag_seen_full_auto_enabled"]}})
                if not b_success:
                    return False
                match job.nodes[-1].name:
                    case "battle_Flag_seen_full_auto_disabled":
                        b_full_auto_off = True
                    case "battle_Flag_seen_full_auto_enabled":
                        b_full_auto_off = False
                    case _:
                        return False
                del (b_success, job)
                if not b_full_auto_off:
                    b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                            pipeline_override={"Common_Entrance":{"next":["battle_Flag_seen_full_auto_disabled"],
                                                                                  "interrupt":["battle_tap_full_auto_enabled"]}})
                    if not b_success:
                        return False
                    del (b_success, job)
                scene = 4.1
            # Scene04: In the game: Do the battle actions according to our battle script.
            # Actions: 1. Make sure we are in the game, 2. implement battle script 3. implement battle actions
            case 4.1:
                # DONE: battle actions: 1. fs(2|3) Focus Shot, 2. ss(2|3) Spread Shot, 3. sw Switch, 4. ba(2) Back, 5. sc(1-5) Spell Card, 6. sk(1-9) Skill, 
                # 7. en(2|3)(1-2|3) Enemy Target, 8. bo(1-3|m) Boost, 9. gr(1-3|m) Graze
                #print("Start replay from " + start_area)
                b_retry = False
                for area, area_actions in record.get("actions").items():
                    if area < start_area:
                        continue
                    else:
                        replay_battle_actions(tasker=tasker, actions=area_actions)
                    # After battle actions replayed, check state
                    b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=120, 
                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory", "battle_Flag_seen_turn_flag", 
                                                                                          "battle_Flag_seen_game_over"], "timeout":180000,
                                                                                  "interrupt":["battle_tap_get_reward", "Common_retry_on_network_timeout_dialog"]}})
                    if not b_success:
                        # Try press back to escape from unexpected stuck in battle
                        b_success, job = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=30, 
                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory", "battle_Flag_seen_turn_flag", 
                                                                                          "battle_Flag_seen_game_over"], "timeout":60000,
                                                                                  "interrupt":["battle_tap_get_reward", "Common_retry_on_network_timeout_dialog", 
                                                                                               "Common_Press_Key_Back"]}})
                    if not b_success:
                        return False
                    elif job.nodes[-1].name == "eternal_battle_Flag_seen_victory":
                        # Victory is expected, tap next
                        b_success1, job1 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                            pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory"], 
                                                                                  "interrupt":["eternal_battle_tap_victory_next_button"]}, 
                                                                "eternal_battle_Flag_seen_victory":{"inverse":True}})
                        if not b_success1:
                            return False
                        del (b_success1, job1)
                    elif job.nodes[-1].name == "battle_Flag_seen_turn_flag":
                        # Still in battle after replay. Might want to retry
                        b_success1, job1 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=20, 
                                            pipeline_override={"Common_Entrance":{"next":["battle_tap_restart_button"], 
                                                                                  "interrupt":["battle_toggle_menu"]}, 
                                                                "battle_tap_restart_button":{"next":["battle_tap_restart_confirm_button"],
                                                                                             "interrupt":["battle_tap_restart_button"]}})
                        if not b_success1:
                            return False
                        del (b_success1, job1)
                        b_retry = True
                        start_area = area
                        break
                    elif job.nodes[-1].name == "battle_Flag_seen_game_over":
                        # Game Over. Proceed to entrance
                        b_success1, job1 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_Entrance", timeout=10, 
                                            pipeline_override={"Common_Entrance":{"next":["battle_Flag_seen_game_over"], 
                                                                                  "interrupt":["battle_tap_next_on_game_over"]}, 
                                                                "battle_Flag_seen_game_over":{"inverse":True}})
                        if not b_success1:
                            return False
                        del (b_success1, job1)
                        return False
                    del (b_success, job)
                if not b_retry:
                    scene = 9.1
            case 9.1:
                # end
                break
        #print("Next Scene: Scene", scene)

    # Scene05: Get Reward and next:
    # DONE: Merged into 4.1

    # Scene06: Game Over
    # DONE: Merged into 4.1

    # Scene07: Low Yaruki confirm
    # DONE: Merged into 2.3
    return True


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
    #b1, r1 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_One_Time_Runner", pipeline_override={})
    #b2, r2 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="Common_One_Time_Runner", pipeline_override={"Common_One_Time_Runner":{"next":["Common_One_Time_Runner"]}})
    #b2, r2 = mlw_run_pipeline_with_timeout(tasker=tasker, entry="battle_difficulty_goto_lunatic", pipeline_override={})
    #print(b1)
    #print(r1)
    #print(b2)
    #print(r2)
    while True:
        b_res = replay_eternal_battle(tasker=tasker, record=eternal_battle_record)
        if not b_res:
            print("Run Failed once. Please notice.")
        with open('stop.json', 'r', encoding='UTF-8') as file:
            data = json.load(file)
        if data.get("stop"):
            break

    #interact(local=locals())
    #print(repr(task_detail))
    




if __name__ == "__main__":
    main()