import pymysql
import logging
from tkinter import messagebox

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MySQLHandler')

class MySQLHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None
        # 尝试使用'donot_starve_food'作为默认表名，因为这是之前错误中提到的表名
        self._table_name = 'donot_starve_food'  # 默认表名
        self._chef_dish_column = None  # 大厨菜相关列名
        self._character_effect_column = None  # 人物效果相关列名
        self._available_tables = []  # 可用的表名列表
        # 数据库连接参数
        self.db_config = {
            'host': 'localhost',  # 数据库主机
            'user': 'root',       # 数据库用户名
            'password': 'root',       # 数据库密码
            'database': 'donot_starve',  # 数据库名
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        logger.info("MySQLHandler初始化完成，数据库配置已设置")
        # 连接数据库并尝试识别正确的表名和列名
        self.connect()
        self._discover_tables_and_columns()
        self.disconnect()
    
    def connect(self):
        """建立数据库连接，不自动创建数据库"""
        try:
            logger.info(f"尝试连接数据库: {self.db_config['host']}, 数据库名: {self.db_config['database']}")
            
            # 直接尝试连接指定数据库
            self.conn = pymysql.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            logger.info("数据库连接成功")
            
            return True
        except pymysql.MySQLError as e:
            error_msg = f"数据库连接错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("数据库连接错误", error_msg)
            return False
        except Exception as e:
            error_msg = f"连接数据库时发生未知错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("数据库连接错误", error_msg)
            return False
    
    def disconnect(self):
        """关闭数据库连接"""
        try:
            logger.info("尝试关闭数据库连接")
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.conn:
                self.conn.close()
                self.conn = None
            logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"断开数据库连接时出错: {str(e)}")
    
    def _discover_tables_and_columns(self):
        """发现数据库中的表和列信息"""
        try:
            if not self.cursor:
                return
            
            # 查询数据库中所有表名
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            self._available_tables = [list(table.values())[0] for table in tables]
            logger.info(f"数据库中可用的表: {self._available_tables}")
            
            # 检查默认表名是否存在，如果不存在尝试其他可能的表名
            if self._table_name not in self._available_tables:
                for table in self._available_tables:
                    if 'food' in table.lower():
                        logger.info(f"发现食物相关表: {table}，将使用该表名")
                        self._table_name = table
                        break
            
            # 检查表是否存在
            if self._table_name:
                logger.info(f"尝试查询表 {self._table_name} 的结构")
                self.cursor.execute(f"DESCRIBE {self._table_name}")
                columns_info = self.cursor.fetchall()
                
                # 记录所有列名
                columns = [col['Field'] for col in columns_info]
                logger.info(f"表 {self._table_name} 的列名: {columns}")
                
                # 尝试找出大厨菜相关列
                for col in columns:
                    if any(keyword in col.lower() for keyword in ['chef', '大厨', 'is_chef', '是否是']):
                        self._chef_dish_column = col
                        logger.info(f"找到大厨菜相关列: {col}")
                        break
                
                # 尝试找出人物效果相关列
                for col in columns:
                    if any(keyword in col.lower() for keyword in ['character', '人物', 'effect', '效果']):
                        self._character_effect_column = col
                        logger.info(f"找到人物效果相关列: {col}")
                        break
        except Exception as e:
            logger.error(f"发现表和列信息时出错: {str(e)}")
    
    def get_food_data(self, is_chef_dish=None, character_effect=None):
        """从数据库获取食物数据，支持筛选条件"""
        logger.info(f"获取食物数据，筛选条件: is_chef_dish={is_chef_dish}, character_effect={character_effect}")
        
        try:
            # 建立数据库连接
            if not self.connect():
                logger.warning("数据库连接失败，返回模拟数据")
                # 如果连接失败，返回基本模拟数据
                return [
                    {"food_name": "浆果", "food_Route": "", "饥饿值": 9, "理智值": 0, "生命值": 0, "备注": "基础食物"},
                    {"food_name": "胡萝卜", "food_Route": "", "饥饿值": 12, "理智值": 0, "生命值": 0, "备注": "基础食物"}
                ]
            
            # 再次检查表名和列名
            self._discover_tables_and_columns()
            
            # 确保使用正确的表名
            if not self._table_name:
                logger.error("未找到可用的食物表")
                return []
            
            # 首先获取所有数据
            query = f"SELECT * FROM {self._table_name}"
            logger.info(f"执行基础查询: {query}")
            self.cursor.execute(query)
            all_foods = self.cursor.fetchall()
            logger.info(f"获取到 {len(all_foods)} 条食物数据")
            
            # 构建筛选查询
            filtered_query = f"SELECT * FROM {self._table_name} WHERE 1=1"
            params = []
            
            # 添加大厨菜筛选条件 - 这是修复的核心部分
            if is_chef_dish is not None:
                # 记录接收到的参数值
                logger.info(f"接收到的大厨菜筛选值: {is_chef_dish}")
                
                # 尝试直接使用数据库中实际存在的列名
                if self._chef_dish_column:
                    filtered_query += f" AND {self._chef_dish_column} = %s"
                    params.append(is_chef_dish)
                    logger.info(f"使用已识别的列 {self._chef_dish_column} 进行大厨菜筛选")
                else:
                    # 尝试所有可能的列名
                    found_valid_column = False
                    possible_columns = ['is_chef_dish', 'chef_dish', '是否是大厨菜', 'is_chef', 'chef', '是否是']
                    
                    # 首先尝试直接使用列名进行查询
                    for col_name in possible_columns:
                        try:
                            # 测试列是否存在
                            test_query = f"SELECT COUNT(*) FROM {self._table_name} WHERE {col_name} IS NOT NULL LIMIT 1"
                            self.cursor.execute(test_query)
                            
                            # 如果测试通过，应用筛选条件
                            filtered_query += f" AND {col_name} = %s"
                            params.append(is_chef_dish)
                            logger.info(f"找到有效的大厨菜列 {col_name}，应用筛选条件")
                            found_valid_column = True
                            self._chef_dish_column = col_name
                            break
                        except Exception as e:
                            logger.info(f"尝试列 {col_name} 失败: {str(e)}")
                    
                    if not found_valid_column:
                        logger.warning("未找到有效的大厨菜列，将对所有数据进行客户端筛选")
            
            # 添加人物效果筛选条件
            if character_effect and character_effect != "所有":
                if self._character_effect_column:
                    filtered_query += f" AND {self._character_effect_column} = %s"
                    params.append(character_effect)
                    logger.info(f"使用已识别的列 {self._character_effect_column} 进行人物效果筛选")
                else:
                    # 尝试常见的列名
                    for possible_col in ['character_effect', '人物特殊效果']:
                        try:
                            test_query = f"SELECT COUNT(*) FROM {self._table_name} WHERE {possible_col} IS NOT NULL LIMIT 1"
                            self.cursor.execute(test_query)
                            filtered_query += f" AND {possible_col} = %s"
                            params.append(character_effect)
                            logger.info(f"找到有效的人物效果列 {possible_col}")
                            self._character_effect_column = possible_col
                            break
                        except Exception as e:
                            logger.info(f"尝试列 {possible_col} 失败: {str(e)}")
            
            # 执行筛选查询
            logger.info(f"执行筛选查询: {filtered_query}, 参数: {params}")
            self.cursor.execute(filtered_query, params)
            filtered_foods = self.cursor.fetchall()
            logger.info(f"筛选查询返回 {len(filtered_foods)} 条数据")
            
            # 如果筛选没有结果但有筛选条件，执行客户端筛选
            if not filtered_foods and params and len(all_foods) > 0:
                logger.warning("SQL筛选未返回数据，尝试客户端筛选")
                filtered_foods = []
                
                # 对所有数据进行客户端筛选
                for food in all_foods:
                    match = True
                    
                    # 客户端大厨菜筛选
                    if is_chef_dish is not None:
                        found_chef_value = False
                        # 尝试所有可能的字段名
                        for key in ['is_chef_dish', 'chef_dish', '是否是大厨菜', 'is_chef', 'chef']:
                            if key in food and str(food[key]).upper() == str(is_chef_dish).upper():
                                found_chef_value = True
                                break
                        if not found_chef_value:
                            match = False
                    
                    # 客户端人物效果筛选
                    if match and character_effect and character_effect != "所有":
                        found_effect = False
                        for key in ['character_effect', '人物特殊效果']:
                            if key in food and str(food[key]) == str(character_effect):
                                found_effect = True
                                break
                        if not found_effect:
                            match = False
                    
                    if match:
                        filtered_foods.append(food)
                
                logger.info(f"客户端筛选返回 {len(filtered_foods)} 条数据")
            
            # 处理结果数据
            results = []
            for item in filtered_foods:
                # 创建标准化的食物数据字典
                food_data = {
                    'food_name': item.get('food_name', item.get('name', item.get('食物名称', '未知食物'))),
                    # 从数据库获取实际的食物路径
                    'food_Route': item.get('food_Route', ''),
                    '饥饿值': item.get('hunger', item.get('hunger_value', item.get('饥饿值', 0))),
                    '理智值': item.get('sanity', item.get('sanity_value', item.get('理智值', 0))),
                    '生命值': item.get('health', item.get('health_value', item.get('生命值', 0))),
                    '备注': item.get('description', item.get('备注', ''))
                }
                results.append(food_data)
            
            return results
        except pymysql.MySQLError as e:
            error_msg = f"数据库查询错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("查询错误", error_msg)
            # 发生错误时返回基本模拟数据
            return [
                {"food_name": "浆果", "food_Route": "", "饥饿值": 9, "理智值": 0, "生命值": 0, "备注": "基础食物"},
                {"food_name": "胡萝卜", "food_Route": "", "饥饿值": 12, "理智值": 0, "生命值": 0, "备注": "基础食物"}
            ]
        except Exception as e:
            error_msg = f"获取数据时发生未知错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("查询错误", error_msg)
            return [
                {"food_name": "浆果", "food_Route": "", "饥饿值": 9, "理智值": 0, "生命值": 0, "备注": "基础食物"},
                {"food_name": "胡萝卜", "food_Route": "", "饥饿值": 12, "理智值": 0, "生命值": 0, "备注": "基础食物"}
            ]
        finally:
            # 无论如何都要断开连接
            self.disconnect()
    
    def get_distinct_character_effects(self):
        """从数据库获取所有不同的人物特殊效果"""
        try:
            logger.info("获取所有不同的人物特殊效果")
            # 建立数据库连接
            if not self.connect():
                logger.warning("数据库连接失败，返回预定义的特效列表")
                # 如果连接失败，返回预定义的特效列表
                return ["沃尔夫冈伤害提升", "温蒂伤害提升", "薇洛生命恢复", "机器人属性加成"]
            
            # 检查food表是否存在
            try:
                self.cursor.execute("SHOW TABLES LIKE 'food'")
                if not self.cursor.fetchone():
                    logger.error("数据库中不存在food表")
                    # 创建表并插入示例数据
                    self._create_food_table_and_insert_data()
            except Exception as e:
                logger.error(f"检查表是否存在时出错: {str(e)}")
            
            # 执行查询获取所有不同的特效
            query = "SELECT DISTINCT character_effect FROM food WHERE character_effect != '' AND character_effect IS NOT NULL"
            logger.info(f"执行查询: {query}")
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            # 提取特效值并去重
            effects = [result['character_effect'] for result in results if result['character_effect']]
            # 去除空字符串并返回唯一值
            distinct_effects = list(set(effects))
            logger.info(f"获取到特效列表: {distinct_effects}")
            
            # 如果没有特效，返回预定义的特效列表
            if not distinct_effects:
                logger.warning("未获取到特效数据，返回预定义列表")
                return ["沃尔夫冈伤害提升", "温蒂伤害提升", "薇洛生命恢复", "机器人属性加成"]
            
            return distinct_effects
        except pymysql.MySQLError as e:
            error_msg = f"数据库查询错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("查询错误", error_msg)
            # 发生错误时返回预定义的特效列表
            return ["沃尔夫冈伤害提升", "温蒂伤害提升", "薇洛生命恢复", "机器人属性加成"]
        except Exception as e:
            error_msg = f"获取特效列表时发生未知错误: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("查询错误", error_msg)
            return ["沃尔夫冈伤害提升", "温蒂伤害提升", "薇洛生命恢复", "机器人属性加成"]
        finally:
            # 无论如何都要断开连接
            self.disconnect()