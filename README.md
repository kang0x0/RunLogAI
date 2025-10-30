# RunLogAI - 智能跑步日志追踪器

RunLogAI 是一个基于人工智能的跑步日志自动追踪和分析工具。它能够自动识别跑步应用截图中的关键信息，并将其整理成结构化的Excel表格，帮助您轻松管理和分析跑步数据。

## 🌟 功能特点

- **图像智能识别**：利用先进的OCR技术自动识别跑步截图中的文字信息
- **AI数据分析**：通过大语言模型智能提取结构化跑步数据
- **自动化处理**：一键批量处理多张跑步截图
- **去重机制**：自动检测并过滤重复的跑步记录
- **Excel导出**：将结构化数据导出至Excel文件便于进一步分析
- **双OCR引擎支持**：支持基于API的OCR和本地PaddleOCR两种识别方式

## 🔧 工作原理

RunLogAI采用两阶段AI处理流程：

1. **第一阶段 - OCR识别**：
   - 支持使用 `deepseek-ai/DeepSeek-OCR` 模型（通过硅基流动API）识别跑步截图中的所有文字内容
   - 也支持使用本地PaddleOCR进行文字识别
   - 将图像信息转换为可处理的文本数据

2. **第二阶段 - 数据分析**：
   - 利用 `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` 模型分析OCR识别出的文字
   - 智能提取关键跑步数据并转换为标准JSON格式
   - 包括跑步日期、距离、时间、配速和卡路里等信息

## 🚀 安装指南

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆项目代码：
   ```bash
   git clone https://github.com/yourusername/RunLogAI.git
   cd RunLogAI
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. （可选）如需使用本地PaddleOCR，安装额外依赖：
   ```bash
   pip install paddlepaddle paddleocr
   ```

4. 配置API密钥：
   - 复制 `.env_example` 文件并重命名为 `.env`
   - 编辑 `.env` 文件，添加您的硅基流动API密钥：
   ```
   SILICONFLOW_API_KEY=your_api_key_here
   ```

## 📁 目录结构

```
RunLogAI/
├── config/                 # 配置文件目录
│   ├── __init__.py         # Python包初始化文件
│   └── settings.py         # 项目配置文件
├── data/                   # 数据目录
│   └── screenshots/        # 跑步截图存放目录
├── output/                 # 输出目录
│   └── running_records.xlsx # 导出的Excel文件
├── src/                    # 源代码目录
│   ├── __init__.py         # Python包初始化文件
│   ├── main.py             # 主程序入口
│   ├── image_processor.py  # 图像处理模块
│   ├── ai_analyzer.py      # AI分析模块
│   ├── excel_writer.py     # Excel写入模块
│   ├── paddle_ocr.py       # 本地PaddleOCR封装模块
│   └── test_api.py         # API测试工具
├── .env                    # 环境变量配置文件（需要手动创建）
├── .env_example            # 环境变量配置示例文件
├── requirements.txt        # Python依赖列表
└── README.md               # 项目说明文档
```

## ⚙️ 配置说明

### API密钥配置
在 `.env` 文件中配置您的硅基流动API密钥：
```env
SILICONFLOW_API_KEY=your_actual_api_key
```

### 模型配置
项目默认使用以下模型：
- OCR模型: `deepseek-ai/DeepSeek-OCR`
- 分析模型: `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`

如需修改模型配置，请编辑 `config/settings.py` 文件。

### OCR引擎选择
项目支持两种OCR引擎：
1. 基于硅基流动API的OCR（默认）
2. 本地PaddleOCR（需要额外安装依赖）

如需使用本地PaddleOCR，在 [main.py](file:///d:/Project/RunLogAI/src/main.py#L22-L22) 中将 `AIAnalyzer()` 初始化改为 `AIAnalyzer(use_paddle_ocr=True)`

## 📖 使用方法

1. 将跑步应用截图放入 `data/screenshots/` 目录

2. 运行主程序：
   ```bash
   python src/main.py
   ```

3. 程序将自动处理所有截图，并将结果保存到 `output/running_records.xlsx`

## 📊 输出数据格式

生成的Excel文件包含以下列：

| 列名 | 描述 |
|------|------|
| Image File | 原始图片文件名 |
| Date | 跑步日期 (YYYY-MM-DD) |
| Distance (km) | 距离 (公里) |
| Duration | 跑步时长 (HH:MM:SS) |
| Pace | 平均配速 (MM:SS/km) |
| Calories | 卡路里消耗 (千卡) |

## ⚠️ 注意事项

1. 确保截图清晰，文字可辨识
2. 每张截图应包含一次完整的跑步记录
3. 程序会自动跳过重复的跑步记录（基于文件名判断）
4. 为避免API调用限制，程序在处理每张图片后会等待2秒
5. 使用API方式时需要网络连接，使用本地PaddleOCR时无需网络

## 🔍 API使用说明

本项目使用硅基流动平台提供的API服务：
- OCR识别服务
- 大语言模型分析服务

请确保您的API密钥有足够的调用额度。

## 🧪 测试工具

项目包含以下测试模块：
- `src/test_api.py` - API连接测试工具

可以使用以下命令运行测试：
```bash
python src/test_api.py
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

MIT License