import os
from dotenv import load_dotenv

load_dotenv()

# 硅基流动 API 配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
# SILICONFLOW_MODEL = "THUDM/GLM-4.1V-9B-Thinking"  # 或其他合适的多模态模型

OCR_MODEL = "deepseek-ai/DeepSeek-OCR" 
CHAT_MODEL = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B" 


# 文件路径配置
SCREENSHOTS_DIR = "data/screenshots"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "running_records.xlsx")


# Prompt 模板
OCR_PROMPT = "请描述图片的内容。"

ANALYSIS_PROMPT = """
OCR识别的图片信息：
\{text_content\}

请根据以上OCR识别出的图片信息，提取并以JSON格式返回以下信息：
1. 跑步日期 (date) - 格式 YYYY-MM-DD
2. 距离 (distance_km) - 数字，单位公里
3. 时间 (duration) - 格式 HH:MM:SS
4. 平均配速 (pace) - 格式 MM:SS/km
5. 卡路里消耗 (calories) - 数字，单位千卡

请严格按照以下JSON格式返回结果，不要包含其他内容,如果图片没有相关字段，则为null：
\{json_format\}
"""

# JSON格式示例
JSON_FORMAT_EXAMPLE = """{
  "date": "YYYY-MM-DD",
  "distance_km": 数字,
  "duration": "HH:MM:SS",
  "pace": "MM:SS/km",
  "calories": 数字
}"""