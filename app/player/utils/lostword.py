from subprocess import run

from ...config import config

adb_address = config.get("adb_device", "address")
lostword_package_name = config.get("lostword", "package_name")


def isLostwordRunning() -> bool:
    try: result = run(f'adb -s {adb_address} shell "ps | grep {lostword_package_name}"', timeout= 9, text= True, capture_output= True)
    except: return False
    return True if lostword_package_name in result.stdout else False

