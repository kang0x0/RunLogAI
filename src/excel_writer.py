import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

class ExcelWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        # 调整列顺序为：文件名、公里数、时长、平均配速、日期等
        self.columns = ['Image File', 'Distance (km)', 'Duration', 'Pace', 'Date', 'Calories']
        
    def create_or_load_excel(self):
        """创建或加载Excel文件"""
        if not os.path.exists(self.output_file):
            # 创建新的Excel文件
            df = pd.DataFrame(columns=self.columns)
            df.to_excel(self.output_file, index=False)
            return True
        return False
    
    def append_to_excel(self, running_data, image_filename=None):
        """将跑步数据追加到Excel文件"""
        try:
            # 加载现有数据
            existing_df = pd.read_excel(self.output_file)
            
            # 创建新数据DataFrame，按照新的列顺序排列
            new_row = pd.DataFrame([[
                image_filename,                           # Image File
                running_data.get('distance_km'),         # Distance (km)
                running_data.get('duration'),            # Duration
                running_data.get('pace'),                # Pace
                running_data.get('date'),                # Date
                running_data.get('calories')             # Calories
            ]], columns=self.columns)
            
            # 合并数据
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            
            # 保存到Excel
            updated_df.to_excel(self.output_file, index=False)
            return True
        except Exception as e:
            print(f"写入Excel失败: {e}")
            return False
    
    def is_duplicate_record(self, image_filename):
        """检查是否为重复记录（基于文件名判断）"""
        try:
            if os.path.exists(self.output_file) and image_filename:
                df = pd.read_excel(self.output_file)
                # 检查相同文件名的记录是否已存在
                if image_filename in df['Image File'].values:
                    return True
            return False
        except Exception as e:
            print(f"检查重复记录失败: {e}")
            return False