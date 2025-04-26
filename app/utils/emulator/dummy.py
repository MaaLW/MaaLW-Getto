# app/utils/emulator/dummy.py
from .define import Emulator

class DummyEmulator(Emulator):
    """Dummy emulator class.

    Does nothing.
    """
    def __init__(self, *, 
                 emulator_name: str = "Dummy",
                 adb_path: str = "adb",
                 adb_address: str = "dummy",
                 default_app_package_name: str = "dummy",
                 **kwargs
                 ) -> None:
        """
        Args:
            emulator_name: Name of the emulator
            adb_path: Path to adb executable
            adb_address: ADB connection string (e.g. "127.0.0.1:7555")
            default_app_package_name: Package name of the app to control
        """
        
        self.emulator_name = emulator_name
        self.adb_path = adb_path
        self.adb_address = adb_address
        self.default_app_package_name = default_app_package_name
    
    def get_emulator_name(self) -> str:
        return self.emulator_name
    
    def start(self) -> bool:
        """Start emulator using ADB"""
        return False
    
    def stop(self, force: bool = False) -> bool:
        """Stop emulator using ADB"""
        return False
    
    def restart(self) -> bool:
        """Restart emulator"""
        return False
    
    def get_adb_connection(self) -> str:
        """Get ADB connection string"""
        return self.adb_address
    
    def is_running(self) -> bool:
        """Check if emulator is running and responsive"""
        return False
    
    def is_app_running(self, package_name: str | None = None) -> bool:
        """Check if specific app is running"""
        return False
        
    def is_app_stopped(self, package_name: str | None = None) -> bool:
        return False
    
    def start_app(self, package_name: str | None = None) -> bool:
        """Start an application on the emulator"""
        return False
    
    def stop_app(self, package_name: str | None = None) -> bool:
        """Stop an application on the emulator"""
        return False
    
    def execute_shell_command(self, command: str) -> str | None:
        """Execute a shell command on the emulator"""
        return None