from dataclasses import dataclass, fields
from time import time, sleep
import json

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from ..maafw import maafw
from ..logger import logger


@maafw.resource.custom_recognition("ErrandReco")
class ErrandRecognition(CustomRecognition):
    '''
    ErrandRecognition
        Start from being at Errand Page, Daily or Temperorary
        Reads errands one by one, record each errand in AnalyzeResult
    '''
    @dataclass
    class CustomParam:
        pass
    @dataclass
    class CustomResult:
        pass
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        enter_time = time()

        custom_param = self.CustomParam(**{k: v for k, v in json.loads(argv.custom_recognition_param).items() if k in (f.name for f in fields(self.CustomParam))})
        # check if at Errand Page, Daily Tab, Top Position
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Errand_Page_0", argv.image)
        if reco_detail is None: logger.debug("Not at Errand Page 0 State"); return CustomRecognition.AnalyzeResult(None, "")
        reco_detail = context.run_recognition("Errand_Base_Flag_At_Daily_Tab", argv.image)
        if reco_detail is None: logger.debug("Not at Daily Tab"); return CustomRecognition.AnalyzeResult(None, "")
        reco_detail = context.run_recognition("Errand_Base_Flag_Seen_Scroll_Bar_Top_5", argv.image) # Assume Daily Tab always have 5 Errands
        if reco_detail is None: logger.debug("Not at Top Position"); return CustomRecognition.AnalyzeResult(None, "")
        print(time() - enter_time)
        images = (argv.image,)

        # Scroll Down and Get 2nd Image
        context.run_action()
        img = context.tasker.controller.post_screencap().wait().get()


        # Scroll Up to Top
        # Go to Temp Tab
        # Get 3rd Image
        # Check if necessary to Scroll Down to Bottom

        # Recognize 1st errand

        # Recognize 2nd errand

        # Recognize 3rd errand




        print("ErrandRecognition is running!")
        #return CustomRecognition.AnalyzeResult(None, "")
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Hello World!")
        