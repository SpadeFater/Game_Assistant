import tkinter as tk
from tkinter import ttk

# 显示我的世界游戏面板
def show_panel(parent, game_data):
    # 设置中文字体
    default_font = ('SimHei', 10)
    
    # 创建内容框架
    content_frame = ttk.Frame(parent)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # 游戏描述
    desc_text = "我的世界是一款沙盒建造游戏，玩家可以在三维空间中自由创造和破坏不同种类的方块。游戏拥有无限的可能性，支持单人游戏和多人联机。"
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
    create_info_card(info_frame, "当前版本", "Java 1.20.4", 0, 0)
    
    # 信息卡片2：月活跃用户
    create_info_card(info_frame, "月活跃用户", "1.4亿+", 0, 1)
    
    # 创建功能按钮区域
    feature_frame = ttk.Frame(content_frame)
    feature_frame.pack(fill=tk.BOTH, expand=True)
    
    # 设置网格权重，使按钮均匀分布
    feature_frame.columnconfigure(0, weight=1)
    feature_frame.columnconfigure(1, weight=1)
    feature_frame.rowconfigure(0, weight=1)
    feature_frame.rowconfigure(1, weight=1)
    
    # 创建功能按钮
    create_feature_button(feature_frame, "方块图鉴", "查询所有方块的特性和用途", 0, 0)
    create_feature_button(feature_frame, "红石教程", "学习红石电路设计和应用", 0, 1)
    create_feature_button(feature_frame, "建筑灵感", "探索精美的建筑设计", 1, 0)
    create_feature_button(feature_frame, "模组推荐", "发现热门模组和数据包", 1, 1)

# 创建信息卡片
def create_info_card(parent, title, value, row, column):
    card_frame = ttk.Frame(parent, padding=15)
    card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
    # 卡片标题
    title_label = tk.Label(card_frame, text=title, font=('SimHei', 10, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 8))
    
    # 卡片内容
    value_label = tk.Label(card_frame, text=value, font=('SimHei', 10))
    value_label.pack(anchor=tk.W)

# 创建功能按钮
def create_feature_button(parent, title, description, row, column):
    button_frame = ttk.Frame(parent)
    button_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
    # 按钮标题
    title_label = tk.Label(button_frame, text=title, font=('SimHei', 10, 'bold'))
    title_label.pack(anchor=tk.W, pady=(0, 5))
    
    # 按钮描述
    desc_label = tk.Label(button_frame, text=description, font=('SimHei', 9), wraplength=250)
    desc_label.pack(anchor=tk.W, pady=(0, 10))
    
    # 操作按钮
    action_button = ttk.Button(button_frame, text="查看详情")
    action_button.pack(anchor=tk.W, fill=tk.X)