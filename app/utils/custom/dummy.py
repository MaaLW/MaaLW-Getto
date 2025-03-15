from maa.define import Rect
from maa.context import Context
from maa.custom_recognition import CustomRecognition
from ..maafw import maafw
@maafw.resource.custom_recognition("Reco2")
class Reco2(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        
        print("Reco2 is running!")
        #context.run_action("Temp001", Rect(230,627,980,93), "", {"Temp001":{"action": "Click"}})
        res = context.run_action("Temp001", Rect(230,627,980,93), "", {"Temp001":{"action": "Custom", 
                                                                            "target": [230,627,980,93],
                                                                            "custom_action": "VerticalSwipe", 
                                                                            "custom_action_param": {"delta_y": -300}}})
        print(res)
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Hello World!")
    
from maa.custom_action import CustomAction
@maafw.resource.custom_action("Act2")
class Act2(CustomAction):
    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> CustomAction.RunResult:
        print("Act2 is running!")
        point = argv.box.x+argv.box.w//2, argv.box.y+argv.box.h//2
        context.tasker.controller.post_click(*point).wait()
        return CustomAction.RunResult(True)