import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入功能实现模块
from 饥荒功能实现 import show_character_gallery, show_food_guide, show_item_guide, show_mod_recommendations

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
    
    # 创建功能按钮区域
    buttons_frame = ttk.Frame(content_frame)
    buttons_frame.pack(fill=tk.X, pady=(0, 20))
    
    # 创建四个功能按钮
    btn_width = 15
    character_btn = ttk.Button(buttons_frame, text="人物图鉴", width=btn_width,
                             command=lambda: show_character_gallery(content_frame))
    character_btn.pack(side=tk.LEFT, padx=10)
    
    food_btn = ttk.Button(buttons_frame, text="食物介绍", width=btn_width,
                        command=lambda: show_food_guide(content_frame))
    food_btn.pack(side=tk.LEFT, padx=10)
    
    item_btn = ttk.Button(buttons_frame, text="物品介绍", width=btn_width,
                        command=lambda: show_item_guide(content_frame))
    item_btn.pack(side=tk.LEFT, padx=10)
    
    mod_btn = ttk.Button(buttons_frame, text="MOD推荐", width=btn_width,
                       command=lambda: show_mod_recommendations(content_frame))
    mod_btn.pack(side=tk.LEFT, padx=10)
    
    # 创建显示区域（用于显示各个功能的内容）
    global display_frame
    display_frame = ttk.Frame(content_frame)
    display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # 初始显示欢迎信息
    welcome_label = tk.Label(display_frame, text="请选择上方的功能按钮开始探索", 
                          font=('SimHei', 12), fg="blue")
    welcome_label.pack(pady=50)

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