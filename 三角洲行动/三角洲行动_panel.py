import tkinter as tk
from tkinter import ttk

# 显示三角洲行动游戏面板
def show_panel(parent, game_data):
    # 设置中文字体
    default_font = ('SimHei', 12)
    
    # 创建内容框架
    content_frame = ttk.Frame(parent)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # 游戏描述
    desc_text = "三角洲行动是一款经典的战术射击游戏，玩家将扮演精英特种部队成员，执行各种高难度任务。游戏以其真实的武器系统和战术玩法而闻名。"
    desc_label = tk.Label(
        content_frame,
        text=desc_text,
        font=default_font,
        wraplength=600,
        justify=tk.LEFT
    )
    desc_label.pack(anchor=tk.W, pady=(0, 20))
    
    # 创建信息卡片区域
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(fill=tk.X, pady=(0, 20))
    
    # 设置网格权重，使卡片均匀分布
    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=1)
    
    # 信息卡片1：当前版本
    create_info_card(info_frame, "当前版本", "1.2.0", 0, 0)
    
    # 信息卡片2：活跃玩家
    create_info_card(info_frame, "活跃玩家", "250,000+", 0, 1)
    
    # 创建功能按钮区域
    feature_frame = ttk.Frame(content_frame)
    feature_frame.pack(fill=tk.BOTH, expand=True)
    
    # 设置网格权重，使按钮均匀分布
    feature_frame.columnconfigure(0, weight=1)
    feature_frame.columnconfigure(1, weight=1)
    feature_frame.rowconfigure(0, weight=1)
    feature_frame.rowconfigure(1, weight=1)
    
    # 创建功能按钮
    create_feature_button(feature_frame, "武器数据库", "查看所有可用武器信息", 0, 0)
    create_feature_button(feature_frame, "地图指南", "探索游戏中的各个地图", 0, 1)
    create_feature_button(feature_frame, "战术技巧", "学习高级战术和策略", 1, 0)
    create_feature_button(feature_frame, "新闻资讯", "获取游戏最新更新和活动", 1, 1)

# 创建信息卡片
def create_info_card(parent, title, value, row, column):
    card_frame = ttk.Frame(parent, padding=15)
    card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
    # 卡片标题
    title_label = tk.Label(card_frame, text=title, font=('SimHei', 11, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 8))
    
    # 卡片内容
    value_label = tk.Label(card_frame, text=value, font=('SimHei', 12))
    value_label.pack(anchor=tk.W)

# 创建功能按钮
def create_feature_button(parent, title, description, row, column):
    button_frame = ttk.Frame(parent)
    button_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
    # 按钮标题
    title_label = tk.Label(button_frame, text=title, font=('SimHei', 12, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 5))
    
    # 按钮描述
    desc_label = tk.Label(button_frame, text=description, font=('SimHei', 10), wraplength=250)
    desc_label.pack(anchor=tk.W, pady=(0, 10))
    
    # 操作按钮
    action_button = ttk.Button(button_frame, text="查看详情")
    action_button.pack(anchor=tk.W, fill=tk.X)