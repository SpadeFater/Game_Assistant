import tkinter as tk
from tkinter import ttk
import random

def show_panel(parent_frame, game_data):
    """显示DOTA2游戏面板"""
    # 游戏描述
    ttk.Label(
        parent_frame,
        text="多人在线战术竞技游戏，10v10对战模式，拥有100多个独特英雄。",
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
    
    # DOTA2特有信息
    stats = {
        "活跃玩家": f"{random.randint(1000000, 2000000)}",
        "服务器状态": "正常" if random.random() > 0.1 else "维护中",
        "最新版本": f"{random.randint(7, 8)}.{random.randint(0, 30)}",
        "Ti赛事": "即将开始" if random.random() > 0.7 else "进行中"
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
    features_frame = ttk.LabelFrame(parent_frame, text="DOTA2功能", padding=10)
    features_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 添加DOTA2特有功能按钮
    feature_buttons = [
        ("🎯 开始游戏", lambda: start_game(game_data)),
        ("👤 英雄指南", lambda: show_hero_guides()),
        ("📋 战绩查询", lambda: show_match_history()),
        ("🏆 MMR排名", lambda: show_mmr_ranking()),
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

def show_hero_guides():
    global content_area
    content_area.config(text="显示英雄技能和出装建议")
    # 这里可以添加显示英雄指南的代码

def show_match_history():
    global content_area
    content_area.config(text="查询近期比赛记录和数据统计")
    # 这里可以添加查询战绩的代码

def show_mmr_ranking():
    global content_area
    content_area.config(text="显示MMR排名和段位信息")
    # 这里可以添加显示MMR排名的代码

def show_settings(game_data):
    global content_area
    content_area.config(text=f"打开 {game_data['name']} 的设置界面")
    # 这里可以添加显示设置界面的代码

def show_community(game_data):
    global content_area
    content_area.config(text=f"访问 {game_data['name']} 的社区页面")
    # 这里可以添加访问社区页面的代码