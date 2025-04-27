import numpy
import json
from logging import DEBUG
from maa.controller import CustomController
from app.utils.maafw import NotificationHandler, Toolkit, CustomRecognition, Context
from app.utils.maafw.maafw import MaaFW
from app.utils.logger import logger
from app.utils.datetime import datetime

logger.setLevel(DEBUG)

class MyNotificationHandler(NotificationHandler):
    def on_raw_notification(self, msg: str, details: dict):
        print(
            f"on MyNotificationHandler.on_raw_notification, msg: {msg}, details: {details}"
        )

        super().on_raw_notification(msg, details)

class MyController(CustomController):

    def __init__(self, notification_handler: NotificationHandler):
        super().__init__(notification_handler=notification_handler)
        self.count = 0

    def connect(self) -> bool:
        print("on MyController.connect")
        self.count += 1
        return True

    def request_uuid(self) -> str:
        print("on MyController.request_uuid")
        # self.count += 1
        return "12345678"

    def start_app(self, intent: str) -> bool:
        print(f"on MyController.start_app, intent: {intent}")
        self.count += 1
        return True

    def stop_app(self, intent: str) -> bool:
        print(f"on MyController.stop_app, intent: {intent}")
        self.count += 1
        return True

    def screencap(self) -> numpy.ndarray:
        print("on MyController.screencap")
        self.count += 1
        return numpy.zeros((1080, 1920, 3), dtype=numpy.uint8)

    def click(self, x: int, y: int) -> bool:
        print(f"on MyController.click, x: {x}, y: {y}")
        self.count += 1
        return True

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int) -> bool:
        print(
            f"on MyController.swipe, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}, duration: {duration}"
        )
        self.count += 1
        return True

    def touch_down(
        self,
        contact: int,
        x: int,
        y: int,
        pressure: int,
    ) -> bool:
        print(
            f"on MyController.touch_down, contact: {contact}, x: {x}, y: {y}, pressure: {pressure}"
        )
        self.count += 1
        return True

    def touch_move(
        self,
        contact: int,
        x: int,
        y: int,
        pressure: int,
    ) -> bool:
        print(
            f"on MyController.touch_move, contact: {contact}, x: {x}, y: {y}, pressure: {pressure}"
        )
        self.count += 1
        return True

    def touch_up(self, contact: int) -> bool:
        print(f"on MyController.touch_up, contact: {contact}")
        self.count += 1
        return True

    def press_key(self, keycode: int) -> bool:
        print(f"on MyController.press_key, keycode: {keycode}")
        self.count += 1
        return True

    def input_text(self, text: str) -> bool:
        print(f"on MyController.input_text, text: {text}")
        self.count += 1
        return True
    
test_notification_handler = MyNotificationHandler()
test_controller = MyController(test_notification_handler)
test_maafw = MaaFW(notification_handler=test_notification_handler, controller=test_controller)
if not Toolkit.init_option(test_maafw.user_path):
    logger.error("Failed to init MaaToolkit.")
    raise RuntimeError("Failed to init MaaToolkit.")
if not test_maafw.load_resource(test_maafw.resource_path):
    logger.error("Failed to load resource.")
    raise RuntimeError("Failed to load resource.")
if not test_maafw.controller.post_connection().wait().succeeded:
    logger.error("Failed to post connection.")
    raise RuntimeError("Failed to post connection.")
if not test_maafw.bind_tasker():
    logger.error("Failed to init MaaFramework.")
    raise RuntimeError("Failed to init MaaFramework.")
