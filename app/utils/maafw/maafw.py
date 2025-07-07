
from . import (Resource, 
               TaskDetail, 
               AdbDevice, 
               AdbController, Controller,
               NotificationHandler,
               Tasker, Job)
from ..datetime import timedelta, sleep, datetime

class MaaFW:
    def __init__(self, controller: Controller | None = None, notification_handler: NotificationHandler | None = None):
        self.resource = Resource()
        self.controller = controller
        self.tasker = None
        self.notification_handler = notification_handler
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
    
    def run_ppl(self, entry: str, pipeline_override: dict = {}, timeout: float = 10.0, 
                                  pre_wait_stopping_timeout: float = 2.0, 
                                  post_wait_stopping_timeout: float = 1.0
                                  ) -> tuple[bool, TaskDetail | None]:
        
        # Pre check
        time_start_pre = datetime.now()
        while self.tasker.stopping and (datetime.now() - time_start_pre) < timedelta(seconds=pre_wait_stopping_timeout):
            # Wait for the tasker to complete stopping
            sleep(0.01)
            continue
        if self.tasker.stopping:
            # Error: Tasker is still stopping
            #logger.error("Tasker is still stopping")
            return False, None
        
        time_start = datetime.now()
        job = self.tasker.post_task(entry, pipeline_override)
        while (datetime.now() - time_start) < timedelta(seconds=timeout):
            if job.done:
                return True, job.get()
            # TODO consider shorten sleep time to enhance performance
            sleep(0.01)
        self.tasker.post_stop()
        time_start_post = datetime.now()
        while self.tasker.stopping and (datetime.now() - time_start_post) < timedelta(seconds=post_wait_stopping_timeout):
            # Wait for the tasker to complete stopping
            sleep(0.01)
            continue
        if self.tasker.stopping:
            # Error: Tasker is still stopping
            # Best Effort. Cannot handle this better. Shouldn't happen
            pass
        return False, job.get()
    
    def dummy_run_ppl(self, *args, **kwargs) -> tuple[bool, TaskDetail | None]:
        return (False, None)
    
    def post_stop(self) -> Job:
        return self.tasker.post_stop()

maafw = MaaFW()