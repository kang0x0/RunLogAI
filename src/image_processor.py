import os
from PIL import Image
import logging

class ImageProcessor:
    def __init__(self, screenshots_dir):
        self.screenshots_dir = screenshots_dir
        self.supported_formats = ('.png', '.jpg', '.jpeg')
        
    def get_screenshot_files(self):
        """获取所有截图文件"""
        files = []
        for file in os.listdir(self.screenshots_dir):
            # 跳过已处理的文件
            if file.lower().endswith('_processed.jpg'):
                continue
                
            if file.lower().endswith(self.supported_formats):
                files.append(os.path.join(self.screenshots_dir, file))
        return files
    
    def preprocess_image(self, image_path, max_size=(1024, 1024)):
        """预处理图像，调整大小以减少API调用成本"""
        # 生成处理后的文件路径
        processed_path = f"{image_path}_processed.jpg"
        
        # 如果已处理的文件已存在，直接返回路径
        if os.path.exists(processed_path):
            logging.info(f"使用已存在的处理文件: {processed_path}")
            return processed_path
            
        try:
            with Image.open(image_path) as img:
                # 转换为RGB（如果是RGBA或其他模式）
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 调整图像大小
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # 保存处理后的图像
                img.save(processed_path, 'JPEG', quality=85)
                logging.info(f"创建新的处理文件: {processed_path}")
                return processed_path
        except Exception as e:
            logging.error(f"图像处理失败 {image_path}: {e}")
            return None