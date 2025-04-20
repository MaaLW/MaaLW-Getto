from app.utils.emulator import EmulatorFactory
from app.utils.emulator.mumu import MuMu12Emulator

emu = EmulatorFactory.create_emulator("mumu12", 
                                      manager_path="C:/Program Files/Netease/MuMu Player 12/shell/MuMuManager.exe", 
                                      instance_id=str(1), 
                                      emulator_name="Mumu12-1", 
                                      adb_path="C:/Program Files/Netease/MuMu Player 12/shell/adb.exe", 
                                      adb_address="192.168.0.131:5555", 
                                      default_app_package_name="com.gg.lostword.bilibili")

assert isinstance(emu, MuMu12Emulator)
#emu.start()
print(emu.get_instance_info())
print(emu.is_app_running())
print(emu.is_app_running("dummy"))

from code import interact
interact(local=locals())
