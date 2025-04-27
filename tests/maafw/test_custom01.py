
from .misc import test_maafw as maafw


def test_yaruki_warning():
    if maafw.tasker is None or not maafw.tasker.inited: 
        assert maafw.controller is not None
        assert maafw.bind_tasker()
    pass




# coding:utf-8
# Consider adapt this to tests 2025/4/17
from dataclasses import asdict
from pathlib import Path
import json
from time import sleep, time
from dataclasses import dataclass
from random import randint, random
from logging import NOTSET, DEBUG

from code import interact

from app.utils.datetime import datetime
from app.utils.logger import logger
from app.utils.maafw import Context, CustomRecognition, CustomAction, Toolkit, AdbDevice
from app.config import config


def main():
    

    job = maafw.tasker.post_task("1",{"1": {"recognition": "custom", "custom_recognition": "MyTestBenchCustomRecognition", 
                                            "custom_recognition_param": {"image": "MuMu12-20250415-230237", 
                                                 "custom_recognition": "GettoScrapeHome_v1"}
                                    }}
                                ).wait().get()
    print(job)
    return


@maafw.custom_recognition("MyTestBenchCustomRecognition")
class MyTestBenchCustomRecognition(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        try: params = dict(json.loads(argv.custom_recognition_param))
        except: return failed_result
        new_context = context.clone()
        from app.utils.image import load_imagefile_as_cvmat
        image = load_imagefile_as_cvmat(f"./assets/cache/debug/forge/{params.get("image")}.png")
        # Done init
        time1 = datetime.now()
        reco_detail = new_context.run_recognition("TestBenchCustomRecognition_Temp", image, 
                                                  {"TestBenchCustomRecognition_Temp": {"recognition": "custom", 
                                                                                       "custom_recognition": params.get("custom_recognition"), 
                                                                                       "roi": params.get("roi", [0]*4)}})
        logger.debug("Got result %s. \nTime elapsed %3f seconds", reco_detail, (datetime.now() - time1).total_seconds())

        # Analyze

        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Hello World!")