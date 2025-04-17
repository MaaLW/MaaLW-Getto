from enum import StrEnum, auto
from dataclasses import dataclass, field, fields
from time import sleep
import json, re

import jsons

from ..maafw import Rect, Context, CustomRecognition
from ..maafw.custom import custom_registry
from ..logger import logger
from ..datetime import datetime, time, timedelta
from .define import is_in_rect

img_save_path = "./assets/cache/debug/getto/"
regex_player_level = re.compile(r'^等级([1-9]\d*)$')
regex_number = re.compile(r"^[1-9]\d*$")

@dataclass(frozen=True)
class DimensionsHome:
    box_player: Rect = field(default_factory=lambda: Rect(0, 0, 450, 120)) # top left box of player info.
    box_sp: Rect = field(default_factory=lambda: Rect(640, 0, 180, 60))
    box_sc: Rect = field(default_factory=lambda: Rect(1060, 0, 120, 60))
    pass

@custom_registry.custom_recognition("GettoScrapeHomeV1")
class GettoScrapeHomeV1(CustomRecognition):
    def analyze(self, context, argv):
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        dims = DimensionsHome(**{k: v for k, v in json.loads(argv.custom_recognition_param).items() if k in (f.name for f in fields(DimensionsHome))})
        new_context = context.clone()
        reco_detail_player = new_context.run_recognition("Home_Scrape_Base_OCR", argv.image, 
                                                         {"Home_Scrape_Base_OCR": {"roi": dims.box_player.roi, 
                                                                                   "expected": regex_player_level.pattern, 
                                                                                   "order_by": "Vertical"}})
        reco_detail_sp = new_context.run_recognition("Home_Scrape_Base_OCR", argv.image, 
                                                     {"Home_Scrape_Base_OCR": {"roi": dims.box_sp.roi, 
                                                                                   "expected": regex_number.pattern, 
                                                                                   "order_by": "Vertical"}})
        reco_detail_sc = new_context.run_recognition("Home_Scrape_Base_OCR", argv.image, 
                                                     {"Home_Scrape_Base_OCR": {"roi": dims.box_sc.roi, 
                                                                                   "expected": regex_number.pattern, 
                                                                                   "order_by": "Vertical"}})
        result = dict[str, int]()
        text_player_level = reco_detail_player.filterd_results[0].text if reco_detail_player is not None and len(reco_detail_player.filterd_results) == 1 else None
        player_level = int(regex_player_level.search(text_player_level).group(1)) if isinstance(text_player_level, str) else None
        if player_level is not None: 
            result["player_level"] = player_level
        text_sp = reco_detail_sp.filterd_results[1].text if reco_detail_sp is not None and len(reco_detail_sp.filterd_results) == 2 else None
        text_sp_max = reco_detail_sp.filterd_results[0].text if reco_detail_sp is not None and len(reco_detail_sp.filterd_results) == 2 else None
        sp = int(regex_number.search(text_sp).group(0)) if isinstance(text_sp, str) else None
        sp_max = int(regex_number.search(text_sp_max).group(0)) if isinstance(text_sp_max, str) else None
        if sp is not None and sp_max is not None:
            result["sp"] = sp
            result["sp_max"] = sp_max
        text_sc = reco_detail_sc.filterd_results[0].text if reco_detail_sc is not None and len(reco_detail_sc.filterd_results) == 1 else None
        sc_quantity = int(regex_number.search(text_sc).group(0)) if isinstance(text_sc, str) else None
        if sc_quantity is not None:
            result["sc_quantity"] = sc_quantity
        logger.debug("Got result %s. \nTime elapsed %3f seconds", result, (datetime.now() - enter_time).total_seconds())
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail=json.dumps(result))