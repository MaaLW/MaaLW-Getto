# app/utils/emulator/generic.py
import subprocess
from ..datetime import sleep
from .define import Emulator

class GenericEmulator(Emulator):
    """Generic emulator class
    Uses adb only
    """
    def __init__(self, *, 
                 emulator_name: str,
                 adb_path: str,
                 adb_address: str,
                 default_app_package_name: str) -> None:
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
        try:
            result = subprocess.run(
                [self.adb_path, "connect", self.adb_address],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30
            )
            return "connected" in result.stdout.lower()
        except subprocess.SubprocessError:
            return False
    
    def stop(self, force: bool = False) -> bool:
        """Stop emulator using ADB"""
        try:
            # First try graceful disconnect
            subprocess.run(
                [self.adb_path, "disconnect", self.adb_address],
                timeout=15
            )
            
            if force:
                # If force is True, kill the ADB server
                subprocess.run(
                    [self.adb_path, "kill-server"],
                    timeout=15
                )
            return True
        except subprocess.SubprocessError:
            return False
    
    def restart(self) -> bool:
        """Restart emulator"""
        try:
            subprocess.run(
                [self.adb_path, "-s", self.adb_address, "reboot"], 
                timeout=120
            )
            return self.wait_until_ready()
        except subprocess.SubprocessError:
            return False
    
    def get_adb_connection(self) -> str:
        """Get ADB connection string"""
        return self.adb_address
    
    def is_running(self) -> bool:
        """Check if emulator is running and responsive"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", self.adb_address, "shell", "getprop", "sys.boot_completed"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10
            )
            return result.stdout.strip() == "1"
        except subprocess.SubprocessError:
            return False
    
    def is_app_running(self, package_name: str | None = None) -> bool:
        """Check if specific app is running"""
        if package_name is None:
            package_name = self.default_app_package_name
            
        try:
            result = subprocess.run(
                [self.adb_path, "-s", self.adb_address, "shell", "pidof", package_name],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10
            )
            return bool(result.stdout.strip())
        except subprocess.SubprocessError:
            return False
        
    def is_app_stopped(self, package_name: str | None = None) -> bool:
        return not self.is_app_running(package_name)
    
    def start_app(self, package_name: str | None = None) -> bool:
        """Start an application on the emulator"""
        if package_name is None:
            package_name = self.default_app_package_name
            
        try:
            result = subprocess.run(
                [self.adb_path, "-s", self.adb_address, "shell", "monkey", "-p", package_name, "1"],
                capture_output=True,
                timeout=15
            )
            return result.returncode == 0
        except subprocess.SubprocessError:
            return False
    
    def stop_app(self, package_name: str | None = None) -> bool:
        """Stop an application on the emulator"""
        if package_name is None:
            package_name = self.default_app_package_name
            
        try:
            result = subprocess.run(
                [self.adb_path, "-s", self.adb_address, "shell", "am", "force-stop", package_name],
                capture_output=True,
                timeout=15
            )
            return result.returncode == 0
        except subprocess.SubprocessError:
            return False
    
    def execute_shell_command(self, command: str) -> str | None:
        """Execute a shell command on the emulator"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", self.adb_address, "shell", command],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=15
            )
            return result.stdout.strip()
        except subprocess.SubprocessError:
            return None