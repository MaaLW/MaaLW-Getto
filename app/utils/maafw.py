



from maa.resource import Resource
from maa.toolkit import AdbDevice
from maa.controller import AdbController
from maa.tasker import Tasker


class MaaFW:
    def __init__(self):
        self.resource = Resource()
        self.controller = None
        self.tasker = None
        self.notification_handler = None
        self.user_path = "./assets/cache"
        self.resource_path = "./assets/resource/base"
        pass
    
    def load_resource(self, dir: str) -> bool:
        return self.resource.post_bundle(dir).wait().succeeded
    
    def connect_adb_device(self, adb_device: AdbDevice) -> bool:
        self.controller = AdbController(adb_path=adb_device.adb_path, 
                                        address=adb_device.address, 
                                        screencap_methods=adb_device.screencap_methods, 
                                        input_methods=adb_device.input_methods, 
                                        config=adb_device.config)
        return self.controller.post_connection().wait().succeeded

    def bind_tasker(self) -> bool:
        self.tasker = Tasker(notification_handler=self.notification_handler)
        self.tasker.bind(self.resource, self.controller)
        return self.tasker.inited

maafw = MaaFW()