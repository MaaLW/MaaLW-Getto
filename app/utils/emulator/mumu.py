# app/utils/emulator/mumu.py
import subprocess
import json
from ..datetime import sleep
from .generic import GenericEmulator

class MuMu12Emulator(GenericEmulator):
    def __init__(self, *, 
                 manager_path: str,
                 instance_id: str = '0',
                 emulator_name: str,
                 adb_path: str,
                 adb_address: str,
                 default_app_package_name: str,
                 **kwargs
                 ) -> None:
        """
        Args:
            manager_path: Path to MuMuManager.exe
            instance_id: Instance ID (default "0" for first instance)
            emulator_name: Name of the emulator
            adb_path: Path to adb executable
            adb_address: ADB connection string (e.g. "127.0.0.1:7555")
            default_app_package_name: Package name of the app to control
        """
        super().__init__(emulator_name=emulator_name, adb_path=adb_path, adb_address=adb_address, default_app_package_name=default_app_package_name)
        self.manager_path = manager_path
        self.instance_id = str(instance_id)

    def _run_manager_command(self, command: str, args: list[str] = [], timeout: int = 30) -> str | None:
        """Execute MuMuManager command and return output"""
        try:
            cmd = [self.manager_path, command, "-v", self.instance_id] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except subprocess.SubprocessError:
            return None
    
    def _run_manager_control(self, subcommand: str, args: list[str] = [], timeout: int = 30) -> str | None:
        return self._run_manager_command("control", [subcommand] + args, timeout)

    def start(self) -> bool:
        """Start emulator using MuMuManager"""
        # First try native manager command
        if self._run_manager_control("launch"):
            # Wait for ADB to become available
            return self.wait_until_ready()
        
        # Fallback to ADB if manager fails
        return super().start()

    def stop(self, force: bool = False) -> bool:
        """Stop emulator using MuMuManager"""
        command = "shutdown"
        if self._run_manager_control(command):
            return True
        
        # Fallback to ADB if manager fails
        return super().stop(force)

    def restart(self) -> bool:
        """Restart emulator using MuMuManager"""
        if self._run_manager_control("restart", timeout=120):
            return self.wait_until_ready()
        return False

    def list_all_instances(self) -> dict[dict]:
        """List all MuMu instances (extended functionality)"""
        try:
            result = subprocess.run(
                [self.manager_path, "info", "-v", "all"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30
            )
            
            return json.loads(result.stdout.strip())
        except (subprocess.SubprocessError, json.JSONDecodeError):
            return {}

    def get_instance_info(self) -> dict | None:
        """Get detailed info about current instance"""
        result = self._run_manager_command("info")
        if result is None:
            return None
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return None

    def is_running(self) -> bool:
        """Check if emulator is running through manager"""
        info = self.get_instance_info()
        if info:
            return info.get("is_android_started", False) is True or super().is_running()
        return super().is_running()

    def is_app_running(self, package_name: str | None = None) -> bool:
        if package_name is None:
            package_name = self.default_app_package_name
        info = self._run_manager_control("app", ["info", "-pkg", package_name])
        try:
            return json.loads(info).get("state") == "running"
        except:
            return super().is_app_running(package_name)
        
    def is_app_stopped(self, package_name: str | None = None) -> bool:
        if package_name is None:
            package_name = self.default_app_package_name
        info = self._run_manager_control("app", ["info", "-pkg", package_name])
        try:
            return json.loads(info).get("state") == "stopped"
        except:
            return super().is_app_stopped(package_name)
        
    def start_app(self, package_name: str | None = None) -> bool:
        if package_name is None:
            package_name = self.default_app_package_name
        if self._run_manager_control("app", ["launch", "-pkg", package_name]) is not None:
            if self.wait_until_app_ready(package_name):
                return True
        return super().start_app(package_name)

    def stop_app(self, package_name: str | None = None) -> bool:
        if package_name is None:
            package_name = self.default_app_package_name
        if self._run_manager_control("app", ["close", "-pkg", package_name]) is not None:
            if self.wait_until_app_stopped(package_name, timeout=10):
                return True
        return super().stop_app(package_name)