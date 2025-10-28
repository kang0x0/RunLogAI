import os
import sys
import base64
import json
import time
import requests
from dotenv import load_dotenv

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from config.settings import SILICONFLOW_API_KEY, OCR_MODEL, CHAT_MODEL, OCR_PROMPT, ANALYSIS_PROMPT, JSON_FORMAT_EXAMPLE

def test_api_connection():
    """测试硅基流动API连接"""
    print("测试硅基流动API连接...")
    
    # 检查API密钥
    if not SILICONFLOW_API_KEY:
        print("错误: 未找到API密钥，请检查.env文件")
        return False
    
    print(f"OCR模型: {OCR_MODEL}")
    print(f"对话模型: {CHAT_MODEL}")
    
    # 测试简单文本请求
    try:
        payload = {
            "model": CHAT_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "你好，请回复'API连接成功'来确认连接正常"
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        
        api_url = "https://api.siliconflow.cn/v1/chat/completions"
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("API连接成功!")
            print(f"响应内容: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"API连接失败，状态码: {response.status_code}")
            print(f"错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"测试过程中出现异常: {e}")
        return False

def test_image_encoding(image_path):
    """测试图片编码"""
    if not os.path.exists(image_path):
        print(f"图片文件不存在: {image_path}")
        return None
        
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            print(f"图片编码成功，长度: {len(encoded)} 字符")
            return encoded
    except Exception as e:
        print(f"图片编码失败: {e}")
        return None

def test_ocr_api_call(image_path):
    """测试OCR API调用"""
    print(f"测试OCR API调用: {image_path}")
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 图片文件不存在 {image_path}")
        return False
    
    # 编码图片
    encoded_image = test_image_encoding(image_path)
    if not encoded_image:
        return False
    
    # 发送OCR API请求
    try:
        payload = {
            "model": OCR_MODEL,
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
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        
        api_url = "https://api.siliconflow.cn/v1/chat/completions"
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("OCR API调用成功!")
            print(f"OCR识别结果: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"OCR API调用失败，状态码: {response.status_code}")
            print(f"错误详情: {response.text}")
            return False
            
    except Exception as e:
        print(f"OCR API测试过程中出现异常: {e}")
        return False

def test_two_stage_analysis(image_path):
    """测试两阶段分析流程"""
    print(f"测试两阶段分析流程: {image_path}")
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 图片文件不存在 {image_path}")
        return False
    
    # 第一阶段：OCR识别
    print("第一阶段：OCR识别...")
    encoded_image = test_image_encoding(image_path)
    if not encoded_image:
        return False
    
    try:
        ocr_payload = {
            "model": OCR_MODEL,
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
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        
        api_url = "https://api.siliconflow.cn/v1/chat/completions"
        ocr_response = requests.post(api_url, headers=headers, json=ocr_payload)
        
        if ocr_response.status_code != 200:
            print(f"OCR调用失败，状态码: {ocr_response.status_code}")
            print(f"错误详情: {ocr_response.text}")
            return False
            
        ocr_result = ocr_response.json()
        text_content = ocr_result['choices'][0]['message']['content']
        print(f"OCR识别成功，文字长度: {len(text_content)} 字符")
        print(f"OCR识别结果: {text_content}")
        
        time.sleep(3)  # 可选：等待一段时间以防止速率限制
        # 第二阶段：对话模型分析
        print("第二阶段：对话模型分析...")
        # 使用安全的字符串替换方式
        analysis_prompt = ANALYSIS_PROMPT.replace("\{json_format\}", JSON_FORMAT_EXAMPLE)
        analysis_prompt = analysis_prompt.replace("\{text_content\}", text_content)

        print(f"分析提示: {analysis_prompt}")
        analysis_payload = {
            "model": CHAT_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            "response_format": {"type": "json_object"}
        }
        
        analysis_response = requests.post(api_url, headers=headers, json=analysis_payload)
        
        if analysis_response.status_code == 200:
            analysis_result = analysis_response.json()
            print("两阶段分析成功!")
            print(f"结构化数据: {analysis_result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"分析调用失败，状态码: {analysis_response.status_code}")
            print(f"错误详情: {analysis_response.text}")
            return False
            
    except Exception as e:
        print(f"两阶段分析过程中出现异常: {e}")
        return False

def main():
    """主测试函数"""
    print("Runflow AI Tracker - API测试工具")
    print("=" * 40)
    
    # 测试API连接
    # if not test_api_connection():
    #     return
    
    # 如果提供了图片参数，则测试图片处理流程
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        # print("\n" + "=" * 40)
        
        # 测试OCR
        # print("1. 测试OCR功能")
        # test_ocr_api_call(image_path)
        
        print("\n" + "-" * 40)
        
        # 测试两阶段分析
        print("2. 测试两阶段分析流程")
        test_two_stage_analysis(image_path)

if __name__ == "__main__":
    main()