# 使用方法
把队伍配置好，永远战线作战脚本准备好

## 安装MaaFramework

```pip install maafw```

## 启动脚本

```python main.py```

启动时请确保游戏在永远战线入口界面

## 退出运行

修改stop.json并保存，等待本次战斗结束

# 配置文件
## MLW-config.json
    可以配置模拟器信息，永远战线作战脚本路径

例子（项目自带的配置文件使用的mumu多开1，例子是没有多开的）

```json
{
    "adb_device": {
        "name": "MuMu12-test",
        "adb_path": "C:/Program Files/Netease/MuMu Player 12/shell/adb.exe",
        "address": "127.0.0.1:16384",
        "screencap_methods": 71,
        "input_methods": 7,
        "config": {
            "extras": {
                "mumu": {
                    "enable": true,
                    "index": 0,
                    "path": "C:/Program Files/Netease/MuMu Player 12"
                }
            }
        },
        "doc00": "请确保adb_path和address为实际地址"
    },
    "eternal_battle_record": {
        "path": "assets/battlescript/2.json",
        "doc00": "path为永远战线录制文件路径"
    }
}
```

## stop.json
    false 一直玩
    true 本次战斗结束后退出
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

# MaaFramework

</div>

本仓库为基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 所开发的东方归言录自动化工具。

> **MaaFramework** 是基于图像识别技术、运用 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 开发经验去芜存菁、完全重写的新一代自动化黑盒测试框架。
> 低代码的同时仍拥有高扩展性，旨在打造一款丰富、领先、且实用的开源库，助力开发者轻松编写出更好的黑盒测试程序，并推广普及。