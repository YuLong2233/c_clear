# 🧹 Windows C 盘深度清理工具 (C Drive Deep Cleaner)

一款基于 Python 和 CustomTkinter 构建的现代化、高性能 C 盘深度清理工具。旨在为普通用户提供一个直观、简单且高效的系统清理方案。

![Language](https://img.shields.io/badge/Language-Python-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![UI](https://img.shields.io/badge/UI-CustomTkinter-orange)

---

## ✨ 核心特性

- **🚀 深度清理**：涵盖 8 大核心清理项，包括系统临时文件、Windows 更新缓存、浏览器缓存、回收站等。
- **🎨 现代化 UI**：采用最新的 CustomTkinter 框架，支持深色模式，界面简洁高级。
- **🌐 多语言支持**：原生支持中英文双语切换，满足不同用户需求。
- **🛡️ 安全可靠**：纯 Python 逻辑实现，无流氓插件，透明化清理过程。
- **📏 高度兼容**：自动请求管理员权限，确保拥有清理核心系统目录的权限。
- **📦 单文件运行**：通过打包脚本可生成独立的 `.exe` 文件，无需安装 Python 环境即可运行。

## 🔍 清理项目

1. **用户临时文件**：清理 `%TEMP%` 及本地应用临时目录。
2. **系统临时文件**：清理 Windows 临时文件夹及预读取 (Prefetch) 文件。
3. **Windows 更新缓存**：清理 SoftwareDistribution 下载目录（自动处理服务启停）。
4. **浏览器缓存**：支持 Chrome、Edge 和 Firefox 浏览器的缓存清理。
5. **系统日志**：清理 CBS、DISM 及 IIS 等过期日志。
6. **回收站**：一键清空所有驱动器的回收站。
7. **其他缓存**：包括错误报告、DirectX 着色器缓存、npm/pip 缓存等。
8. **系统磁盘清理**：可选调用 Windows 自带的 `cleanmgr.exe` 进行额外处理。

## 🛠️ 如何使用

### 1. 开发运行
如果你已安装 Python 环境：
```bash
# 1. 克隆/下载项目到本地
# 2. 安装依赖
pip install -r requirements.txt
# 3. 运行应用
python app/main.py
```

### 2. 打包为 EXE
直接在项目根目录下双击运行 `build.bat`，打包完成后，可在 `dist` 文件夹中找到生成的 `Windows_Cleaner.exe`。

## 📂 项目结构

```text
.
├── app/                # 源代码目录
│   ├── main.py         # 程序入口
│   ├── ui.py           # UI 界面布局
│   ├── cleaner.py      # 驱动清理核心逻辑
│   ├── i18n.py         # 中英文语言包
│   └── utils.py        # 磁盘信息与权限工具
├── assets/             # 资源文件 (图标等)
├── requirements.txt    # 项目依赖
├── build.bat           # 一键打包脚本
└── .gitignore          # Git 忽略配置
```

## 🤝 贡献与反馈

如果您有任何好的建议或发现了 Bug，欢迎提交 Issue 或 Pull Request。

- **GitHub**: [您的项目地址]
- **更多软件**: [您的个人网站地址]

---

*注意：请务必以管理员权限运行此工具以获得最佳清理效果。*
