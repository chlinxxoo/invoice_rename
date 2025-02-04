# 发票重命名工具 (Invoice Rename Tool)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

一个用于处理电子发票PDF文件的Python工具，支持自动提取文本、重命名文件和计算总金额。支持 Windows 和 macOS 系统。

## ✨ 功能特点

- 📄 自动处理目录下的所有PDF发票文件
- 🔄 智能重命名PDF文件（格式：发票号-公司名-日期-类型-金额）
- 📊 支持导出发票文本内容
- 💰 自动计算发票总金额
- ⚡ 支持批量处理
- 🛡️ 完善的错误处理机制
- 🖥️ 支持 Windows 和 macOS 系统

## 🚀 快速开始

### 环境要求

- Python 3.6 或更高版本
- pip 包管理器
- Windows 或 macOS 系统

### 安装

1. 克隆仓库：
```bash
git clone https://github.com/chlinxxoo/invoice_rename.git
cd invoice_rename
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 💻 使用方法

### 方式一：Python脚本

```bash
python extract_invoice.py [--pdfFolder 发票文件夹路径] [--dumpTxt] [--dumpTotalCount]
```

参数说明：
- `--pdfFolder`：必填，指定PDF发票文件所在的文件夹路径
- `--dumpTxt`：可选，输出PDF文件的完整文本内容
- `--dumpTotalCount`：可选，计算并输出所有发票的总金额

### 方式二：可执行文件

1. 生成可执行文件：
```bash
python build_exe.py
```

2. 运行生成的可执行文件：

Windows:
```bash
dist/发票处理工具.exe [--pdfFolder 发票文件夹路径] [--dumpTxt] [--dumpTotalCount]
```

macOS:
```bash
dist/发票处理工具 [--pdfFolder 发票文件夹路径] [--dumpTxt] [--dumpTotalCount]
```

## 📝 示例

处理指定文件夹下的所有发票并计算总金额：
```bash
# Python脚本方式
python extract_invoice.py --pdfFolder ./发票文件夹 --dumpTotalCount

# 可执行文件方式（macOS）
./dist/发票处理工具 --pdfFolder ./发票文件夹 --dumpTotalCount

# 可执行文件方式（Windows）
dist/发票处理工具.exe --pdfFolder ./发票文件夹 --dumpTotalCount
```

## 🤝 贡献

欢迎提交问题和改进建议！如果你想贡献代码：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 📄 许可证

该项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔍 注意事项

- 确保PDF文件可以正常打开和读取
- 对于大型PDF文件，处理可能需要较长时间
- 建议定期备份重要的发票文件
- macOS用户首次运行可能需要添加执行权限：`chmod +x dist/发票处理工具`
