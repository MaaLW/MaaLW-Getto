from maa.toolkit import Toolkit


user_path = "./assets/cache"

Toolkit.init_option(user_path)

adb_devices = Toolkit.find_adb_devices()
for device in adb_devices:
    print(device)
