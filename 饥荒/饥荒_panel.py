import tkinter as tk
from tkinter import ttk

# 显示饥荒游戏面板
def show_panel(parent, game_data):
    # 设置中文字体
    default_font = ('SimHei', 10)
    
    # 创建内容框架
    content_frame = ttk.Frame(parent)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # 游戏描述
    desc_text = "饥荒是一款生存类游戏，玩家需要在充满危险的世界中收集资源、建造基地、制作工具，努力存活下去。游戏拥有丰富的角色系统和多样化的生存挑战。"
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
    create_info_card(info_frame, "当前版本", "2023.12.01", 0, 0)
    
    # 信息卡片2：可用角色
    create_info_card(info_frame, "可用角色", "25+", 0, 1)
    
    # 创建功能按钮区域
    feature_frame = ttk.Frame(content_frame)
    feature_frame.pack(fill=tk.BOTH, expand=True)
    
    # 设置网格权重，使按钮均匀分布
    feature_frame.columnconfigure(0, weight=1)
    feature_frame.columnconfigure(1, weight=1)
    feature_frame.rowconfigure(0, weight=1)
    feature_frame.rowconfigure(1, weight=1)
    
    # 创建功能按钮
    create_feature_button(feature_frame, "生存指南", "学习基础生存技巧和策略", 0, 0)
    create_feature_button(feature_frame, "角色图鉴", "了解所有角色的特性和能力", 0, 1)
    create_feature_button(feature_frame, "资源百科", "查询各类资源的获取和用途", 1, 0)
    create_feature_button(feature_frame, "MOD推荐", "探索热门MOD和使用方法", 1, 1)

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