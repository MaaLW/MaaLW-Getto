# app/utils/emulator/define.py
from abc import ABC, abstractmethod
from ..datetime import datetime, timedelta, sleep

class Emulator(ABC):
    """Abstract base class of emulator, defines common interface"""
    
    @abstractmethod
    def get_emulator_name(self) -> str:
        """Get emulator name"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Start emulator"""
        pass
    
    @abstractmethod
    def stop(self, force: bool = False) -> bool:
        """Stop emulator"""
        pass
    
    @abstractmethod
    def restart(self) -> bool:
        """Restart emulator"""
        pass
    
    @abstractmethod
    def get_adb_connection(self) -> str:
        """Get ADB connection info"""
        pass
    
    @abstractmethod
    def is_running(self) -> bool:
        """Check if emulator is running"""
        pass
    
    @abstractmethod
    def is_app_running(self, package_name: str | None = None) -> bool:
        """Check if app is running"""
        pass

    @abstractmethod
    def is_app_stopped(self, package_name: str | None = None) -> bool:
        """Check if app is stopped"""
        pass

    @abstractmethod
    def start_app(self, package_name: str | None = None) -> bool:
        """Start app"""
        pass

    @abstractmethod
    def stop_app(self, package_name: str | None = None) -> bool:
        """Stop app"""
        pass
    
    # Optional common method
    def is_ready(self) -> bool:
        """Check if emulator is ready"""
        return self.is_running()

    def wait_until_ready(self, timeout: int = 300) -> bool:
        """Wait until instance is ready"""
        start_time = datetime.now()
        while datetime.now() - start_time < timedelta(seconds=timeout):
            if self.is_running():
                return True
            sleep(5)
        return False

    def wait_until_app_ready(self, package_name: str | None = None, timeout: int = 30) -> bool:
        """Wait until app is ready"""
        start_time = datetime.now()
        while datetime.now() - start_time < timedelta(seconds=timeout):
            if self.is_app_running(package_name):
                return True
            sleep(1)
        return False
    
    def wait_until_app_stopped(self, package_name: str | None = None, timeout: int = 30) -> bool:
        """Wait until app is stopped"""
        start_time = datetime.now()
        while datetime.now() - start_time < timedelta(seconds=timeout):
            if self.is_app_stopped(package_name):
                return True
            sleep(1)
        return False