import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import random

# 人物图鉴功能
def show_character_gallery(parent):
    # 获取display_frame
    import 饥荒_panel
    if hasattr(饥荒_panel, 'display_frame'):
        target_frame = 饥荒_panel.display_frame
        # 清空显示容器
        clear_frame(target_frame)
        
        # 创建标题
        title_label = tk.Label(target_frame, text="饥荒人物图鉴", font=('SimHei', 14, 'bold'))
        title_label.pack(anchor=tk.W, padx=20, pady=(10, 20))
        
        # 示例角色数据
        characters = [
            {"name": "威尔逊", "description": "游戏主角，有着不错的胡须能力", "specialty": "胡子生长，可制作胡须帽"},
            {"name": "薇洛", "description": "纵火少女，免疫火焰伤害", "specialty": "免疫火焰，自带打火机"},
            {"name": "沃尔夫冈", "description": "大力士，力量随饱食度变化", "specialty": "高伤害，高生命，但消耗食物快"},
            {"name": "温蒂", "description": "忧郁少女，能召唤姐姐的帮助", "specialty": "召唤阿比盖尔，夜间精神消耗低"},
            {"name": "机器人WX-78", "description": "机器人，吃齿轮能升级", "specialty": "升级后属性提升，不怕下雨但会被闪电充电"},
            {"name": "薇克巴顿", "description": "图书管理员，知识渊博", "specialty": "制作不需要原型，读书恢复精神"},
            {"name": "伍迪", "description": "伐木工，拥有变身能力", "specialty": "变身海狸，无限砍伐"},
            {"name": "麦斯威尔", "description": "魔术师，高精神值", "specialty": "可以制造暗影分身，自带暗影剑"},
        ]
        
        # 创建角色列表框架
        list_frame = ttk.Frame(target_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建画布
        canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        # 创建内容框架
        content_frame = ttk.Frame(canvas)
        canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # 添加鼠标滚轮事件
        def on_mousewheel(event):
            # 对于Windows系统，event.delta是±120
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            # 阻止事件继续传播，避免被其他控件捕获
            return "break"
        
        # 为控件及其所有子控件绑定滚轮事件
        def bind_wheel_to_widget(widget):
            """为控件及其所有子控件绑定滚轮事件"""
            widget.bind("<MouseWheel>", on_mousewheel, add="+")
            # 递归绑定所有子控件
            for child in widget.winfo_children():
                bind_wheel_to_widget(child)
        
        # 存储创建的角色卡片，方便后续为其绑定滚轮事件
        character_cards = []
        
        # 添加角色卡片
        for character in characters:
            card = create_character_card(content_frame, character)
            character_cards.append(card)
        
        # 更新滚动区域
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # 绑定配置事件
        content_frame.bind("<Configure>", on_configure)
        
        # 为所有相关组件绑定滚轮事件
        list_frame.bind("<MouseWheel>", on_mousewheel, add="+")
        canvas.bind("<MouseWheel>", on_mousewheel, add="+")
        content_frame.bind("<MouseWheel>", on_mousewheel, add="+")
        
        # 为所有角色卡片及其子控件绑定滚轮事件
        for card in character_cards:
            bind_wheel_to_widget(card)

# 创建角色卡片
def create_character_card(parent, character_data):
    card = ttk.Frame(parent, padding=15, relief=tk.RAISED)
    card.pack(fill=tk.X, pady=10, padx=10)
    
    # 角色名称
    name_label = tk.Label(card, text=character_data["name"], font=('SimHei', 12, 'bold'))
    name_label.pack(anchor=tk.W, pady=(0, 5))
    
    # 角色描述
    desc_label = tk.Label(card, text=character_data["description"], font=('SimHei', 10))
    desc_label.pack(anchor=tk.W, pady=(0, 5))
    
    # 角色特长
    spec_label = tk.Label(card, text=f"特长: {character_data['specialty']}", font=('SimHei', 10), fg="blue")
    spec_label.pack(anchor=tk.W)
    
    # 返回卡片引用，方便后续绑定事件
    return card

# 食物介绍功能
def show_food_guide(display_frame):
    # 清空display_frame，只显示食物信息和限制条件
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    # 导入数据库处理模块
    from 饥荒_handler import MySQLHandler
    
    # 创建标题
    title_label = tk.Label(display_frame, text="饥荒食物指南", font=('SimHei', 16, 'bold'))
    title_label.pack(anchor=tk.W, padx=20, pady=(10, 20))
    
    # 大厨菜下拉框变量定义
    is_chef_dish_var = tk.StringVar(value="默认")
    # 人物效果下拉框变量定义
    character_effect_var = tk.StringVar(value="默认")
    
    # 重置筛选条件函数（在使用前定义）
    def reset_filters():
        is_chef_dish_var.set("默认")
        character_effect_var.set("默认")
    
    # 查询食物数据函数（在使用前定义）
    def query_food_data():
        # 清空内容框架
        clear_frame(content_frame)
        
        # 解析筛选条件
        is_chef_dish = is_chef_dish_var.get() if is_chef_dish_var.get() != "默认" else None
        character_effect = character_effect_var.get() if character_effect_var.get() != "默认" else None
        
        # 从数据库查询数据 - 使用donot_starve_food表
        db_handler = MySQLHandler()
        
        # 修改MySQLHandler的查询表名
        db_handler._table_name = 'donot_starve_food'  # 动态设置表名
        
        try:
            # 根据筛选条件查询数据
            foods = db_handler.get_food_data(is_chef_dish, character_effect)
            
            # 添加调试信息
            print(f"数据库返回数据数量: {len(foods)}")
            if foods:
                print(f"第一条数据格式: {foods[0].keys()}")
                print(f"第一条数据内容: {foods[0]}")
            else:
                print("数据库未返回任何数据")
        except Exception as e:
            print(f"查询数据库时出错: {str(e)}")
            foods = []
        
        # 如果没有数据，显示提示
        if not foods:
            no_data_label = tk.Label(content_frame, text="没有找到符合条件的食物数据", font=('SimHei', 12))
            no_data_label.pack(pady=50)
            return
        
        # 显示数据
        print(f"开始创建食物卡片，总数: {len(foods)}")
        for i, food in enumerate(foods):
            print(f"创建第{i+1}个食物卡片: {food.get('food_name', '未知食物')}")
            create_food_card(content_frame, food)
        print("所有食物卡片创建完成")
    
    # 创建筛选条件框架
    filter_frame = ttk.LabelFrame(display_frame, text="筛选条件")
    filter_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # 大厨菜下拉框
    ttk.Label(filter_frame, text="是否是大厨菜:", font=('SimHei', 10)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    is_chef_dish_combo = ttk.Combobox(filter_frame, textvariable=is_chef_dish_var, values=["默认", "T", "F"], state="readonly", width=10)
    is_chef_dish_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
    
    # 人物效果下拉框
    ttk.Label(filter_frame, text="人物效果:", font=('SimHei', 10)).grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
    character_effect_combo = ttk.Combobox(filter_frame, textvariable=character_effect_var, 
                                        values=["默认", "hot", "cold", "dry", "attack", "change", "light"], state="readonly", width=10)
    character_effect_combo.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)
    
    # 查询按钮
    query_button = ttk.Button(filter_frame, text="查询", command=lambda: query_food_data())
    query_button.grid(row=0, column=4, padx=20, pady=10)
    
    # 重置按钮
    reset_button = ttk.Button(filter_frame, text="重置", command=reset_filters)
    reset_button.grid(row=0, column=5, padx=10, pady=10)
    
    # 创建结果显示区域
    result_frame = ttk.Frame(display_frame)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # 创建滚动条
    scrollbar = ttk.Scrollbar(result_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 创建画布
    canvas = tk.Canvas(result_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=canvas.yview)
    
    # 创建内容框架
    content_frame = ttk.Frame(canvas)
    canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # 添加鼠标滚轮事件
    def on_mousewheel(event):
        # 对于Windows系统，event.delta是±120
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # 阻止事件继续传播，避免被其他控件捕获
        return "break"
    
    # 为控件及其所有子控件绑定滚轮事件
    def bind_wheel_to_widget(widget):
        """为控件及其所有子控件绑定滚轮事件"""
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 递归绑定所有子控件
        for child in widget.winfo_children():
            bind_wheel_to_widget(child)
    
    # 更新滚动区域
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    # 绑定配置事件
    canvas.bind("<Configure>", on_configure)
    content_frame.bind("<Configure>", on_configure)
    
    # 为所有相关组件绑定滚轮事件
    result_frame.bind("<MouseWheel>", on_mousewheel, add="+")
    canvas.bind("<MouseWheel>", on_mousewheel, add="+")
    content_frame.bind("<MouseWheel>", on_mousewheel, add="+")
    
    # 让query_food_data函数能够访问这个绑定函数
    def enhanced_query_food_data():
        # 清空内容框架
        clear_frame(content_frame)
        
        # 解析筛选条件
        is_chef_dish = is_chef_dish_var.get() if is_chef_dish_var.get() != "默认" else None
        character_effect = character_effect_var.get() if character_effect_var.get() != "默认" else None
        
        # 从数据库查询数据 - 使用donot_starve_food表
        db_handler = MySQLHandler()
        
        # 修改MySQLHandler的查询表名
        db_handler._table_name = 'donot_starve_food'  # 动态设置表名
        
        try:
            # 根据筛选条件查询数据
            foods = db_handler.get_food_data(is_chef_dish, character_effect)
            
            # 添加调试信息
            print(f"数据库返回数据数量: {len(foods)}")
            if foods:
                print(f"第一条数据格式: {foods[0].keys()}")
                print(f"第一条数据内容: {foods[0]}")
            else:
                print("数据库未返回任何数据")
        except Exception as e:
            print(f"查询数据库时出错: {str(e)}")
            foods = []
        
        # 如果没有数据，显示提示
        if not foods:
            no_data_label = tk.Label(content_frame, text="没有找到符合条件的食物数据", font=('SimHei', 12))
            no_data_label.pack(pady=50)
            # 为提示标签也绑定滚轮事件
            no_data_label.bind("<MouseWheel>", on_mousewheel, add="+")
            return
        
        # 显示数据
        print(f"开始创建食物卡片，总数: {len(foods)}")
        food_cards = []
        for i, food in enumerate(foods):
            print(f"创建第{i+1}个食物卡片: {food.get('food_name', '未知食物')}")
            card = create_food_card(content_frame, food)
            food_cards.append(card)
        print("所有食物卡片创建完成")
        
        # 为所有创建的食物卡片再次绑定滚轮事件，确保万无一失
        for card in food_cards:
            bind_wheel_to_widget(card)
    
    # 替换原来的query_food_data函数
    query_food_data = enhanced_query_food_data
    
    # 另外，为了确保所有子组件都能响应滚轮，我们需要一个更简单的方法：
    # 在内容框架创建后，对整个框架启用滚动传播
    # 这是Tkinter中处理嵌套控件滚动的标准方法
    
    # query_food_data函数已在上方定义，这里不再重复
    
    # 初始加载全部数据
    query_food_data()

# 创建食物卡片
def create_food_card(parent, food_data):
    """创建食物信息卡片，每条数据前预留图片空间"""
    print(f"创建食物卡片: {food_data.get('food_name', '未知食物')}，父容器类型: {type(parent).__name__}")
    
    # 创建普通的卡片框架
    card = ttk.Frame(parent, padding=15, relief=tk.RAISED)
    card.pack(fill=tk.X, pady=10, padx=10)
    
    # 查找并保存画布引用的函数
    def get_scroll_canvas(widget):
        """向上查找最近的Canvas父组件"""
        current = widget
        while current:
            if isinstance(current, tk.Canvas):
                return current
            if hasattr(current, 'master'):
                current = current.master
            else:
                break
        return None
    
    # 简单直接的滚轮处理函数
    def on_mousewheel(event):
        """处理卡片内的鼠标滚轮事件"""
        canvas = get_scroll_canvas(card)
        if canvas:
            # 对于Windows系统，event.delta是±120
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            # 阻止事件继续传播
            return "break"
    
    # 为卡片及其所有子组件创建后自动绑定滚轮事件
    def bind_wheel_to_widget(widget):
        """为控件及其所有子控件绑定滚轮事件"""
        # 使用add="+"确保不会覆盖现有绑定
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 递归绑定所有子控件
        for child in widget.winfo_children():
            bind_wheel_to_widget(child)
    
    # 为卡片绑定滚轮事件
    card.bind("<MouseWheel>", on_mousewheel, add="+")
    print(f"卡片框架已创建，pack方式: fill=tk.X, pady=10, padx=10")
    
    # 创建内容框架，左侧图片区域，右侧信息区域
    content_frame = ttk.Frame(card)
    content_frame.pack(fill=tk.X, expand=True)
    
    # 左侧图片预留区域（80x80）
    image_frame = ttk.Frame(content_frame, width=80, height=80, relief=tk.SUNKEN)
    image_frame.pack(side=tk.LEFT, padx=(0, 15))
    image_frame.pack_propagate(False)  # 防止内容改变框架大小
    
    # 图片占位提示
    image_placeholder = tk.Label(image_frame, text="图片位置", font=('SimHei', 8))
    image_placeholder.pack(expand=True)
    
    # 右侧信息区域
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 食物名称
    food_name = food_data.get('food_name', '未知食物')
    name_label = tk.Label(info_frame, text=food_name, font=('SimHei', 12, 'bold'))
    name_label.pack(anchor=tk.W, pady=(0, 5))
    print(f"名称标签已创建: {food_name}")
    
    # 创建详细信息框架，使用网格布局
    details_frame = ttk.Frame(info_frame)
    details_frame.pack(fill=tk.X, pady=(0, 5))
    
    # 基本属性 - 使用新的字段名
    properties = [
        ("饥饿值:", food_data.get('饥饿值', 0)),
        ("生命值:", food_data.get('生命值', 0)),
        ("理智值:", food_data.get('理智值', 0)),
        ("食物路径:", food_data.get('food_Route', '')),
    ]
    
    property_labels = []
    for i, (label, value) in enumerate(properties):
        label_widget = ttk.Label(details_frame, text=label, font=('SimHei', 10))
        value_widget = ttk.Label(details_frame, text=value, font=('SimHei', 10, 'bold'))
        label_widget.grid(row=i//2, column=i%2*2, sticky=tk.W, padx=(0, 5))
        value_widget.grid(row=i//2, column=i%2*2+1, sticky=tk.W, padx=(0, 20))
        property_labels.extend([label_widget, value_widget])
    
    # 备注信息
    desc_label = None
    description = food_data.get('备注', '')
    if description:
        desc_label = tk.Label(info_frame, text=f"备注: {description}", 
                             font=('SimHei', 10), wraplength=700)
        desc_label.pack(anchor=tk.W, pady=(5, 0))
    
    # 为所有卡片内的子控件手动绑定滚轮事件
    bind_wheel_to_widget(content_frame)
    bind_wheel_to_widget(image_frame)
    bind_wheel_to_widget(info_frame)
    bind_wheel_to_widget(details_frame)
    
    # 确保所有标签都绑定了滚轮事件
    for widget in property_labels:
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
    
    if desc_label:
        desc_label.bind("<MouseWheel>", on_mousewheel, add="+")
    
    print(f"所有标签已创建完成: {food_name}")
    # 返回卡片引用，方便后续绑定事件
    return card
    
    # 确保父容器的父容器（画布）可以正确滚动
    if parent.winfo_parent() and hasattr(parent, 'master'):
        # 尝试获取画布
        current = parent.master
        while current and not isinstance(current, tk.Canvas):
            if hasattr(current, 'master'):
                current = current.master
            else:
                current = None
        
        if current:
            # 更新滚动区域
            current.update_idletasks()
            current.configure(scrollregion=current.bbox("all"))
            print(f"已更新画布滚动区域: {current}")

# 物品介绍功能
def show_item_guide(parent):
    # 获取display_frame
    import 饥荒_panel
    if hasattr(饥荒_panel, 'display_frame'):
        target_frame = 饥荒_panel.display_frame
        # 清空显示容器
        clear_frame(target_frame)
        
        # 创建标题
        title_label = tk.Label(target_frame, text="饥荒物品指南", font=('SimHei', 14, 'bold'))
        title_label.pack(anchor=tk.W, padx=20, pady=(10, 20))
        
        # 创建分类标签页
        notebook = ttk.Notebook(target_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建不同类别的标签页
        survival_frame = ttk.Frame(notebook)
        tools_frame = ttk.Frame(notebook)
        weapons_frame = ttk.Frame(notebook)
        structures_frame = ttk.Frame(notebook)
        
        # 添加标签页
        notebook.add(survival_frame, text="生存物品")
        notebook.add(tools_frame, text="工具")
        notebook.add(weapons_frame, text="武器")
        notebook.add(structures_frame, text="建筑")
        
        # 在每个标签页添加内容
        add_survival_items(survival_frame)
        add_tools_items(tools_frame)
        add_weapons_items(weapons_frame)
        add_structures_items(structures_frame)

# 添加生存物品
def add_survival_items(frame):
    items = [
        {"name": "草绳", "materials": "草 x3", "usage": "制作各种工具和建筑的基础材料"},
        {"name": "火把", "materials": "草 x3 + 木头 x1 +  rope x1", "usage": "照明，驱赶怪物"},
        {"name": "背包", "materials": "草绳 x4 + 树枝 x4", "usage": "增加8格物品栏"},
        {"name": "燧石刀", "materials": "燧石 x2 + 树枝 x1", "usage": "加速采集资源"},
    ]
    
    create_items_list(frame, items)

# 添加工具物品
def add_tools_items(frame):
    items = [
        {"name": "斧头", "materials": "燧石 x1 + 树枝 x2 + 草绳 x1", "usage": "砍伐树木"},
        {"name": "镐", "materials": "燧石 x2 + 树枝 x2 + 草绳 x1", "usage": "开采矿石和石头"},
        {"name": "铲子", "materials": "燧石 x1 + 树枝 x2 + 草绳 x1", "usage": "挖掘地皮和坟墓"},
        {"name": "草叉", "materials": "树枝 x2 + 燧石 x2", "usage": "翻耕土地，种植作物"},
    ]
    
    create_items_list(frame, items)

# 添加武器物品
def add_weapons_items(frame):
    items = [
        {"name": "长矛", "materials": "树枝 x2 + 燧石 x2 + 草绳 x1", "usage": "基础近战武器，伤害34"},
        {"name": "回旋镖", "materials": "树枝 x1 + 燧石 x1 + 蜘蛛网 x1", "usage": "远程武器，可以回收"},
        {"name": "火腿棒", "materials": "熟肉 x2 + 树枝 x2", "usage": "高伤害武器，伤害59"},
        {"name": "触手钉锤", "materials": "触手 x1 + 狼牙棒 x1", "usage": "高伤害武器，伤害51"},
    ]
    
    create_items_list(frame, items)

# 添加建筑物品
def add_structures_items(frame):
    items = [
        {"name": "营火", "materials": "树枝 x3 + 草 x3 + 燧石 x1", "usage": "烹饪食物，照明，取暖"},
        {"name": "科学机器", "materials": "金子 x1 + 石头 x4 + 木头 x4", "usage": "解锁科学类物品"},
        {"name": "炼金术引擎", "materials": "科学机器 + 金子 x2 + 石头 x4 + 齿轮 x2", "usage": "解锁高级科学类物品"},
        {"name": "箱子", "materials": "木头 x3", "usage": "储存物品，12格空间"},
    ]
    
    create_items_list(frame, items)

# 创建物品列表
def create_items_list(frame, items):
    # 创建滚动条
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 创建画布
    canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=canvas.yview)
    
    # 创建内容框架
    content_frame = ttk.Frame(canvas)
    canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # 添加鼠标滚轮事件
    def on_mousewheel(event):
        # 对于Windows系统，event.delta是±120
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # 阻止事件继续传播，避免被其他控件捕获
        return "break"
    
    # 为控件及其所有子控件绑定滚轮事件
    def bind_wheel_to_widget(widget):
        """为控件及其所有子控件绑定滚轮事件"""
        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        # 递归绑定所有子控件
        for child in widget.winfo_children():
            bind_wheel_to_widget(child)
    
    # 存储创建的物品卡片
    item_frames = []
    
    # 添加物品卡片
    for item in items:
        item_frame = ttk.Frame(content_frame, padding=10, relief=tk.RAISED)
        item_frame.pack(fill=tk.X, pady=8, padx=10)
        
        name_label = tk.Label(item_frame, text=item["name"], font=('SimHei', 11, 'bold'))
        name_label.pack(anchor=tk.W, pady=(0, 3))
        
        materials_label = tk.Label(item_frame, text=f"制作材料: {item['materials']}", font=('SimHei', 10))
        materials_label.pack(anchor=tk.W, pady=(0, 3))
        
        usage_label = tk.Label(item_frame, text=f"用途: {item['usage']}", font=('SimHei', 10))
        usage_label.pack(anchor=tk.W)
        
        item_frames.append(item_frame)
    
    # 更新滚动区域
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    # 绑定配置事件
    content_frame.bind("<Configure>", on_configure)
    
    # 为所有相关组件绑定滚轮事件
    frame.bind("<MouseWheel>", on_mousewheel, add="+")
    canvas.bind("<MouseWheel>", on_mousewheel, add="+")
    content_frame.bind("<MouseWheel>", on_mousewheel, add="+")
    
    # 为所有物品卡片及其子控件绑定滚轮事件
    for item_frame in item_frames:
        bind_wheel_to_widget(item_frame)

# Mod推荐功能
def show_mod_recommendations(parent):
    # 获取display_frame
    import 饥荒_panel
    if hasattr(饥荒_panel, 'display_frame'):
        target_frame = 饥荒_panel.display_frame
        # 清空显示容器
        clear_frame(target_frame)
        
        # 创建标题
        title_label = tk.Label(target_frame, text="饥荒MOD推荐", font=('SimHei', 14, 'bold'))
        title_label.pack(anchor=tk.W, padx=20, pady=(10, 20))
        
        # 创建MOD推荐区域
        mod_frame = ttk.Frame(target_frame)
        mod_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 示例MOD数据
        mods = [
            {"name": "巨人的统治 (Reign of Giants)", "type": "DLC", 
             "description": "原版的第一个DLC，增加了新季节、新生物和新资源", 
             "rating": 4.8},
            {"name": "船难 (Shipwrecked)", "type": "DLC", 
             "description": "以热带岛屿为背景的DLC，新增了海上探索和生存元素", 
             "rating": 4.6},
            {"name": "猪镇 (Hamlet)", "type": "DLC", 
             "description": "以猪人城镇为背景的DLC，新增了城镇生活和新的生存机制", 
             "rating": 4.5},
            {"name": "全球定位系统 (Global Positional System)", "type": "实用", 
             "description": "显示玩家坐标和地图方向，方便导航", 
             "rating": 4.9},
            {"name": "神话书说 (Chinese Fable)", "type": "内容", 
             "description": "国产MOD，添加了中国神话元素和角色", 
             "rating": 4.7},
            {"name": "更多物品 (More Items)", "type": "内容", 
             "description": "增加了更多实用物品和工具", 
             "rating": 4.3},
        ]
        
        # 创建MOD列表
        for mod in mods:
            mod_card = ttk.Frame(mod_frame, padding=12, relief=tk.RAISED)
            mod_card.pack(fill=tk.X, pady=10, padx=5)
            
            # MOD名称和评分
            header_frame = ttk.Frame(mod_card)
            header_frame.pack(fill=tk.X, pady=(0, 5))
            
            name_label = tk.Label(header_frame, text=mod["name"], font=('SimHei', 11, 'bold'))
            name_label.pack(side=tk.LEFT)
            
            rating_label = tk.Label(header_frame, text=f"评分: {mod['rating']}/5", 
                                   font=('SimHei', 10), fg="green")
            rating_label.pack(side=tk.RIGHT)
            
            # MOD类型
            type_label = tk.Label(mod_card, text=f"类型: {mod['type']}", font=('SimHei', 10), fg="blue")
            type_label.pack(anchor=tk.W, pady=(0, 3))
            
            # MOD描述
            desc_label = tk.Label(mod_card, text=f"描述: {mod['description']}", 
                                font=('SimHei', 10), wraplength=600)
            desc_label.pack(anchor=tk.W)

# 辅助函数：清空框架
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# 辅助函数：显示错误消息
def show_error(message):
    messagebox.showerror("错误", message)

# 辅助函数：显示成功消息
def show_success(message):
    messagebox.showinfo("成功", message)

# 辅助函数：显示信息消息
def show_info(message):
    messagebox.showinfo("信息", message)