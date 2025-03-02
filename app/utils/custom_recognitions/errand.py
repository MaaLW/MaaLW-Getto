from dataclasses import dataclass
import json

from maa.context import Context
from maa.custom_recognition import CustomRecognition

from ..maafw import maafw


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
        custom_param = self.CustomParam(**json.loads(argv.custom_action_param))
        # check if at Errand Page

        # Recognize 1st errand

        # Recognize 2nd errand

        # Recognize 3rd errand

        # if exist, Scroll Down and Recognize 4th errand
        
        # if exist, Scroll Down and Recognize 5th errand
        
        # if exist, Scroll Down and Recognize 6th errand 





        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Hello World!")
        