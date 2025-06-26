# app/player/eternal_battle_player.py

import threading 
import json
import time
from time import sleep, time, localtime, strftime

from maa.tasker import Tasker

from .player import Player
from ..utils.logger import logger

class EternalBattlePlayer(Player):
    def __init__(
        self, *,
        tasker: Tasker,
        recordfile: str,
        repeat_times: int = 9999
    ):
        threading.Thread.__init__(self)
        self.tasker = tasker
        self.recordfile = recordfile
        self.repeat_times = repeat_times
        self.b_stop = False
        self.load_recordfile()
        self.__run_ppl = mlw_run_pipeline_with_timeout

    def run(self):
        while self.repeat_times > 0 and not self.b_stop:
            logger.info("%s Replaying. %s Times Remaining...", self, self.repeat_times)
            b_res = self.__replay_eternal_battle()
            if not b_res:
                logger.warning("%s Run Failed once. Please notice.", self)
            else:
                pass
            self.repeat_times -= 1
            if not threading.main_thread().is_alive():
                break
        pass

    def post_stop(self):
        """Sets the stop flag to True, indicating that the player should stop gracefully.
        
        This method sets the `b_stop` attribute to True and logs a message indicating
        that the player has received a stop signal and will stop gracefully. Consider
        adding logging functionality for better tracking and debugging.
        """

        self.b_stop = True
        logger.info("%s Get Stop Signal, Will Stop Gracefully. Please Wait...", self)

    def force_stop(self):
        """Forces the player to stop executing any more actions and stop soon.

        This method immediately sets the `b_stop` attribute to True and replaces the
        `__run_ppl` function with a dummy function that always returns False. This
        prevents the player from executing any more actions and stops the player
        as soon as possible. The player will finish the current action and then
        stop.

        This method is useful when you want to immediately stop the player from
        executing any more actions."""
        self.b_stop = True
        # Replace the Driver function to a dummy one
        self.__run_ppl = lambda *args, **kwargs: (bool(False), object())
        logger.info("%s Get Force Stop Signal, Will Do No More Actions and Stop Soon. Please Wait...", self)
        pass

    def load_recordfile(self):
        """
        Loads the record data from the specified JSON file into the `self.record` attribute.

        This method opens the file defined by `self.recordfile`, reads its contents,
        and deserializes the JSON data into a Python dictionary assigned to `self.record`.

        Note: This method currently does not parse the record data beyond loading it
        from the file.
        """

        with open(self.recordfile, 'r', encoding='UTF-8') as file:
            self.record = json.load(file)
        # TODO maybe parse record here, not doing it now

    def __replay_eternal_battle(self) -> bool:
        scene = 1.1
        while True:
            match scene:
                # Scene01: Start from the eternal battle menu: select the desired difficulty (easy, hard, lunatic) and navigate to the prepare screen
                # Actions: 1. Verify menu presence, 2. Determine current difficulty, 3. Choose the appropriate difficulty, 4. Proceed to the prepare screen
                # DONE: Implement difficulty selection
                case 1.1:
                    # Verify eternal battle, difficulty, entrance presence    
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
                                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_at_entrance"]},
                                                                                "eternal_battle_Flag_at_entrance":{"next":["battle_Flag_get_difficulty"]},
                                                                                "battle_Flag_get_difficulty":{"next":["eternal_battle_Flag_seen_entrance"]}})
                    if not b_success:
                        return False
                    del (b_success, job)
                    scene = 1.2
                case 1.2:
                    # Choose difficulty
                    difficulty = self.record.get("difficulty")
                    match difficulty:
                        case "lunatic" | "hard" | "normal":
                            entry = "battle_difficulty_goto_" + difficulty
                        case _:
                            logger.error("%s Unknown Difficulty %s! Must be one of {lunatic hard normal} ", self, difficulty)
                            return False
                    
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
                                                                pipeline_override={"Common_Entrance":{"next":[entry]}})
                    if not b_success:
                        return False
                    del (b_success, job)
                    scene = 1.3
                case 1.3:   
                    # Enter prepare screen
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
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
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=120, 
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
                        b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_next_area_mark_at_2", "eternal_battle_Flag_next_area_mark_at_3",
                                                                                            "eternal_battle_Flag_next_area_mark_at_4", "eternal_battle_Flag_next_area_mark_at_5"]}})
                        if not b_success:
                            logger.error("%s Cannot Find Next Area Mark", self)
                            return False
                        start_area = "area" + job.nodes[-1].name[-1]
                        del (b_success, job)
                    scene = 2.3
                case 2.3:
                    # Tap confirm till seen start
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=30, 
                                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_start_button"], "timeout": 40000, 
                                                                                                    "interrupt":["eternal_battle_tap_confirm_button"]}})
                    if not b_success:
                        return False
                    del (b_success, job)
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=120, 
                                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_start_button"], "timeout": 180000, 
                                                                                                    "interrupt":["Common_retry_on_network_timeout_dialog", 
                                                                                                                "battle_confirm_on_not_enough_yaruki_dialog", 
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
                    b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=60, 
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
                        b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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
                    b_retry = False
                    for area, area_actions in self.record.get("actions").items():
                        if area < start_area:
                            continue
                        else:
                            self.__replay_battle_actions(actions=area_actions)
                        # After battle actions replayed, check state
                        b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=120, 
                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory", "battle_Flag_seen_turn_flag", 
                                                                                            "battle_Flag_seen_game_over"], "timeout":180000,
                                                                                    "interrupt":["battle_tap_get_reward", "Common_retry_on_network_timeout_dialog"]}})
                        if not b_success:
                            # Try press back to escape from unexpected stuck in battle
                            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=30, 
                                                pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory", "battle_Flag_seen_turn_flag", 
                                                                                            "battle_Flag_seen_game_over"], "timeout":60000,
                                                                                    "interrupt":["battle_tap_get_reward", "Common_retry_on_network_timeout_dialog", 
                                                                                                "Common_Press_Key_Back"]}})
                        if not b_success:
                            return False
                        elif job.nodes[-1].name == "eternal_battle_Flag_seen_victory":
                            # Victory is expected, tap next
                            if self.b_stop:
                                # try to tap interrupt button first
                                b_success1, job1 = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory"], 
                                                                                        "interrupt":["eternal_battle_tap_victory_interrupt_button", 
                                                                                                     "eternal_battle_tap_victory_next_button"]}, 
                                                                        "eternal_battle_Flag_seen_victory":{"inverse":True}})
                                scene = 9.1
                            else:
                                b_success1, job1 = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["eternal_battle_Flag_seen_victory"], 
                                                                                        "interrupt":["eternal_battle_tap_victory_next_button"]}, 
                                                                        "eternal_battle_Flag_seen_victory":{"inverse":True}})
                            if not b_success1:
                                return False
                            del (b_success1, job1)
                        elif job.nodes[-1].name == "battle_Flag_seen_turn_flag":
                            # Still in battle after replay. Might want to retry
                            b_success1, job1 = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
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
                            b_success1, job1 = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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

        # Scene05: Get Reward and next:
        # DONE: Merged into 4.1

        # Scene06: Game Over
        # DONE: Merged into 4.1

        # Scene07: Low Yaruki confirm
        # DONE: Merged into 2.3
        return True
    
    def __replay_battle_actions(self, actions: list) -> bool:
        """Replay battle actions.

        Args:
            tasker (Tasker): The Tasker instance to use.
            actions (list): The battle actions to replay.
        """
        for line in actions:
            # Wait for waiting order state
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=120, 
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
                if not self.__replay_single_battle_action(act):
                    # Failed to replay one action, exit
                    return False
                pass
            pass
        return True
    
    def __replay_single_battle_action(self, action: str) -> bool:
        #battle actions: 1. fs(2|3) Focus Shot, 2. ss(2|3) Spread Shot, 3. sw Switch, 4. ba(2) Back, 5. sc(1-5) Spell Card, 6. sk(1-9) Skill, 
        #               7. en(2|3)(1-2|3) Enemy Target, 8. bo(1-3|m) Boost, 9. gr(1-3|m) Graze
        if action[:2] == "fs":
            if action[-1] in "23":
                repeat_times = int(action[-1])
            else:
                repeat_times = 1
            for i in range(repeat_times):
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                        pipeline_override={"Common_Entrance":{"next":["battle_spread_shot"]}})
                if not b_success:
                    return False
                del (b_success, job)
        elif action[:2] == "sw":
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
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
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                        pipeline_override={"Common_Entrance":{"next":["battle_back"]}})
                if not b_success:
                    return False
                del (b_success, job)
        elif action[:2] == "sc":
            # first toggle spell card menu
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_spell_card_toggle_menu"]}})
            if not b_success:
                return False
            del (b_success, job)
            # then tap spell card
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_spell_card_tap_" + action]}})
            if not b_success:
                return False
            del (b_success, job)
        elif action[:2] == "sk":
            # first toggle skill menu
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                    pipeline_override={"Common_Entrance":{"next":["battle_skill_toggle_menu"]}})
            if not b_success:
                return False
            del (b_success, job)
            # then tap skill and confirm
            for skill in list(action[2:]):
                entry = "battle_skill_tap_sk" + skill
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=20, 
                                                        pipeline_override={"Common_Entrance":{"next":[entry]}, 
                                                                        entry: {"next":["battle_skill_confirm"]}})
                if not b_success:
                    return False
                del (b_success, job)
            # toggle skill menu
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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
            b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
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
                b_success, job = self.__run_ppl(tasker=self.tasker, entry="Common_Entrance", timeout=10, 
                                                        pipeline_override={"Common_Entrance":{"next":["battle_graze_tap"]}})
                if not b_success:
                    return False
                del (b_success, job)
        else:
            return False
        return True


def mlw_run_pipeline_with_timeout(tasker: Tasker, entry: str, pipeline_override: dict = {}, timeout: int = 10, 
                                  pre_wait_stopping_timeout: int = 2, 
                                  post_wait_stopping_timeout: int = 2
                                  ) -> tuple[bool, object]:
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
    while tasker.stopping and (time() - time_start) < pre_wait_stopping_timeout:
        # Wait for the tasker to complete stopping
        sleep(0.01)
        continue
    if tasker.stopping:
        # Error: Tasker is still stopping
        return False, None
    time_start2 = time()
    job = tasker.post_task(entry, pipeline_override)
    while (time() - time_start2) < timeout:
        if job.done:
            return True, job.get()
        sleep(0.01)
        continue
    # Timeout
    tasker.post_stop()
    time_start3 = time()
    while tasker.stopping and (time() - time_start3) < post_wait_stopping_timeout:
        # Wait for the tasker to complete stopping
        sleep(0.01)
        continue
    if tasker.stopping:
        # Error: Tasker is still stopping
        # Best Effort. Cannot handle this better. Shouldn't happen
        pass
    return False, job.get()

