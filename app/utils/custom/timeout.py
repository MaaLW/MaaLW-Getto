from ..maafw import Rect, Context, CustomRecognition
from ..maafw.custom import custom_registry
from ..logger import logger
from ..datetime import datetime, time, timedelta

@custom_registry.custom_recognition("LostwordFindNetworkTimeoutDialog_v1")
class LostwordFindNetworkTimeoutDialog_v1(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("Entering %s", self)
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        rd_tm = context.run_recognition("Common_Network_Timeout_Handler_v1_Helper_Template_Match", argv.image)
        if rd_tm is None: return failed_result
        rd_ocr = context.run_recognition("Common_Network_Timeout_Handler_v1_Helper_OCR", argv.image)
        if rd_ocr is None: return failed_result
        rd_confirm_btn = context.run_recognition("Common_Network_Timeout_Handler_v1_Helper_Confirm_Button", argv.image)
        if rd_confirm_btn is None: return failed_result
        return CustomRecognition.AnalyzeResult(box=rd_confirm_btn.best_result.box, detail="")