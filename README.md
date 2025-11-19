# 刘子硕（Grant Scholar）的生存厨房 / Grant Scholar's Survival Kitchen

一个基于Pygame的生存模拟游戏。A survival simulation game built with Pygame.

## 游戏简介 / Game Overview

刘子硕距离硕士毕业只剩30天，但生活费只剩1500元！玩家需要帮助他合理安排饮食，平衡各项属性，顺利度过这30天并完成毕业。

Grant Scholar has only 30 days until graduation, but only $1500 left for living expenses! Help him manage his diet, balance various attributes, and survive these 30 days to graduate.

## 项目特色 / Project Features

### 🎯 专业的工程结构
- **数据驱动设计**: 所有游戏配置使用JSON文件，便于策划调整数值
- **资产管理系统**: 完整的美术资源加载和缓存系统，支持图片、音频、字体
- **模块化架构**: 代码按功能分层组织，易于维护和扩展
- **单例数据加载器**: 统一管理所有配置文件的加载和访问
- **标准Python包**: 包含setup.py、pyproject.toml等标准配置

### 🎮 游戏特色
- **五维属性系统**: 体力、心情、健康、饱腹、金钱
- **丰富事件系统**: 固定事件、条件事件、随机事件
- **烹饪系统**: 购买食材，制作多种菜品
- **时间管理**: 每天分为早间、白天、采购、晚饭、夜间、睡觉六个时段

## 项目结构 / Project Structure

```
GrantScholarSurvivalKitchen/
├── assets/                # 美术资源（图片、音频、字体）
│   ├── images/           # 图片资源
│   ├── sounds/           # 音频资源
│   └── fonts/            # 字体文件
├── data/                  # 游戏配置数据（JSON格式）
│   ├── config.json       # 窗口、颜色、游戏设置
│   ├── stats.json        # 玩家属性配置
│   ├── items.json        # 食材和餐厅菜单
│   ├── recipes.json      # 烹饪食谱
│   ├── events.json       # 游戏事件
│   └── assets.json       # 资产路径配置
├── src/                   # 源代码
│   ├── data_loader.py    # 数据加载器
│   ├── asset_loader.py   # 资产加载器
│   ├── config.py         # 配置常量
│   ├── player.py         # 玩家类
│   ├── events.py         # 事件系统
│   ├── scenes.py         # 场景管理
│   ├── ui.py             # UI组件
│   └── game.py           # 游戏主控制
├── main.py               # 程序入口
└── ...
```

详细说明请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 美术资源 / Art Assets

### 资源目录结构

游戏支持完整的美术资源系统，资源文件存放在 `assets/` 目录：

- `assets/images/` - 图片资源（UI、角色、物品、背景）
- `assets/sounds/` - 音频资源（背景音乐、音效）
- `assets/fonts/` - 字体文件

### 添加资源 / Adding Assets

1. 将图片文件放入 `assets/images/` 相应子目录
2. 将音频文件放入 `assets/sounds/` 相应子目录
3. 将字体文件放入 `assets/fonts/` 目录

代码中使用资源：
```python
from src.asset_loader import asset_loader

# 加载图片
image = asset_loader.load_image('items/egg.png')

# 加载音效
sound = asset_loader.load_sound('sfx/click.wav')

# 加载字体
font = asset_loader.load_font('game_font.ttf', 24)
```

详细指南请查看：
- [assets/README.md](assets/README.md) - 资源目录说明
- [ASSET_GUIDE.md](ASSET_GUIDE.md) - 完整使用指南

## 策划人员快速上手 / Quick Start for Game Designers

### 修改游戏数值 / Modifying Game Values

所有游戏数据都在 `data/` 目录的JSON文件中，您可以直接编辑：

1. **调整玩家初始属性** (`data/stats.json`)
2. **添加新食材** (`data/items.json`)
3. **创建新食谱** (`data/recipes.json`)
4. **设计新事件** (`data/events.json`)
5. **修改游戏参数** (`data/config.json`)

### 示例：添加新食材

编辑 `data/items.json`:
```json
{
  "ingredients": {
    "新食材名": {
      "price": 价格,
      "location": "Market",  // 或 "Convenience Store"
      "shelf_life": 保质期天数,
      "description": "描述"
    }
  }
}
```

修改后无需重新编译，直接运行游戏即可生效！

详细配置指南请查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
```bash
pip install -r requirements.txt
```

4. 运行游戏：
```bash
python main.py
```

### 方式二：作为包安装 / Install as Package

```bash
# 开发模式安装
pip install -e .

# 或直接安装
pip install .

# 运行游戏
grant-scholar
```

## 运行游戏 / Run Game

### Windows
```bash
# 使用虚拟环境Python
.venv\Scripts\python.exe main.py

# 或双击运行
run_game.bat
```

### Linux/Mac
```bash
python main.py
```

## 游戏玩法

### 属性说明

- **体力(0-100)**: 做饭等行动需要消耗，睡觉恢复
- **心情(五档)**: 影响随机事件触发概率
- **健康(0-100)**: 归零则游戏失败
- **饱腹(0-100)**: 随时间下降，归零后持续扣血
- **金钱**: 购买食材消耗

### 每日流程

1. **早间**: 查看状态，触发随机事件
2. **白天**: 可能遇到固定事件或随机事件
3. **采购**: 选择菜市场、便利店、餐厅或放弃采买
4. **晚饭**: 用现有食材烹饪（可多次）
5. **夜间**: 提前休息/消磨时间/熬夜
6. **睡觉**: 恢复体力，进入下一天

### 食材与食谱

#### 食材
- 即食面、鸡蛋、番茄、米饭、猪肉（菜市场）
- 便当A、便当B（便利店）
- 烧鹅饭（餐厅直接食用）

#### 食谱
- 煮即食面、鸡蛋即食面
- 番茄炒蛋、煲仔饭
- 便当A/B（直接食用）

### 游戏目标

在30天内保持健康值不归零，成功毕业！

## 操作说明

- 鼠标左键：选择选项/购买物品
- 鼠标右键（购物界面）：取消已选物品

## 开发信息

- 开发语言: Python
- 游戏引擎: Pygame
- 版本: 1.0

## 文件结构

```
GrantScholarSurvivalKitchen/
├── main.py          # 主程序入口
├── game.py          # 游戏主控制
├── player.py        # 玩家属性管理
├── events.py        # 事件系统
├── scenes.py        # 场景系统
├── ui.py            # UI组件
├── config.py        # 游戏配置
├── requirements.txt # 依赖列表
└── README.md        # 说明文档
```

## 注意事项

- 食材有保质期，过期会自动丢弃
- 体力耗尽会强制昏睡并扣除心情和健康
- 连续三天心情低落会触发家人关心事件
- 合理规划金钱，避免入不敷出

祝游戏愉快！
