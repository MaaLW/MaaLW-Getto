# 功能

**[MaaLW-Getto](https://github.com/MaaLW/MaaLW-Getto)**

自动刷永远战线

安卓模拟器建议使用MuMu模拟器或雷电模拟器，识图更快

分辨率需为最低`1280*720`的`16:9`比例

Python 3.12

## v0.1.x

目前可以应对的翻车情况：  
|        意外情况                          	|       措施             	|   	|   	|   	|
|----------------------------------	|--------------------	|---	|---	|---	|
| GameOver                         	| 尝试回到入口界面   	|   	|   	|   	|
| 动作执行完战斗没有结束（漏怪）   	| 尝试重新战斗       	|   	|   	|   	|
| 连接超时                         	| 尝试重连           	|   	|   	|   	|
|                                  	|                    	|   	|   	|   	|

# 使用方法

把队伍配置好，战斗操作按照[永远战线作战脚本](#作战脚本)格式写好

## 安装

`install.bat`

## 修改配置文件

[config.ini](#MLW-config)

## 启动脚本

```start.bat```

## 退出运行

```stop```

本次战斗结束后将停止

```force stop```

强制停止

## 再次开始

```start```

恢复连续战斗

`start 10`

战斗10次后停止


# 配置文件

## MLW-config

    config.ini 配置模拟器信息，游戏包名，永远战线作战脚本路径

例子（项目自带的配置文件使用的mumu多开1，例子是没有多开的）

```ini
[adb_device]
name = MuMu12
adb_path = C:/Program Files/Netease/MuMu Player 12/shell/adb.exe
address = 127.0.0.1:16384
screencap_methods = 71
input_methods = 7
config = {"extras": {"mumu": {"enable": true, "index": 0, "path": "C:/Program Files/Netease/MuMu Player 12"}}}

[lostword]
package_name = com.gg.lostword.bilibili

[lostword.eternal_battle_record]
path = assets/battlescript/2.json


```

`adb_path` 和 `address` 按模拟器实际地址修改，index为多开实例序号

可以使用 `find_Adb_device.bat` 或 `python find_Adb_device.py` 脚本来搜索本机的模拟器的 `adb_path` 和 `address`

### 截图增强模式

MuMu和雷电模拟器额外参数的配置，设置好了截图速度会快一些，其他模拟器可以不管

MuMu

```json
        {"extras": {"mumu": {"enable": true, "index": 0, "path": "C:/Program Files/Netease/MuMu Player 12"}}}
```

雷电

```json
        {"extras": {"mumu": {"enable": true, "index": 0, "path": "C:/leidian/LDPlayer9"}}}
```

其中 `index` 是多开的实例序号， `path` 是模拟器的安装位置

### 包名

可使用adb命令查找游戏包名

`adb shell "pm list packages | grep lostword"`

## 作战脚本

目前只需要改

 "difficulty" 从("normal" "hard" "lunatic")里选择一个

 "actions"

例子：
```json
{
    "name": "ebs1",
    "target": "eternal_battle",
    "version": "0.1.0",
    "doc00": "永远战线操作录制，使用MaaLW-Getto回放 ",
    "doc01": "battle actions: 1. fs(2|3) Focus Shot, 2. ss(2|3) Spread Shot, 3. sw Switch, 4. ba(2) Back, 5. sc(1-5) Spell Card, 6. sk(1-9) Skill,",
    "doc02": "7. en(2|3)(1-2|3) Enemy Target, 8. bo(1-3|m) Boost, 9. gr(1-3|m) Graze",
    "difficulty": "hard",
    "actions": {
        "area1": [
            "sk12389 bo3 sc1 sc1 gr2 ss",
            "sk64 bo3 sc3 sc3 gr2 ss",
            "sk578 bo3 sc5 bo3 sc5 bo3 sc5"
        ],
        "area2": [
            "sk1234 bo3 gr3 sc5 en31 sc3 sc2",
            "sk56 bo2 fs bo3 sc2 bo3 gr2 sc5",
            "sk2789 fs bo3 sc5 bo3 gr2 fs"
        ],
        "area3": [
            "sk4562 bo3 sc3 bo2 sc2 gr2 sc2",
            "sk3 bo3 sc1 bo3 sc3 bo3 gr2 sk8 sc3",
            "bo3 sc2 bo3 sc5 bo3 gr2 sc4",
            "sk1 bo3 sc5 bo3 fs bo3 sc1",
            "sw sk45 ss sw ba sk269 bo2 sc1 bo2 sc1 bo2 ss",
            "sk34 bo3 sc4 bo3 sc2 bo3 sc5",
            "sk157 bo3 sc5 bo3 sc5 bo3 ss"
        ]
    }
}
```

actions说明：

| 指令     	|             	| 说明                       	|   	|   	|
|----------	|-------------	|----------------------------	|---	|---	|
| fs[1-3]? 	| focus shot  	| 集中射击x次                	|   	|   	|
| ss[1-3]? 	| spread shot 	| 扩散射击x次                	|   	|   	|
| sw       	| switch      	| 换人                       	|   	|   	|
| ba[1-2]? 	| back        	| 返回x次                    	|   	|   	|
| sc[1-5]  	| spell card  	| 使用第x个符卡              	|   	|   	|
| sk[1-9]+ 	| skill       	| 依次使用数字对应位置的技能 	|   	|   	|
| en3[1-3] 	| enemy       	| 选择从右上起第x格的敌人    	|   	|   	|
| bo[1-3]  	| boost       	| 强化x次                    	|   	|   	|
| gr[1-3]  	| graze       	| 擦弹x次                    	|   	|   	|

目前没有检查指令合法性，不符合列表里模式的指令（如ss11 sc45）可能引发未定义行为


# Contact

QQ群 1034459632

# MaaFramework

</div>

本仓库为基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 所开发的东方归言录自动化工具。

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。