# EXE Packager - Python转EXE打包工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

## 项目简介

EXE Packager是一个基于PyInstaller的图形化Python转EXE打包工具，可以将Python脚本打包成独立的Windows可执行文件(.exe)。该工具提供直观的图形界面，让用户无需掌握复杂的命令行操作即可轻松完成Python程序的打包工作。

## 功能特性

- 🖥️ 图形化界面操作，简单易用
- 📦 支持单文件打包模式（--onefile）
- 🖼️ 支持窗口模式运行（--windowed）
- 🎨 支持自定义图标
- 📁 支持指定输出目录
- 📋 实时打包日志显示
- 🛠️ 基于PyInstaller，兼容性好

## 安装依赖

在使用本工具之前，请确保已安装以下依赖：

```bash
pip install pyinstaller
```

## 使用方法

### 方法一：直接运行源代码

1. 克隆或下载本项目
2. 安装依赖：`pip install pyinstaller`
3. 运行工具：`python exe_packager.py`

### 方法二：打包为exe后使用

1. 使用本工具将`exe_packager.py`打包为exe文件
2. 直接运行生成的exe文件即可使用

## 使用说明

1. 选择要打包的Python脚本文件
2. 选择输出目录（默认为脚本所在目录）
3. 设置打包选项：
   - 单文件模式：将所有依赖打包到一个exe文件中
   - 窗口模式：运行时不显示控制台窗口
   - 图标文件：为exe文件设置自定义图标
4. 点击"开始打包"按钮
5. 等待打包完成，生成的exe文件会保存在指定的输出目录中

## 项目结构

```
EXE_Packager_Source/
├── exe_packager.py     # 主程序文件
├── README.md           # 项目说明文件
├── LICENSE             # 开源许可证
├── requirements.txt    # 依赖列表
└── setup.py            # 安装配置文件
```

## 许可证

本项目采用MIT许可证，详情请见[LICENSE](LICENSE)文件。

## 免责声明

本工具仅供学习和研究使用，不得用于任何商业用途或非法用途。使用本工具造成的任何后果由使用者自行承担。