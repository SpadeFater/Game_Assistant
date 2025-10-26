import tkinter as tk
from tkinter import ttk
import random

def show_panel(parent_frame, game_data):
    """显示王者荣耀游戏面板"""
    # 游戏描述
    ttk.Label(
        parent_frame,
        text="多人在线战术竞技手游，5v5对战模式，拥有丰富的英雄角色。",
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
    
    # 王者荣耀特有信息
    stats = {
        "当前版本": "S38",
        "活跃英雄": "120+",
        "游戏模式": "5v5",
        "服务器状态": "正常"
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
    features_frame = ttk.LabelFrame(parent_frame, text="王者荣耀功能", padding=10)
    features_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 添加王者荣耀特有功能按钮
    feature_buttons = [
        ("🎯 开始游戏", lambda: start_game(game_data)),
        ("👤 英雄攻略", lambda: show_hero_guides()),
        ("📋 战绩查询", lambda: show_match_history()),
        ("🏆 排行榜", lambda: show_ranking()),
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

def show_hero_guides():
    global content_area
    content_area.config(text="显示英雄技能和出装建议")
    # 这里可以添加显示英雄攻略的代码

def show_match_history():
    global content_area
    content_area.config(text="查询近期比赛记录和战绩统计")
    # 这里可以添加查询战绩的代码

def show_ranking():
    global content_area
    content_area.config(text="显示排位赛排行榜和段位信息")
    # 这里可以添加显示排行榜的代码

def show_settings(game_data):
    global content_area
    content_area.config(text=f"打开 {game_data['name']} 的设置界面")
    # 这里可以添加显示设置界面的代码

def show_community(game_data):
    global content_area
    content_area.config(text=f"访问 {game_data['name']} 的社区页面")
    # 这里可以添加访问社区页面的代码