import tkinter as tk
from tkinter import ttk, font
import importlib.util
import os
import sys

class GameAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏助手")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 设置中文字体
        self.setup_fonts()
        
        # 创建主布局
        self.create_main_layout()
        
        # 初始化游戏数据
        self.games = [
            {"name": "英雄联盟", "icon": "🎮"},
            {"name": "绝地求生", "icon": "🔫"},
            {"name": "原神", "icon": "⚔️"},
            {"name": "王者荣耀", "icon": "🏆"},
            {"name": "CS2", "icon": "💥"},
            {"name": "DOTA2", "icon": "🎯"}
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
    
    def create_main_layout(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧标签栏框架
        self.left_frame = ttk.Frame(self.main_frame, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 右侧内容面板框架
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 添加分隔线
        self.separator = ttk.Separator(self.main_frame, orient=tk.VERTICAL)
        self.separator.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 5))
    
    def create_game_tabs(self):
        # 创建标签标题
        ttk.Label(self.left_frame, text="游戏列表", font=("SimHei", 12, "bold")).pack(pady=(0, 10))
        
        # 创建游戏标签按钮
        self.game_buttons = []
        for game in self.games:
            button = ttk.Button(
                self.left_frame,
                text=f"{game['icon']} {game['name']}",
                style="Game.TButton",
                command=lambda g=game: self.show_game_panel(g)
            )
            button.pack(fill=tk.X, pady=2, padx=5)
            self.game_buttons.append(button)
        
        # 配置按钮样式
        self.style = ttk.Style()
        self.style.configure("Game.TButton", font=("SimHei", 10))
        
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
        
        # 显示游戏标题
        title_frame = ttk.Frame(self.right_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame,
            text=f"{game['icon']} {game['name']}",
            font=("SimHei", 16, "bold")
        ).pack(anchor=tk.W, padx=10, pady=10)
        
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
    app = GameAssistantApp(root)
    root.mainloop()