# src/paddle_ocr.py
import logging
import os
import sys
import argparse

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from paddleocr import PaddleOCR
    PADDLE_OCR_AVAILABLE = True
except ImportError:
    PADDLE_OCR_AVAILABLE = False
    print("警告: 未安装 PaddleOCR，相关功能不可用")
    print("请运行 'pip install paddlepaddle paddleocr' 安装")

class PaddleOCRWrapper:
    def __init__(self):
        """
        初始化 PaddleOCR 实例
        """
        if not PADDLE_OCR_AVAILABLE:
            self.ocr_engine = None
            return
            
        try:
            # 在初始化前保存当前日志级别
            original_level = logging.root.level
            # 初始化 PaddleOCR，使用文档优化参数
            self.ocr_engine = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
                lang="ch"
            )
            # 恢复原来的日志级别
            logging.root.setLevel(original_level)
            logging.info("PaddleOCR 初始化成功")
        except Exception as e:
            logging.error(f"PaddleOCR 初始化失败: {e}")
            self.ocr_engine = None

    def recognize_text(self, image_path):
        """
        使用 PaddleOCR 识别图片中的文字
        
        Args:
            image_path (str): 图片文件路径 或 URL
            
        Returns:
            str: 识别出的文字内容，如果失败则返回 None
        """
        if not PADDLE_OCR_AVAILABLE or not self.ocr_engine:
            logging.error("PaddleOCR 不可用")
            return None

        try:
            # 如果是本地文件，检查文件是否存在
            if not image_path.startswith('http'):
                if not os.path.exists(image_path):
                    logging.error(f"图片文件不存在: {image_path}")
                    return None

            # 执行 OCR 识别
            result = self.ocr_engine.predict(input=image_path)
            
            # 提取文字内容
            text_results = []
            for res in result:
                # 保存结果到图像和JSON文件
                # res.save_to_img("output")
                # res.save_to_json("output")
                
                # 打印结果
                # res.print()
                
                # 提取文本内容 - 使用 rec_texts 而不是 boxes
                if hasattr(res, 'rec_texts'):
                    text_results.extend(res.rec_texts)
                elif isinstance(res, dict) and 'rec_texts' in res:
                    text_results.extend(res['rec_texts'])
            
            # 将所有识别出的文字拼接成一个字符串
            full_text = "\n".join(text_results)
            logging.info(f"PaddleOCR 识别成功，文字长度: {len(full_text)} 字符")
            return full_text
            
        except Exception as e:
            logging.error(f"PaddleOCR 识别失败 {image_path}: {e}")
            return None


def test_paddle_ocr(image_path):
    """测试 PaddleOCR 功能"""
    print(f"测试 PaddleOCR 功能: {image_path}")
    
    # 检查文件是否存在（如果是本地文件）
    if not image_path.startswith('http') and not os.path.exists(image_path):
        print(f"错误: 图片文件不存在 {image_path}")
        return False
    
    # 初始化 PaddleOCR
    paddle_ocr = PaddleOCRWrapper()
    if not paddle_ocr.ocr_engine:
        print("错误: PaddleOCR 初始化失败")
        return False
    
    # 执行 OCR 识别
    print("正在执行 OCR 识别...")
    text_content = paddle_ocr.recognize_text(image_path)
    
    if text_content:
        print("OCR 识别成功!")
        print(f"识别结果: {text_content}")
        return True
    else:
        print("OCR 识别失败!")
        return False


def main():
    """主测试函数"""
    parser = argparse.ArgumentParser(description="PaddleOCR 测试工具")
    parser.add_argument("image_path", nargs="?", help="要识别的图片路径")
    args = parser.parse_args()
    
    if not args.image_path:
        print("用法: python src/paddle_ocr.py <图片路径>")
        return
    
    print("RunLogAI - PaddleOCR 测试工具")
    print("=" * 40)
    
    test_paddle_ocr(args.image_path)


if __name__ == "__main__":
    main()