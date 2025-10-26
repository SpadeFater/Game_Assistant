import tkinter as tk
from tkinter import ttk
import random

def show_panel(parent_frame, game_data):
    """显示绝地求生游戏面板"""
    # 游戏描述
    ttk.Label(
        parent_frame,
        text="大逃杀类型游戏，100名玩家在孤岛上战斗，最后存活者获胜。",
        font=("SimHei", 10)
    ).pack(anchor=tk.W, padx=20, pady=(0, 20))
    
    # 创建游戏信息卡片
    create_info_cards(parent_frame)
    
    # 创建功能区
    create_feature_section(parent_frame, game_data)

def create_info_cards(parent_frame):
    """创建游戏信息卡片"""
    # 创建信息卡片容器
    cards_frame = ttk.Frame(parent_frame)
    cards_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # 绝地求生特有信息
    stats = {
        "在线人数": f"{random.randint(3000000, 5000000)}",
        "服务器状态": "正常" if random.random() > 0.1 else "维护中",
        "最新版本": f"{random.randint(25, 30)}.{random.randint(0, 9)}",
        "地图轮换": "艾伦格" if random.random() > 0.5 else "米拉玛"
    }
    
    for i, (label, value) in enumerate(stats.items()):
        # 增大卡片尺寸和内边距
        card = ttk.Frame(cards_frame, padding=15, relief=tk.RAISED)
        card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        ttk.Label(card, text=label, font=("SimHei", 11)).pack(anchor=tk.CENTER)
        ttk.Label(card, text=value, font=("SimHei", 14, "bold")).pack(anchor=tk.CENTER)
    
    # 设置网格权重，让卡片均匀分布
    for i in range(len(stats)):
        cards_frame.columnconfigure(i, weight=1)

def create_feature_section(parent_frame, game_data):
    """创建功能区"""
    # 创建功能区框架
    features_frame = ttk.LabelFrame(parent_frame, text="绝地求生功能", padding=10)
    features_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 添加绝地求生特有功能按钮
    feature_buttons = [
        ("🎯 开始游戏", lambda: start_game(game_data)),
        ("🔫 武器数据", lambda: show_weapon_data()),
        ("📋 战绩查询", lambda: show_match_history()),
        ("🗺️ 地图信息", lambda: show_map_info()),
        ("🔧 设置", lambda: show_settings(game_data)),
        ("💬 社区", lambda: show_community(game_data))
    ]
    
    # 创建按钮容器，使用网格布局，增大边距
    button_frame = ttk.Frame(features_frame)
    button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # 使用网格布局排列按钮，增大按钮尺寸和间距，改为2列布局
    for i, (text, command) in enumerate(feature_buttons):
        row = i // 2
        col = i % 2
        # 使用更大的按钮尺寸
        button = ttk.Button(
            button_frame,
            text=text,
            width=20,
            padding=10,
            command=command
        )
        button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
    # 使按钮能够均匀拉伸并占据更多空间
    for i in range(2):  # 改为2列布局，让按钮更宽
        button_frame.columnconfigure(i, weight=1, minsize=250)
    for i in range((len(feature_buttons) + 1) // 2):
        button_frame.rowconfigure(i, weight=1, minsize=80)
    
    # 创建内容区域
    global content_area
    content_area = ttk.Label(
        features_frame,
        text=f"选择上方功能按钮以操作 {game_data['name']}",
        font=("SimHei", 11)
    )
    content_area.pack(pady=20)

# 功能函数定义
def start_game(game_data):
    global content_area
    content_area.config(text=f"正在启动 {game_data['name']}...")
    # 这里可以添加实际启动游戏的代码

def show_weapon_data():
    global content_area
    content_area.config(text="显示武器属性和伤害数据")
    # 这里可以添加显示武器数据的代码

def show_match_history():
    global content_area
    content_area.config(text="查询近期比赛记录和击杀统计")
    # 这里可以添加查询战绩的代码

def show_map_info():
    global content_area
    content_area.config(text="显示地图信息和资源分布")
    # 这里可以添加显示地图信息的代码

def show_settings(game_data):
    global content_area
    content_area.config(text=f"打开 {game_data['name']} 的设置界面")
    # 这里可以添加显示设置界面的代码

def show_community(game_data):
    global content_area
    content_area.config(text=f"访问 {game_data['name']} 的社区页面")
    # 这里可以添加访问社区页面的代码