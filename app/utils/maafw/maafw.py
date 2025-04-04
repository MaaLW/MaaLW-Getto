
from . import (Resource, JobWithResult,
               AdbDevice, 
               AdbController, Tasker)
from ..datetime import timedelta, sleep, datetime

class MaaFW:
    def __init__(self):
        self.resource = Resource()
        self.controller = None
        self.tasker = None
        self.notification_handler = None
        self.user_path = "./assets/cache"
        self.resource_path = "./assets/resource/base"
        self.register_custom()
        pass

    def register_custom(self):
        from .custom import custom_registry
        for name, recognition in custom_registry.custom_recognition_holder.items():
            self.resource.register_custom_recognition(name=name, recognition=recognition)
        for name, action in custom_registry.custom_action_holder.items():
            self.resource.register_custom_action(name=name, action=action)
    
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

    def custom_recognition(self, name: str):
        self_deco = self.resource.custom_recognition(name)
        return self_deco

    def custom_action(self, name: str):
        self_deco = self.resource.custom_action(name)
        return self_deco
    
    def run_ppl(self, entry: str, pipeline_override: dict = {}, timeout: int = 10) -> tuple[bool, JobWithResult | None]:
        time_start = datetime.now()
        job = self.tasker.post_task(entry, pipeline_override)
        while (datetime.now() - time_start) < timedelta(seconds=timeout):
            if job.done:
                return True, job.get()
            # TODO consider shorten sleep time to enhance performance
            sleep(0.01)
        self.tasker.post_stop()
        return False, job.get()
    
    def dummy_run_ppl(self, *args, **kwargs) -> tuple[bool, JobWithResult | None]:
        return (False, None)

maafw = MaaFW()