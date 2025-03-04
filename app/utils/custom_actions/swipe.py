from dataclasses import dataclass, fields
from random import random, randint
from time import sleep
import json

from maa.context import Context
from maa.custom_action import CustomAction

from ..maafw import maafw

@maafw.resource.custom_action("VerticalSwipe")
class VerticalSwipe(CustomAction):
    @dataclass
    class CustomParam:
        delta_y: int = 0
        delta_fuzzy_x: int = 5
        delta_x_min: int = 30
        delta_x_max: int = 40
        step_y: int = 20
        step_fuzzy_y: int = 2
        step_time: float = 0.04
        step_fuzzy_time: float = 0.005
        hold_time: float = 0.8
        pass

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        """
        :param argv.box: comes from pipeline "target" & "target_offset", the region from which to randomly pick StartPoint
        :param argv.custom_action_param: comes from pipeline "custom_action_param", str json
        :param context: 运行上下文
        :return: 是否执行成功。-参考流水线协议 `on_error`
        """
        # First determine the Start Point and the End Point, make a horizontal 30-40 pxs touch_move to enter the swipe mode, then move step by step to the End Point
        # parse argv
        # params = json.loads(argv.custom_action_param)
        custom_param = self.CustomParam(**{k: v for k, v in json.loads(argv.custom_action_param).items() if k in (f.name for f in fields(self.CustomParam))})
        # determine the Start Point from argv.box
        start_point = (randint(argv.box.x, argv.box.x + argv.box.w), randint(argv.box.y, argv.box.y + argv.box.h))
        # determine the End Point, fuzzy x and determined y
        end_point = (start_point[0] + randint(-custom_param.delta_fuzzy_x, custom_param.delta_fuzzy_x), start_point[1] + custom_param.delta_y)
        # make a horizontal 30-40 pxs touch_move to enter the swipe mode
        first_point = (start_point[0] + randint(custom_param.delta_x_min, custom_param.delta_x_max), start_point[1])
        points, delays = [], []        
        points.append(first_point)
        delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
        #points.append(start_point)
        #delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
        while True:
            points.append(self.__get_next_point(end_point, points[-1], custom_param.step_y, custom_param.step_fuzzy_y))
            delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
            if points[-1] == end_point:
                break
        #print(f"start_point: {start_point}, end_point: {end_point}, points: {points}, delays: {delays}")
        

        if not context.tasker.controller.post_touch_down(*start_point).wait().succeeded:
            return False
        for point, delay in zip(points, delays):
            sleep(delay)
            if not context.tasker.controller.post_touch_move(*point).wait().succeeded:
                return False
        sleep(custom_param.hold_time)
        if not context.tasker.controller.post_touch_up().wait():
            return False
        return True
    @staticmethod
    def __get_next_point(end_point: tuple[int, int], prev_point: tuple[int, int], step_y: int, step_fuzzy_y: int) -> tuple[int, int]:
        next_x = randint(end_point[0], prev_point[0])
        if end_point[1] > prev_point[1]:
            next_y = prev_point[1] + step_y + randint(-step_fuzzy_y, step_fuzzy_y)
            if next_y >= end_point[1]:
                return end_point
        else:
            next_y = prev_point[1] - step_y - randint(-step_fuzzy_y, step_fuzzy_y)
            if next_y <= end_point[1]:
                return end_point
        return next_x, next_y

@maafw.resource.custom_action("HorizontalSwipe")
class HorizontalSwipe(CustomAction):
    @dataclass
    class CustomParam:
        delta_x: int = 0
        delta_fuzzy_y: int = 5
        delta_y_min: int = 30
        delta_y_max: int = 40
        step_x: int = 20
        step_fuzzy_x: int = 2
        step_time: float = 0.04
        step_fuzzy_time: float = 0.005
        hold_time: float = 0.8
        pass

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        """
        :param argv.box: comes from pipeline "target" & "target_offset", the region from which to randomly pick StartPoint
        :param argv.custom_action_param: comes from pipeline "custom_action_param", str json
        :param context: 运行上下文
        :return: 是否执行成功。-参考流水线协议 `on_error`
        """
        # First determine the Start Point and the End Point, make a vertical 30-40 pxs touch_move to enter the swipe mode, then move step by step to the End Point
        # parse argv
        # params = json.loads(argv.custom_action_param)
        custom_param = self.CustomParam(**{k: v for k, v in json.loads(argv.custom_action_param).items() if k in (f.name for f in fields(self.CustomParam))})
        # determine the Start Point from argv.box
        start_point = (randint(argv.box.x, argv.box.x + argv.box.w), randint(argv.box.y, argv.box.y + argv.box.h))
        # determine the End Point, fuzzy y and determined x
        end_point = (start_point[0] + custom_param.delta_x, start_point[1] + randint(-custom_param.delta_fuzzy_y, custom_param.delta_fuzzy_y))
        # make a horizontal 30-40 pxs touch_move to enter the swipe mode
        first_point = (start_point[0], start_point[1] + randint(custom_param.delta_y_min, custom_param.delta_y_max))
        points, delays = [], []        
        points.append(first_point)
        delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
        #points.append(start_point)
        #delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
        while True:
            points.append(self.__get_next_point(end_point, points[-1], custom_param.step_x, custom_param.step_fuzzy_x))
            delays.append(custom_param.step_time + random() * custom_param.step_fuzzy_time)
            if points[-1] == end_point:
                break
        #print(f"start_point: {start_point}, end_point: {end_point}, points: {points}, delays: {delays}")
        

        if not context.tasker.controller.post_touch_down(*start_point).wait().succeeded:
            return False
        for point, delay in zip(points, delays):
            sleep(delay)
            if not context.tasker.controller.post_touch_move(*point).wait().succeeded:
                return False
        sleep(custom_param.hold_time)
        if not context.tasker.controller.post_touch_up().wait():
            return False
        return True
    @staticmethod
    def __get_next_point(end_point: tuple[int, int], prev_point: tuple[int, int], step_x: int, step_fuzzy_x: int) -> tuple[int, int]:
        next_y = randint(end_point[1], prev_point[1])
        if end_point[0] > prev_point[0]:
            next_x = prev_point[0] + step_x + randint(-step_fuzzy_x, step_fuzzy_x)
            if next_x >= end_point[0]:
                return end_point
        else:
            next_x = prev_point[0] - step_x - randint(-step_fuzzy_x, step_fuzzy_x)
            if next_x <= end_point[0]:
                return end_point
        return next_x, next_y
