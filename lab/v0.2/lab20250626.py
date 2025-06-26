# coding:utf-8

from dataclasses import asdict
from pathlib import Path
import json
from time import sleep, time

from code import interact

#import maa
from maa.tasker import Tasker
from maa.toolkit import Toolkit, AdbDevice
from maa.resource import Resource
from maa.controller import AdbController

# for register decorator
resource = Resource()


def main():
    user_path = "./assets/cache"
    resource_path = "./assets/resource/base"

    with open('./MLW-config.json', 'r', encoding='UTF-8') as file:
        mlw_config = json.load(file)
        adb_device_info = mlw_config.get("adb_device")

    Toolkit.init_option(user_path)

    res_job = resource.post_bundle(resource_path)
    res_job.wait()

    adb_device = AdbDevice(
        name = adb_device_info.get("name"),
        adb_path = Path(adb_device_info.get("adb_path")),
        address = adb_device_info.get("address"),
        screencap_methods = adb_device_info.get("screencap_methods"),     # 64 4 2 1
        input_methods = adb_device_info.get("input_methods"),         # DON'T USE 8 On Mumu
        config = adb_device_info.get("config")
    )
    controller = AdbController(**{k:v for k,v in asdict(adb_device).items() if not k == "name"})
    controller.post_connection().wait()

    tasker = Tasker()
    # tasker = Tasker(notification_handler=MyNotificationHandler())
    tasker.bind(resource, controller)

    if not tasker.inited:
        print("Failed to init MAA.")
        exit()

    # Start Lab Below
    lab_timeout = 1
    time_start = time()
    job = tasker.post_task("lab20250626_Entrance")
    print(time() - time_start, "Task Started")
    while not job.done:
        print(time() - time_start, "Task ID", job.job_id, "is Running")
        if time() - time_start < lab_timeout:
            sleep(0.1)
        else:
            print(time() - time_start, "Task ID", job.job_id, "is Timeout")
            tasker.post_stop()
            print(time() - time_start, "Posted Stop Signal. Now tasker.stopping is", tasker.stopping)
            while tasker.stopping:
                print(time() - time_start, "Tasker is still stopping...")
                sleep(0.02)
            break
    time_job2_start = time()
    job2 = tasker.post_task("lab20250626_Entrance")
    print(job2.job_id, job2.done, job2.failed, job2.pending, job2.running, job2.succeeded)
    print(time() - time_start, "Task ID", job2.job_id, "is Running")
    while not job2.done:
        print(time() - time_start, "Task ID", job2.job_id, "is Running")
        if time() - time_job2_start < lab_timeout:
            sleep(0.1)
        else:
            print(time() - time_start, "Task ID", job2.job_id, "is Timeout")
            tasker.post_stop()
            print(time() - time_start, "Posted Stop Signal. Now tasker.stopping is", tasker.stopping)
            break

    print(time() - time_start, "Task Completed")
    


if __name__ == "__main__":
    main()