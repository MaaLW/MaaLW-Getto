from ..maafw.custom import custom_registry
from ..maafw import Rect, Context, CustomRecognition, CustomAction

@custom_registry.custom_recognition("overridelab202504main")
class OverrideLab202504Main(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg) -> CustomRecognition.AnalyzeResult:
        new_context = context.clone()
        reco1 = context.run_recognition("OverrideLab202504Sub", argv.image)

        # override roi
        context.override_pipeline({"OverrideLab202504Sub": {"roi": [100, 100, 200, 300]}})
        reco2 = context.run_recognition("OverrideLab202504Sub", argv.image)
        
        # override custom param
        new_context.override_pipeline({"OverrideLab202504Sub": {"custom_recognition_param": {"value": "new value"}}})
        reco3 = new_context.run_recognition("OverrideLab202504Sub", argv.image)

        print(f"reco1 is {reco1.best_result.detail}")
        print(f"reco2 is {reco2.best_result.detail}")
        print(f"reco3 is {reco3.best_result.detail}")

        # action
        print("run action 1")
        context.run_action("OverrideLab202504Action")

        # override target
        context.override_pipeline({"OverrideLab202504Action": {"target": [100, 100, 200, 300]}})
        print("run action 2")
        context.run_action("OverrideLab202504Action")

        # override custom param
        print("run action 3")
        new_context.run_action("OverrideLab202504Action", pipeline_override={"OverrideLab202504Action": {"custom_action_param": {"value": "new value"}}})

        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Hello World!")
    
@custom_registry.custom_recognition("overridelab202504sub")
class OverrideLab202504Sub(CustomRecognition):
    def analyze(self, context: Context, argv: CustomRecognition.AnalyzeArg) -> CustomRecognition.AnalyzeResult:
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail=f"roi is {argv.roi}. custom_recognition_param is {argv.custom_recognition_param}")
    
@custom_registry.custom_action("overridelab202504action")
class OverrideLab202504Action(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> CustomAction.RunResult:
        print(f"OverrideLab202504Action: box is {argv.box}. custom_action_param is {argv.custom_action_param}")
        return CustomAction.RunResult(True)