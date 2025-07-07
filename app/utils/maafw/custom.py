from . import CustomAction, CustomRecognition
from ..logger import logger
class Custom_Registry:
    def __init__(self):
        self.custom_action_holder = dict[str, CustomAction]()
        self.custom_recognition_holder = dict[str, CustomRecognition]()
    def custom_recognition(self, name: str):

        def wrapper_recognition(recognition):
            self.register_custom_recognition(name=name, recognition=recognition())
            return recognition
        
        return wrapper_recognition
    
    def register_custom_recognition(self, name: str, recognition: CustomRecognition):
        if name in self.custom_recognition_holder:
            logger.warning(f"Recognition {name} is already registered and is being overridden.")
        self.custom_recognition_holder[name] = recognition

    def custom_action(self, name: str):

        def wrapper_action(action):
            self.register_custom_action(name=name, action=action())
            return action

        return wrapper_action
    
    def register_custom_action(self, name: str, action: CustomAction):
        if name in self.custom_action_holder:
            logger.warning(f"Action {name} is already registered and is being overridden.")
        self.custom_action_holder[name] = action

custom_registry = Custom_Registry()
# To register custom actions and recognitions, import them in ../custom/__init__.py
# import so that they can be registered
from .. import custom