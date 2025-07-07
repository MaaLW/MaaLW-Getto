import json
from ..maafw import Rect, Context, CustomRecognition
from ..maafw.custom import custom_registry
from ..logger import logger
from ..datetime import datetime, time, timedelta

@custom_registry.custom_recognition("LostwordFindYarukiWarningDialog_v1")
class LostwordFindYarukiWarningDialog_v1(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("Entering %s", self)
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        rd_tm = context.run_recognition("Common_Yaruki_Warning_Handler_v1_Helper_Template_Match", argv.image)
        if rd_tm is None: return failed_result
        rd_ocr = context.run_recognition("Common_Yaruki_Warning_Handler_v1_Helper_OCR_01", argv.image)
        if rd_ocr is None: return failed_result
        rd_ocr = context.run_recognition("Common_Yaruki_Warning_Handler_v1_Helper_OCR_02", argv.image)
        if rd_ocr is None: return failed_result
        try:
            param = json.loads(argv.custom_recognition_param)
        except:
            param = {}
        find_button = param.get("find_button", "confirm")
        find_button_entry = "Common_Yaruki_Warning_Handler_v1_Helper_Confirm_Button" if find_button == "confirm" else "Common_Yaruki_Warning_Handler_v1_Helper_Cancel_Button"
        rd_find_btn = context.run_recognition(find_button_entry, argv.image)
        if rd_find_btn is None: return failed_result
        return CustomRecognition.AnalyzeResult(box=rd_find_btn.best_result.box, detail="")
    
@custom_registry.custom_recognition("LostwordFindGenericErrorDialog_v1")
class LostwordFindGenericErrorDialog_v1(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        logger.debug("Entering %s", self)
        enter_time = datetime.now()
        failed_result = CustomRecognition.AnalyzeResult(None, "")
        rd_caption = context.run_recognition("Common_Generic_Error_Dialog_Handler_v1_Helper_Seen_Caption", argv.image)
        if rd_caption is None: return failed_result
        rd_close = context.run_recognition("Common_Generic_Error_Dialog_Handler_v1_Helper_Seen_Close_Button", argv.image)
        if rd_close is None: return failed_result
        try:
            # save image
            from app.utils.image import save_cvmat_as_imagefile
            imgfile = save_cvmat_as_imagefile(argv.image, "./assets/cache/debug/getto/generic_error/")
            logger.error("%s Saved image to %s", self, imgfile)
        except Exception as e:
            logger.error("%s Failed to save image: %s", self, e)

        return CustomRecognition.AnalyzeResult(box=rd_close.best_result.box, detail=imgfile)