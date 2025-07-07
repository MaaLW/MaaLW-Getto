from .define import Emulator
from .generic import GenericEmulator
from .mumu import MuMu12Emulator
from .dummy import DummyEmulator

class EmulatorFactory:
    """Emulator factory class"""
    
    @staticmethod
    def create_emulator(emulator_type: str, **kwargs) -> Emulator:
        try:
            match emulator_type.casefold():
                case "mumu12":
                    return MuMu12Emulator(**kwargs)
                case "dummy":
                    return DummyEmulator(**kwargs)
                case _:
                    raise NotImplementedError(f"Emulator type {emulator_type} is not implemented.")
        except Exception as e:
            return GenericEmulator(**kwargs)