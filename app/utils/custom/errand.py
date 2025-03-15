from enum import StrEnum, auto
from dataclasses import dataclass, field, fields
from time import sleep
from typing import Optional
import json, re

import jsons
from maa.define import Rect
from maa.context import Context
from maa.custom_recognition import CustomRecognition

from ..maafw import maafw
from ..logger import logger
from ..datetime import datetime, time, timedelta

def is_in_rect(r: Rect):
    """
    Returns a function that checks if a given rectangle `r1` is completely
    within the boundaries of rectangle `r`.

    Parameters:
    - r: The reference rectangle within which the check is performed.

    Returns:
    - A function that takes a rectangle `r1` and returns True if `r1` is
      entirely within `r`, otherwise False.
    """

    def _is_in_rect(r1: Rect) -> bool:
        return max(r1.x, r1.x + r1.w) <= max(r.x, r.x + r.w) and min(r1.x, r1.x + r1.w) >= min(r.x, r.x + r.w) and\
              max(r1.y, r1.y + r1.h) <= max(r.y, r.y + r.h) and min(r1.y, r1.y + r1.h) >= min(r.y, r.y + r.h)
    return _is_in_rect

regex_time = re.compile(r"[0-9]{2}:[0-9]{2}:[0-9]{2}")
img_save_path = "./assets/cache/debug/errand/"

@dataclass(frozen=True)
class Dimensions:
    box_t_1st: Rect = field(default_factory=lambda: Rect(230, 60, 980, 189))  # At Top State, box of 1st Errand from top
    box_t_4th: Rect = field(default_factory=lambda: Rect(230, 627, 980, 93)) # At Top State, visible part of 4th Errand from top
    box_b_1st: Rect = field(default_factory=lambda: Rect(230, 523, 980, 189)) # At Bottom State, box of 1st Errand from bottom
    box_b_4th: Rect = field(default_factory=lambda: Rect(230, 57, 980, 88)) # At Bottom State, visible part of 4th Errand from bottom
    origin_t_1st: Rect = field(default_factory=lambda: Rect(230, 60, 0, 0)) # At Top State, origin of 1st Errand from top
    origin_b_1st: Rect = field(default_factory=lambda: Rect(230, 523, 0, 0)) # At Bottom State, origin of 1st Errand from bottom
    offset_one_errand_down: Rect = field(default_factory=lambda: Rect(0, 189, 0, 0)) # Move Down 1 Errand
    offset_one_errand_up: Rect = field(default_factory=lambda: Rect(0, -189, 0, 0)) # Move Up 1 Errand
    offset_b4_2_t1: Rect = field(default_factory=lambda: Rect(0, 104, 0, 0)) # Move from Bottom to Top
    offset_t4_2_b1: Rect = field(default_factory=lambda: Rect(0, -104, 0, 0)) # Move from Top to Bottom
    offset_grow_one_down: Rect = field(default_factory=lambda: Rect(h = 189)) # Grow Down 1 Errand Height
    offset_grow_one_up: Rect = field(default_factory=lambda: Rect(y = -189, h = 189)) # Grow Up 1 Errand Height
    offset_click: Rect = field(default_factory=lambda: Rect(40, 13, -100, -23)) # Shrink for click n swipe
    relative_box_whole_errand: Rect = field(default_factory=lambda: Rect(0, 0, 980, 189)) # add this to origin to get the actual box for whole errand
    relative_box_negative_whole_errand: Rect = field(default_factory=lambda: Rect(0, 0, -980, -189)) # add this to ctual box for whole errand to get the origin
    relative_box_time_expire: Rect = field(default_factory=lambda: Rect(0, 120, 220, 70)) # add this to origin to get the actual box for time expire
    relative_box_time_cost: Rect = field(default_factory=lambda: Rect(250, 80, 240, 90)) # add this to origin to get the actual box for time cost
    pass
@dataclass
class CustomParam:
    num_daily_errands: int = 5
    num_limited_errands: int = 3
@dataclass
class CustomResult:
    pass

class ErrandState(StrEnum):
    DEFAULT = auto()
    OUT_NOW = auto()
    DONE = auto()
    UNKNOWN = auto()
