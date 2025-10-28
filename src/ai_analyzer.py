import base64
import json
import requests
import re
import time
import logging
from config.settings import SILICONFLOW_API_KEY, OCR_MODEL, CHAT_MODEL, OCR_PROMPT, ANALYSIS_PROMPT, JSON_FORMAT_EXAMPLE

class AIAnalyzer:
    def __init__(self):
        self.api_key = SILICONFLOW_API_KEY
        self.ocr_model = OCR_MODEL
        self.chat_model = CHAT_MODEL
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        
    def encode_image(self, image_path):
        """将图像编码为base64"""
        try:
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                logging.info(f"图片编码成功，大小: {len(encoded)} 字符")
                return encoded
        except Exception as e:
            logging.error(f"图片编码失败 {image_path}: {e}")
            return None
    
    def call_ocr_model(self, image_path):
        """调用OCR模型识别图片中的文字"""
        try:
            # 编码图像
            base64_image = self.encode_image(image_path)
            if not base64_image:
                return None
            
            # 构建OCR请求载荷
            payload = {
                "model": self.ocr_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": OCR_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logging.info(f"发送OCR请求到 {self.api_url}")
            logging.info(f"使用模型: {self.ocr_model}")
            
            # 发送OCR请求
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                logging.error(f"OCR请求失败: {response.status_code} - {response.text}")
                return None
                
            # 解析OCR响应
            result = response.json()
            text_content = result['choices'][0]['message']['content']
            logging.info(f"OCR识别成功，文字长度: {len(text_content)} 字符")
            print("识别结果：", text_content)
            return text_content
            
        except requests.RequestException as e:
            logging.error(f"OCR请求失败: {e}")
            return None
        except Exception as e:
            logging.error(f"OCR处理过程出错: {e}")
            return None
    

    def extract_json_from_response(self, content):
        """从模型响应中提取JSON数据"""
        # 移除可能的代码块标记
        cleaned_content = content.strip()
        
        # 处理 ```json ... ``` 格式
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', cleaned_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 尝试直接查找第一个完整的JSON对象
            json_match = re.search(r'({.*})', cleaned_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 如果没有找到明确的JSON对象，使用整个内容
                json_str = cleaned_content
        
        # 清理JSON字符串
        json_str = json_str.strip()
        return json_str
    
    def clean_and_parse_json(self, content):
        """清理并解析JSON数据"""
        try:
            # 提取JSON部分
            json_str = self.extract_json_from_response(content)
            logging.info(f"提取的JSON字符串: {json_str}")
            
            # 解析JSON
            running_data = json.loads(json_str)
                
            return running_data
        except json.JSONDecodeError as e:
            logging.error(f"JSON解析失败: {e}")
            logging.error(f"尝试解析的内容: {content}")
            return None
        except Exception as e:
            logging.error(f"JSON处理过程出错: {e}")
            return None

    def call_chat_model(self, text_content):
        """调用对话模型分析OCR识别的文字并提取结构化信息"""
        try:
            # 构建分析提示
            # 使用 % 格式化避免花括号冲突
            analysis_prompt = ANALYSIS_PROMPT.replace("\{json_format\}", JSON_FORMAT_EXAMPLE)
            analysis_prompt = analysis_prompt.replace("\{text_content\}", text_content)
            
            # 构建对话模型请求载荷
            payload = {
                "model": self.chat_model,
                "messages": [
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                "response_format": {"type": "json_object"}
            }
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logging.info(f"发送分析请求到 {self.api_url}")
            logging.info(f"使用模型: {self.chat_model}")
            
            # 发送分析请求
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                logging.error(f"分析请求失败: {response.status_code} - {response.text}")
                return None
                
            # 解析分析响应
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("响应数据：", content)
            
            # 清理并解析JSON数据
            running_data = self.clean_and_parse_json(content)
            if running_data:
                logging.info(f"成功解析跑步数据: {running_data}")
                return running_data
            else:
                logging.error("JSON数据解析失败")
                return None
            
        except requests.RequestException as e:
            logging.error(f"分析请求失败: {e}")
            return None
        except Exception as e:
            logging.error(f"分析过程出错: {e}")
            return None
    
    def analyze_running_screenshot(self, image_path):
        """分析跑步截图并提取信息（两阶段处理）"""
        logging.info(f"开始分析跑步截图: {image_path}")
        
        # 第一阶段：OCR识别图片中的文字
        text_content = self.call_ocr_model(image_path)
        if not text_content:
            logging.error(f"OCR识别失败: {image_path}")
            return None
        
        time.sleep(3)

        # 第二阶段：使用对话模型分析OCR识别的文字并提取结构化信息
        running_data = self.call_chat_model(text_content)
        if not running_data:
            logging.error(f"结构化信息提取失败: {image_path}")
            return None
            
        logging.info(f"成功完成图片分析: {image_path}")
        return running_data