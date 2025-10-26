import tkinter as tk
from tkinter import ttk, font
import importlib.util
import os
import sys
from tkinter import Canvas

class GameAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏助手")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # 设置中文字体
        self.setup_fonts()
        
        # 创建样式
        self.style = ttk.Style()
        
        # 添加渐变背景
        self.create_gradient_background()
        
        # 创建主布局
        self.create_main_layout()
        
        # 初始化游戏数据，添加颜色属性
        self.games = [
            {"name": "英雄联盟", "icon": "🎮", "color": "#4B7BEC"},
            {"name": "绝地求生", "icon": "🔫", "color": "#FF6B6B"},
            {"name": "原神", "icon": "⚔️", "color": "#4ECDC4"},
            {"name": "王者荣耀", "icon": "🏆", "color": "#FFD166"},
            {"name": "CS2", "icon": "💥", "color": "#06D6A0"},
            {"name": "DOTA2", "icon": "🎯", "color": "#118AB2"}
        ]
        
        # 创建左侧标签栏
        self.create_game_tabs()
        
        # 加载游戏模块
        self.game_modules = {}
        self.load_game_modules()
        
        # 默认显示第一个游戏
        if self.games:
            self.show_game_panel(self.games[0])
    
    def setup_fonts(self):
        # 设置中文字体，确保中文正常显示
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="SimHei", size=10)
        text_font = font.nametofont("TkTextFont")
        text_font.configure(family="SimHei", size=10)
    
    def create_gradient_background(self):
        # 创建画布作为背景
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定尺寸变化事件，更新渐变背景
        self.root.bind("<Configure>", self.update_gradient)
        
        # 初始绘制渐变
        self.update_gradient(None)
    
    def update_gradient(self, event):
        # 创建从浅蓝色到深蓝色的渐变背景
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # 确保窗口尺寸有效
        if width <= 1 or height <= 1:
            return
        
        # 清空画布
        self.canvas.delete("gradient")
        
        # 绘制渐变
        r1, g1, b1 = 220, 230, 255  # 浅蓝色
        r2, g2, b2 = 100, 149, 237  # 深蓝色
        
        # 优化：每10像素绘制一条，提高性能
        for y in range(0, height, 10):
            # 线性插值计算RGB值
            r = int(r1 + (r2 - r1) * y / height)
            g = int(g1 + (g2 - g1) * y / height)
            b = int(b1 + (b2 - b1) * y / height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # 绘制水平条
            self.canvas.create_line(0, y, width, y, fill=color, tags="gradient")
        
        # 确保画布在底层
        self.canvas.lower("gradient")
    
    def create_main_layout(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧标签栏框架，增大宽度
        self.left_frame = ttk.Frame(self.main_frame, width=250)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 右侧内容面板框架
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 添加分隔线
        self.separator = ttk.Separator(self.main_frame, orient=tk.VERTICAL)
        self.separator.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 5))
    
    def create_game_tabs(self):
        # 创建标签标题，使用更大的字体
        title_label = ttk.Label(self.left_frame, text="游戏列表", font=("SimHei", 14, "bold"))
        title_label.pack(pady=(0, 15))
        
        # 创建游戏标签按钮
        self.game_buttons = []
        
        # 为每个游戏创建独特的按钮样式
        for i, game in enumerate(self.games):
            # 创建自定义按钮样式
            button_style = f"Game.TButton{i}"
            
            # 在Windows上，ttk按钮的样式限制较多，这里使用一种简化方法
            if sys.platform.startswith("win"):
                # 在Windows上使用默认样式，但增加字体大小和内边距
                self.style.configure(
                    button_style,
                    font=("SimHei", 12, "bold"),
                    padding=15
                )
                
                # 创建按钮
                button = tk.Button(
                    self.left_frame,
                    text=f"{game['icon']} {game['name']}",
                    font=("SimHei", 12, "bold"),
                    bg=game['color'],
                    fg="white",
                    height=2,
                    relief=tk.RAISED,
                    command=lambda g=game: self.show_game_panel(g)
                )
            else:
                # 在其他平台上使用ttk样式
                self.style.configure(
                    button_style,
                    font=("SimHei", 12, "bold"),
                    padding=15,
                    background=game['color'],
                    foreground="white"
                )
                
                # 创建按钮
                button = ttk.Button(
                    self.left_frame,
                    text=f"{game['icon']} {game['name']}",
                    style=button_style,
                    command=lambda g=game: self.show_game_panel(g)
                )
            
            button.pack(fill=tk.X, pady=5, padx=8)
            self.game_buttons.append(button)
        
        # 添加滚动条（如果游戏列表很长）
        self.left_scrollbar = ttk.Scrollbar(self.left_frame)
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_game_modules(self):
        # 加载各个游戏的模块
        for game in self.games:
            game_name = game["name"]
            module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), game_name, f"{game_name}_panel.py")
            
            if os.path.exists(module_path):
                # 动态导入模块
                spec = importlib.util.spec_from_file_location(f"{game_name}_module", module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"{game_name}_module"] = module
                spec.loader.exec_module(module)
                self.game_modules[game_name] = module
            else:
                print(f"警告: 未找到游戏模块 {module_path}")
    
    def show_game_panel(self, game):
        # 清空右侧面板
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        
        # 显示游戏标题，使用更大的字体和游戏特定颜色
        title_frame = ttk.Frame(self.right_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 创建带有游戏颜色的标题标签
        title_label = tk.Label(
            title_frame,
            text=f"{game['icon']} {game['name']}",
            font=("SimHei", 18, "bold"),
            fg=game.get('color', '#000000')
        )
        title_label.pack(anchor=tk.W, padx=20, pady=15)
        
        # 检查是否有对应的游戏模块
        game_name = game["name"]
        if game_name in self.game_modules:
            try:
                # 调用模块中的show_panel函数
                if hasattr(self.game_modules[game_name], "show_panel"):
                    self.game_modules[game_name].show_panel(self.right_frame, game)
                else:
                    ttk.Label(
                        self.right_frame,
                        text="游戏模块未实现show_panel函数",
                        font=("SimHei", 10)
                    ).pack(anchor=tk.W, padx=20, pady=10)
            except Exception as e:
                ttk.Label(
                    self.right_frame,
                    text=f"加载游戏模块出错: {str(e)}",
                    font=("SimHei", 10)
                ).pack(anchor=tk.W, padx=20, pady=10)
        else:
            # 如果没有找到模块，显示默认内容
            ttk.Label(
                self.right_frame,
                text="该游戏模块尚未实现",
                font=("SimHei", 10)
            ).pack(anchor=tk.W, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    # 运行应用
    app = GameAssistantApp(root)
    root.mainloop()