class ErrandType(StrEnum):
    DAILY = auto()
    LIMITED = auto()
    UNKNOWN = auto()
class ErrandReward(StrEnum):
    SC = auto() # Sealed Crystal
    GC = auto() # God Crystal
    SPIRIT_P = auto() # Spirit Power
    TILES = auto()
    BOOKS = auto()
    INCENSE_WOOD = auto()
    OTHERS = auto()
    UNKNOWN = auto()

@dataclass
class Errand:
    type: ErrandType = ErrandType.UNKNOWN        # DAILY, LIMITED
    position: int = 0
    state: ErrandState = ErrandState.UNKNOWN     # DEFAULT, OUT_NOW, DONE
    reward_type: ErrandReward = ErrandReward.UNKNOWN  # SC, GC, SPIRIT_P, TILES, BOOKS, INCENSE_WOOD, OTHERS
    reward_count: int = 0
    time_expire: Optional[timedelta] = None      # only for Limited Errands
    time_cost: Optional[timedelta] = None
    datetime_reco: Optional[datetime] = None
    datetime_expire: Optional[datetime] = None      # Time when the errand is expired
    datetime_complete: Optional[datetime] = None
    pass

@maafw.resource.custom_recognition("ErrandRecoTest1")
class ErrandRecognition1(CustomRecognition):
    '''
    ErrandRecognition1
        After images are captured, Parse and Analyze errands one by one
        For develop purpose only, not for production
        Reads from files as captured images
    '''

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        enter_time = datetime.now()
        today_end_time = datetime.combine(enter_time, time.max)
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        dims = Dimensions(**{k: v for k, v in json.loads(argv.custom_recognition_param).items() if k in (f.name for f in fields(Dimensions))})
        # Read Images
        from ..image import load_imagefile_as_cvmat
        images = tuple(load_imagefile_as_cvmat(f"./assets/cache/debug/errand/forge/01-{i}.png") for i in range(4))
        reco_times = tuple(datetime.now() for i in range(4)) # forge it for now
        # Assume 3 errands, could be 4,5,6 in practice
        count_limited_errands = 5
        count_daily_errands = 5
        # Done init

        # If no more than 3 limited errands, let's find the actual number
        if count_limited_errands <= 3:
            roi_offset = dims.offset_grow_one_down + dims.offset_grow_one_down
            reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Limited_Errand_At_Slot_1", images[2], 
                                                  {"Errand_Base_Flag_Seen_Limited_Errand_At_Slot_1": {"roi_offset": roi_offset.roi}})
            count_limited_errands = 0 if reco_detail is None else len(reco_detail.filterd_results)
        logger.debug("Number of Limited Errands: %d", count_limited_errands)
        # Parse Limited Errands. 
        limited_errands = tuple()
        if count_limited_errands > 0:
            # 3rd image
            num_errands = 3 if count_limited_errands > 3 else count_limited_errands
            roi_offset = sum((dims.offset_grow_one_down,) * (num_errands - 1), Rect()) 
            reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1", images[2], 
                                                {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1": {"roi_offset": roi_offset.roi}})
            reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[2], 
                                                {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[2], 
                                                {"Errand_Base_Find_God_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[2],
                                                {"Errand_Base_Find_Times": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            for i in range(num_errands):
                errand = Errand(type=ErrandType.LIMITED, position= i + 1)
                current_box = sum((dims.offset_one_errand_down,) * i, dims.box_t_1st)
                current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
                current_box_time_expire = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_expire
                current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
                current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
                current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
                current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
                current_time_expire_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_expire)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_expire = str(current_time_expire_tp[0]) if len(current_time_expire_tp) == 1 else None
                errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
                errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
                errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
                errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
                errand.time_expire = datetime.strptime(regex_time.search(current_time_expire).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_expire is not None else None
                errand.datetime_reco = reco_times[2]
                errand.datetime_expire = errand.datetime_reco + errand.time_expire if errand.time_expire is not None else None
                errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
                #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
                # TODO : Validate errand?
                limited_errands = limited_errands + (errand,)
        if count_limited_errands in range(4,7):
            # 4th image
            num_errands = count_limited_errands - 3
            roi_offset = sum((dims.offset_grow_one_up,) * (num_errands - 1), Rect())
            reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1", images[3], 
                                                {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1": {"roi_offset": roi_offset.roi}})
            reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[3], 
                                                {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[3], 
                                                {"Errand_Base_Find_God_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[3],
                                                {"Errand_Base_Find_Times": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            for i in range(num_errands):
                errand = Errand(type=ErrandType.LIMITED, position= i + 3 + 1)
                current_box = sum((dims.offset_one_errand_up,) * (num_errands - i - 1), dims.box_b_1st)
                current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
                current_box_time_expire = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_expire
                current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
                current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
                current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
                current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
                current_time_expire_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_expire)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_expire = str(current_time_expire_tp[0]) if len(current_time_expire_tp) == 1 else None
                errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
                errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
                errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
                errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
                errand.time_expire = datetime.strptime(regex_time.search(current_time_expire).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_expire is not None else None
                errand.datetime_reco = reco_times[3]
                errand.datetime_expire = errand.datetime_reco + errand.time_expire if errand.time_expire is not None else None
                errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
                #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
                # TODO : Validate errand?
                limited_errands = limited_errands + (errand,)
        daily_errands = tuple()
        # 1st image
        num_errands = 3
        roi_offset = sum((dims.offset_grow_one_down,) * (num_errands - 1), Rect()) 
        reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1", images[0], 
                                            {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1": {"roi_offset": roi_offset.roi}})
        reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[0], 
                                            {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[0], 
                                            {"Errand_Base_Find_God_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[0],
                                            {"Errand_Base_Find_Times": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        for i in range(num_errands):
            errand = Errand(type=ErrandType.DAILY, position= i + 1)
            current_box = sum((dims.offset_one_errand_down,) * i, dims.box_t_1st)
            current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
            current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
            current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
            current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
            current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
            current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
            errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
            errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
            errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
            errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
            errand.time_expire = None
            errand.datetime_reco = reco_times[0]
            errand.datetime_expire = today_end_time
            errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
            #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
            # TODO : Validate errand?
            daily_errands = daily_errands + (errand,)
        # 2nd image
        num_errands = count_daily_errands - 3
        roi_offset = sum((dims.offset_grow_one_up,) * (num_errands - 1), Rect()) 
        reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1", images[1], 
                                            {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1": {"roi_offset": roi_offset.roi}})
        reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[1], 
                                            {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[1], 
                                            {"Errand_Base_Find_God_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[1],
                                            {"Errand_Base_Find_Times": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        for i in range(num_errands):
            errand = Errand(type=ErrandType.DAILY, position= i + 3 + 1)
            current_box = sum((dims.offset_one_errand_up,) * (num_errands - i - 1), dims.box_b_1st)
            current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
            current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
            current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
            current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
            current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
            current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
            errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
            errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
            errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
            errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
            errand.time_expire = None
            errand.datetime_reco = reco_times[0]
            errand.datetime_expire = today_end_time
            errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
            #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
            # TODO : Validate errand?
            daily_errands = daily_errands + (errand,)
        
        print(daily_errands)
        print(limited_errands)
        dumped = jsons.dumps((daily_errands, limited_errands))
        pass



        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail=dumped)
        

@maafw.resource.custom_recognition("ErrandReco")
class ErrandRecognition(CustomRecognition):
    '''
    ErrandRecognition
        Start from being at Errand Page, Daily or Limited
        Reads errands one by one, record each errand in AnalyzeResult
    '''
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        enter_time = datetime.now()
        today_end_time = datetime.combine(enter_time, time.max)
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        dims = Dimensions(**{k: v for k, v in json.loads(argv.custom_recognition_param).items() if k in (f.name for f in fields(Dimensions))})
        images, reco_times = (), ()
        # Get 1st Image
        img = context.tasker.controller.post_screencap().wait().get()
        images = images + (img,); reco_times = reco_times + (datetime.now(),)
        # check if at Errand Page, Daily Tab, Top Position
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Errand_Page_0", img)
        if reco_detail is None: logger.debug("Not at Errand Page with 0 Finished Errands, Stop Recognition"); return failed_result
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Daily_Tab", img)
        if reco_detail is None: logger.debug("Not at Daily Tab"); return failed_result
        reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Scroll_Bar_Top_5", img) # Assume Daily Tab always have 5 Errands
        if reco_detail is None: logger.debug("Not at Top Position"); return failed_result
        logger.debug("Got 1st image. Time Elapsed %3f seconds",(datetime.now() - enter_time).total_seconds())
        # Scroll Down and Get 2nd Image
        delta_y = dims.offset_t4_2_b1.y + dims.offset_one_errand_up.y
        action_result = context.run_action("Errand_Base_Run_VerticalSwipe", dims.box_t_4th + dims.offset_click, "", 
                                           {"Errand_Base_Run_VerticalSwipe":{"custom_action_param": {"delta_y": delta_y}}})
        if action_result is None: logger.debug("Failed to Scroll Down"); return failed_result
        img = context.tasker.controller.post_screencap().wait().get()
        images = images + (img,); reco_times = reco_times + (datetime.now(),)
        reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Scroll_Bar_Bottom_68px", img)
        if reco_detail is None: logger.debug("Not at Bottom Position"); return failed_result
        logger.debug("Got 2nd image. Time Elapsed %3f seconds",(datetime.now() - enter_time).total_seconds())
        # Scroll Up to Top
        delta_y = dims.offset_b4_2_t1.y + dims.offset_one_errand_down.y
        action_result = context.run_action("Errand_Base_Run_VerticalSwipe", dims.box_b_4th + dims.offset_click, "", 
                                           {"Errand_Base_Run_VerticalSwipe":{"custom_action_param": {"delta_y": delta_y}}})
        if action_result is None: logger.debug("Failed to Scroll Up"); return failed_result
        # Go to Limited Tab
        action_result = context.run_action("Errand_Base_Tap_Limited_Tab")
        if action_result is None: logger.debug("Failed to Tap Limited Tab"); return failed_result
        # Get 3rd Image
        sleep(1.0)
        img = context.tasker.controller.post_screencap().wait().get()
        images = images + (img,); reco_times = reco_times + (datetime.now(),)
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Errand_Page_0", img)
        if reco_detail is None: logger.debug("Got Finished Errand, Stop Recognition"); return failed_result
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Limited_Tab", img)
        if reco_detail is None: logger.debug("Not at Limited Tab"); return failed_result
        logger.debug("Got 3rd image. Time Elapsed %3f seconds",(datetime.now() - enter_time).total_seconds())
        # Check if necessary to Scroll Down to Bottom
        count_daily_errands = 5
        count_limited_errands = 0
        reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Scroll_Bar_Top_456", img)
        if reco_detail is None: logger.debug("No Need to Scroll Down at Limited Tab"); count_limited_errands = 3
        else:
            for i in range(4, 7):
                reco_detail = context.run_recognition(f"Errand_Base_Flag_Seen_Scroll_Bar_Top_{i}", img)
                if reco_detail is not None: count_limited_errands = i; break
            if count_limited_errands not in range(4, 7): logger.debug("Failed to Count Limited Errands"); return failed_result
            else: logger.debug("Found %d Limited Errands", count_limited_errands)
            # Scroll Down to Bottom
            delta_y = dims.offset_t4_2_b1.y + dims.offset_one_errand_up.y * (count_limited_errands - 4)
            action_result = context.run_action("Errand_Base_Run_VerticalSwipe", dims.box_t_4th + dims.offset_click, "", 
                                            {"Errand_Base_Run_VerticalSwipe":{"custom_action_param": {"delta_y": delta_y}}})
            if action_result is None: logger.debug("Failed to Scroll Down"); return failed_result
            img = context.tasker.controller.post_screencap().wait().get()
            images = images + (img,); reco_times = reco_times + (datetime.now(),)
            reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Scroll_Bar_Bottom_68px", img)
            if reco_detail is None: logger.debug("Not at Bottom Position"); return failed_result
            reco_detail = context.run_recognition("Errand_Base_Flag_At_Errand_Page_0", img)
            if reco_detail is None: logger.debug("Got Finished Errand, Stop Recognition"); return failed_result
            logger.debug("Got 4th image. Time Elapsed %3f seconds",(datetime.now() - enter_time).total_seconds())
            # Scroll Up to Top
            delta_y = dims.offset_b4_2_t1.y + dims.offset_one_errand_down.y * (count_limited_errands - 4)
            action_result = context.run_action("Errand_Base_Run_VerticalSwipe", dims.box_b_4th + dims.offset_click, "", 
                                            {"Errand_Base_Run_VerticalSwipe":{"custom_action_param": {"delta_y": delta_y}}})
            if action_result is None: logger.debug("Failed to Scroll Up"); return failed_result
        logger.debug("Got %d images. Time Elapsed %3f seconds", len(images),(datetime.now() - enter_time).total_seconds())
        # For Debug Save the Images
        from ..image import save_cvmat_as_imagefile
        for i, img in enumerate(images):
            save_cvmat_as_imagefile(img, img_save_path, str(i))

        # If no more than 3 limited errands, let's find the actual number
        if count_limited_errands <= 3:
            roi_offset = dims.offset_grow_one_down + dims.offset_grow_one_down
            reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Limited_Errand_At_Slot_1", images[2], 
                                                  {"Errand_Base_Flag_Seen_Limited_Errand_At_Slot_1": {"roi_offset": roi_offset.roi}})
            count_limited_errands = 0 if reco_detail is None else len(reco_detail.filterd_results)
        logger.debug("Number of Limited Errands: %d", count_limited_errands)
        # Parse Limited Errands. 
        limited_errands = tuple()
        if count_limited_errands > 0:
            # 3rd image
            num_errands = 3 if count_limited_errands > 3 else count_limited_errands
            roi_offset = sum((dims.offset_grow_one_down,) * (num_errands - 1), Rect()) 
            reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1", images[2], 
                                                {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1": {"roi_offset": roi_offset.roi}})
            reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[2], 
                                                {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[2], 
                                                {"Errand_Base_Find_God_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[2],
                                                {"Errand_Base_Find_Times": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
            for i in range(num_errands):
                errand = Errand(type=ErrandType.LIMITED, position= i + 1)
                current_box = sum((dims.offset_one_errand_down,) * i, dims.box_t_1st)
                current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
                current_box_time_expire = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_expire
                current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
                current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
                current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
                current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
                current_time_expire_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_expire)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_expire = str(current_time_expire_tp[0]) if len(current_time_expire_tp) == 1 else None
                errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
                errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
                errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
                errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
                errand.time_expire = datetime.strptime(regex_time.search(current_time_expire).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_expire is not None else None
                errand.datetime_reco = reco_times[2]
                errand.datetime_expire = errand.datetime_reco + errand.time_expire if errand.time_expire is not None else None
                errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
                #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
                # TODO : Validate errand?
                limited_errands = limited_errands + (errand,)
        if count_limited_errands in range(4,7):
            # 4th image
            num_errands = count_limited_errands - 3
            roi_offset = sum((dims.offset_grow_one_up,) * (num_errands - 1), Rect())
            reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1", images[3], 
                                                {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1": {"roi_offset": roi_offset.roi}})
            reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[3], 
                                                {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[3], 
                                                {"Errand_Base_Find_God_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[3],
                                                {"Errand_Base_Find_Times": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
            for i in range(num_errands):
                errand = Errand(type=ErrandType.LIMITED, position= i + 3 + 1)
                current_box = sum((dims.offset_one_errand_up,) * (num_errands - i - 1), dims.box_b_1st)
                current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
                current_box_time_expire = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_expire
                current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
                current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
                current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
                current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
                current_time_expire_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_expire)(Rect(*r.box))) if reco_detail_times is not None else tuple()
                current_time_expire = str(current_time_expire_tp[0]) if len(current_time_expire_tp) == 1 else None
                errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
                errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
                errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
                errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
                errand.time_expire = datetime.strptime(regex_time.search(current_time_expire).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_expire is not None else None
                errand.datetime_reco = reco_times[3]
                errand.datetime_expire = errand.datetime_reco + errand.time_expire if errand.time_expire is not None else None
                errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
                #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
                # TODO : Validate errand?
                limited_errands = limited_errands + (errand,)
        daily_errands = tuple()
        # 1st image
        num_errands = 3
        roi_offset = sum((dims.offset_grow_one_down,) * (num_errands - 1), Rect()) 
        reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1", images[0], 
                                            {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_1": {"roi_offset": roi_offset.roi}})
        reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[0], 
                                            {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[0], 
                                            {"Errand_Base_Find_God_Crystal": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[0],
                                            {"Errand_Base_Find_Times": {"roi": dims.box_t_1st.roi, "roi_offset": roi_offset.roi}})
        for i in range(num_errands):
            errand = Errand(type=ErrandType.DAILY, position= i + 1)
            current_box = sum((dims.offset_one_errand_down,) * i, dims.box_t_1st)
            current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
            current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
            current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
            current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
            current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
            current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
            errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
            errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
            errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
            errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
            errand.time_expire = None
            errand.datetime_reco = reco_times[0]
            errand.datetime_expire = today_end_time
            errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
            #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
            # TODO : Validate errand?
            daily_errands = daily_errands + (errand,)
        # 2nd image
        num_errands = count_daily_errands - 3
        roi_offset = sum((dims.offset_grow_one_up,) * (num_errands - 1), Rect()) 
        reco_detail_out_now = context.run_recognition("Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1", images[1], 
                                            {"Errand_Base_Flag_Seen_In_Progress_Mark_At_Slot_-1": {"roi_offset": roi_offset.roi}})
        reco_detail_sealed_crystal = context.run_recognition("Errand_Base_Find_Sealed_Crystal", images[1], 
                                            {"Errand_Base_Find_Sealed_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_god_crystal = context.run_recognition("Errand_Base_Find_God_Crystal", images[1], 
                                            {"Errand_Base_Find_God_Crystal": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        reco_detail_times = context.run_recognition("Errand_Base_Find_Times", images[1],
                                            {"Errand_Base_Find_Times": {"roi": dims.box_b_1st.roi, "roi_offset": roi_offset.roi}})
        for i in range(num_errands):
            errand = Errand(type=ErrandType.DAILY, position= i + 3 + 1)
            current_box = sum((dims.offset_one_errand_up,) * (num_errands - i - 1), dims.box_b_1st)
            current_box_time_cost = current_box + dims.relative_box_negative_whole_errand + dims.relative_box_time_cost
            current_out_now = tuple(r for r in reco_detail_out_now.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_out_now is not None else tuple()
            current_sealed_crystal = tuple(r for r in reco_detail_sealed_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_sealed_crystal is not None else tuple()
            current_god_crystal = tuple(r for r in reco_detail_god_crystal.filterd_results if is_in_rect(current_box)(Rect(*r.box))) if reco_detail_god_crystal is not None else tuple()
            current_time_cost_tp = tuple(r.text for r in reco_detail_times.filterd_results if is_in_rect(current_box_time_cost)(Rect(*r.box))) if reco_detail_times is not None else tuple()
            current_time_cost = str(current_time_cost_tp[0]) if len(current_time_cost_tp) == 1 else None
            errand.state = ErrandState.OUT_NOW if any(current_out_now) else ErrandState.DEFAULT
            errand.reward_type = ErrandReward.SC if any(current_sealed_crystal) else ErrandReward.GC if any(current_god_crystal) else ErrandReward.OTHERS
            errand.reward_count = len(current_sealed_crystal) if errand.reward_type == ErrandReward.SC else len(current_god_crystal) if errand.reward_type == ErrandReward.GC else 0
            errand.time_cost = datetime.strptime(regex_time.search(current_time_cost).group(), "%H:%M:%S") - datetime.strptime("0", "%S") if current_time_cost is not None else None
            errand.time_expire = None
            errand.datetime_reco = reco_times[0]
            errand.datetime_expire = today_end_time
            errand.datetime_complete = errand.datetime_reco + errand.time_cost if errand.state is ErrandState.OUT_NOW and errand.time_cost is not None else None
            #print(current_out_now, current_sealed_crystal, current_god_crystal, current_times)
            # TODO : Validate errand?
            daily_errands = daily_errands + (errand,)
        logger.debug("Successfully parsed %d Daily Errands and %d Limited Errands. Time Elapsed %3f seconds.", len(daily_errands), len(limited_errands), (datetime.now() - enter_time).total_seconds())
        dumped = jsons.dumps((daily_errands, limited_errands))
        
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail=dumped)

