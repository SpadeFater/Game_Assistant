import tkinter as tk
from tkinter import ttk
import random

def show_panel(parent_frame, game_data):
    """显示原神游戏面板"""
    # 游戏描述
    ttk.Label(
        parent_frame,
        text="开放世界冒险游戏，玩家可以探索提瓦特大陆，收集角色和武器。",
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
    
    # 原神特有信息
    stats = {
        "活跃玩家": f"{random.randint(6000000, 9000000)}",
        "服务器状态": "正常" if random.random() > 0.1 else "维护中",
        "最新版本": f"{random.randint(4, 5)}.{random.randint(0, 8)}",
        "当前活动": "限时祈愿" if random.random() > 0.3 else "版本活动"
    }
    
    for i, (label, value) in enumerate(stats.items()):
        card = ttk.Frame(cards_frame, padding=10, relief=tk.RAISED)
        card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
        ttk.Label(card, text=label, font=("SimHei", 9)).pack(anchor=tk.CENTER)
        ttk.Label(card, text=value, font=("SimHei", 12, "bold")).pack(anchor=tk.CENTER)
    
    # 设置网格权重，让卡片均匀分布
    for i in range(len(stats)):
        cards_frame.columnconfigure(i, weight=1)

def create_feature_section(parent_frame, game_data):
    """创建功能区"""
    # 创建功能区框架
    features_frame = ttk.LabelFrame(parent_frame, text="原神功能", padding=10)
    features_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 添加原神特有功能按钮
    feature_buttons = [
        ("🎯 开始游戏", lambda: start_game(game_data)),
        ("👤 角色信息", lambda: show_character_info()),
        ("⚔️ 武器数据", lambda: show_weapon_data()),
        ("🗺️ 地图工具", lambda: show_map_tools()),
        ("🔧 设置", lambda: show_settings(game_data)),
        ("💬 社区", lambda: show_community(game_data))
    ]
    
    button_frame = ttk.Frame(features_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    for i, (text, command) in enumerate(feature_buttons):
        row = i // 3
        col = i % 3
        button = ttk.Button(
            button_frame,
            text=text,
            width=15,
            command=command
        )
        button.grid(row=row, column=col, padx=5, pady=5)
    
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

def show_character_info():
    global content_area
    content_area.config(text="显示角色属性和培养建议")
    # 这里可以添加显示角色信息的代码

def show_weapon_data():
    global content_area
    content_area.config(text="显示武器属性和搭配推荐")
    # 这里可以添加显示武器数据的代码

def show_map_tools():
    global content_area
    content_area.config(text="打开地图标记和资源查询工具")
    # 这里可以添加显示地图工具的代码

def show_settings(game_data):
    global content_area
    content_area.config(text=f"打开 {game_data['name']} 的设置界面")
    # 这里可以添加显示设置界面的代码

def show_community(game_data):
    global content_area
    content_area.config(text=f"访问 {game_data['name']} 的社区页面")
    # 这里可以添加访问社区页面的代码