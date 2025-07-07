# 2025/4/30
# Now we can test custom recognitions which only uses one image
# To test custom recognitions which uses screencap(), one may require to override the custom controller's screencap to support it.

import json

from maa.define import RecognitionDetail

from app.utils.datetime import datetime
from app.utils.logger import logger
from app.utils.maafw import Context, CustomRecognition, TaskDetail, Rect
from .misc import test_maafw as maafw

testbench_name = "MyTestBenchCustomRecognition_20250428"

class RecoResults:
    def __init__(self) -> None:
        self.reco_results : dict[int, RecognitionDetail | None] = {}
    def reset(self,key: int = 0):
        self.set(key, None)
        return
    def get(self, key: int = 0) -> RecognitionDetail | None:
        return self.reco_results.get(key)
    def set(self, key: int = 0, result: RecognitionDetail | None = None):
        self.reco_results[key] = result
        return

reco_results = RecoResults()

def test_yaruki_warning():
    if maafw.tasker is None or not maafw.tasker.inited: 
        assert maafw.controller is not None
        assert maafw.bind_tasker()
    key = 2
    reco_results.reset(key)
    entry_node_name = "TestEntry_20250428"
    runner_node_name = "TestRunner_20250428"
    entry_node_timeout = 10
    test_img = "tests/imgs/Yaruki_Warning.png"
    test_reco = "LostwordFindYarukiWarningDialog_v1"
    entry_ppl = {entry_node_name: {"recognition": "DirectHit", "action": "DoNothing", "next": [runner_node_name], "timeout": entry_node_timeout*1000}}
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.succeeded
    reco_result = reco_results.get(key)
    assert isinstance(reco_result, RecognitionDetail)
    assert reco_result.best_result.box == [700, 480, 160, 50]

    # Test cancel
    reco_results.reset(key)
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key, "custom_recognition_param": {"find_button": "cancel"}}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.succeeded
    reco_result = reco_results.get(key)
    assert isinstance(reco_result, RecognitionDetail)
    assert reco_result.best_result.box == [420, 480, 160, 50]
    # Test with other image
    reco_results.reset(key)
    test_img = "tests/imgs/Network_Timeout-202410.png"
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.done
    reco_result = reco_results.get(key)
    assert reco_result is None
    return

def test_generic_error_dialog():
    if maafw.tasker is None or not maafw.tasker.inited: 
        assert maafw.controller is not None
        assert maafw.bind_tasker()
    key = 1
    reco_results.reset(key)
    entry_node_name = "TestEntry_20250428"
    runner_node_name = "TestRunner_20250428"
    entry_node_timeout = 10
    test_img = "tests/imgs/Network_Error-20250430.png"
    test_reco = "LostwordFindGenericErrorDialog_v1"
    entry_ppl = {entry_node_name: {"recognition": "DirectHit", "action": "DoNothing", "next": [runner_node_name], "timeout": entry_node_timeout*1000}}
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.succeeded
    reco_result = reco_results.get(key)
    assert isinstance(reco_result, RecognitionDetail)
    assert reco_result.best_result.box == [400, 470, 480, 80]

    # Change image
    reco_results.reset(key)
    test_img = "tests/imgs/Network_Timeout-202410.png"
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.done
    reco_result = reco_results.get(key)
    assert reco_result is None

    # Change image to maintainance
    reco_results.reset(key)
    test_img = "tests/imgs/Maintainance-20250303.png"
    runner_ppl = {runner_node_name: {"recognition": "custom", "custom_recognition": testbench_name, 
                                     "custom_recognition_param": {"image": test_img, "custom_recognition": test_reco, "key": key}}}
    ppl = entry_ppl | runner_ppl
    b, td = maafw.run_ppl(entry=entry_node_name, pipeline_override=ppl)
    assert b
    assert isinstance(td, TaskDetail)
    assert td.status.done
    reco_result = reco_results.get(key)
    assert reco_result.best_result.box[2:4] == [480, 80]


@maafw.custom_recognition(testbench_name)
class MyTestBenchCustomRecognition_20250428(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        params = dict(json.loads(argv.custom_recognition_param))
        new_context = context.clone()
        from app.utils.image import load_imagefile_as_cvmat
        image = load_imagefile_as_cvmat(params.get("image"))
        # Done init
        time1 = datetime.now()
        entry = testbench_name + "_Temp"
        reco_detail = new_context.run_recognition(entry, image, 
                                                  {entry: {"recognition": "custom", 
                                                            "custom_recognition": params.get("custom_recognition"), 
                                                            "custom_recognition_param": params.get("custom_recognition_param", {}),
                                                            "roi": params.get("roi", [0]*4)}})
        logger.debug("%s Got result %s. \nTime elapsed %3f seconds", self, reco_detail, (datetime.now() - time1).total_seconds())
        key = params.get("key", 0)
        reco_results.set(key, reco_detail)
        return CustomRecognition.AnalyzeResult(box=(0, 0, 100, 100), detail="Done!")