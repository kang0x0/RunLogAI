import os
import sys
import time
import logging

# 获取当前文件所在目录，然后添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from config.settings import SCREENSHOTS_DIR, OUTPUT_DIR, OUTPUT_FILE
from src.image_processor import ImageProcessor
from src.ai_analyzer import AIAnalyzer
from src.excel_writer import ExcelWriter

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directories():
    """创建必要的目录"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_running_screenshots():
    """主处理流程"""
    # 初始化组件
    image_processor = ImageProcessor(SCREENSHOTS_DIR)
    ai_analyzer = AIAnalyzer()
    excel_writer = ExcelWriter(OUTPUT_FILE)
    
    # 创建或加载Excel文件
    excel_writer.create_or_load_excel()
    
    # 获取截图文件
    screenshot_files = image_processor.get_screenshot_files()
    
    if not screenshot_files:
        logging.info("未找到截图文件，请将跑步截图放入 data/screenshots 目录")
        return
    
    logging.info(f"找到 {len(screenshot_files)} 个截图文件")
    
    # 处理每个截图
    for screenshot_path in screenshot_files:
        logging.info(f"处理文件: {screenshot_path}")
        
        # 预处理图像
        processed_image = image_processor.preprocess_image(screenshot_path)
        if not processed_image:
            logging.error(f"图像处理失败: {screenshot_path}")
            continue
        
        # AI分析
        running_data = ai_analyzer.analyze_running_screenshot(processed_image)
        if not running_data:
            logging.error(f"AI分析失败: {screenshot_path}")
            continue
        
        # 检查是否为重复记录
        if excel_writer.is_duplicate_record(running_data):
            logging.warning(f"发现重复记录，跳过: {running_data.get('date')}")
            continue

        # 提取图片文件名（不含路径）
        image_filename = os.path.basename(screenshot_path)
        
        # 写入Excel
        if excel_writer.append_to_excel(running_data, image_filename):
            logging.info(f"成功添加记录: {running_data.get('date')} (来自 {image_filename})")
        else:
            logging.error(f"写入Excel失败: {screenshot_path}")
        
        time.sleep(2)  # 避免请求过快

def main():
    """主函数"""
    logging.info("Runflow AI Tracker 启动")
    
    # 创建必要目录
    setup_directories()
    
    # 处理跑步截图
    process_running_screenshots()
    
    logging.info("处理完成")

if __name__ == "__main__":
    main()