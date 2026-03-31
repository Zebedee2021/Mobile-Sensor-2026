# 手机传感器技术

> 智能手机内置传感器 —— 原理、硬件与编程实践

[![Deploy](https://github.com/Zebedee2021/Mobile-Sensor-2026/actions/workflows/deploy.yml/badge.svg)](https://github.com/Zebedee2021/Mobile-Sensor-2026/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://zebedee2021.github.io/Mobile-Sensor-2026/)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zebedee2021/Mobile-Sensor-2026/blob/main/notebooks/sensor_demo.ipynb)

**在线阅读** :point_right: <https://zebedee2021.github.io/Mobile-Sensor-2026/>

---

## 项目简介

本站是一份面向高校教学的智能手机传感器技术文档，采用 **MkDocs + Material** 主题、**Docs-as-Code** 工作流构建，涵盖从硬件原理到编程实践的完整知识体系。全站中文撰写，配有 **32 张中文标注技术插图**，图文并茂。

## 内容结构

```
docs/
├── index.md                  # 首页
├── sensors/
│   ├── overview.md           # 传感器总览 (发展史·分类·MEMS·融合)
│   ├── motion/               # 运动类传感器
│   │   ├── accelerometer.md  #   加速度计 (MEMS 电容式)
│   │   ├── gyroscope.md      #   陀螺仪 (科氏力)
│   │   └── magnetometer.md   #   磁力计 (霍尔/AMR/TMR)
│   ├── environment/          # 环境类传感器
│   │   ├── barometer.md      #   气压计 (MEMS 压阻/电容)
│   │   ├── light.md          #   环境光传感器
│   │   └── temperature.md    #   温湿度传感器
│   ├── position/             # 位置与距离
│   │   ├── gnss.md           #   GNSS 定位 (多星座·双频·AGNSS)
│   │   ├── proximity.md      #   接近传感器
│   │   └── tof-lidar.md      #   ToF 与 LiDAR
│   ├── biometric/            # 生物识别
│   │   ├── fingerprint.md    #   指纹传感器 (电容/光学/超声波)
│   │   ├── face.md           #   面部识别 (结构光·TrueDepth)
│   │   └── health.md         #   心率与血氧 (PPG·SpO2)
│   └── others/               # 通信与其他
│       ├── nfc.md            #   NFC (近场通信)
│       ├── uwb.md            #   UWB (超宽带)
│       └── hall-ir.md        #   霍尔传感器与红外发射器
├── programming/              # 编程接口
│   ├── android.md            #   Android 传感器 API (Kotlin)
│   └── ios.md                #   iOS Core Motion (Swift)
└── practice/                 # 实验实践
    ├── sensorlog.md          #   SensorLog 使用指南
    ├── sensor-logger.md      #   Sensor Logger 使用指南 (数据上云)
    └── data-collection.md    #   数据采集实验 (计步器·指南针·气压楼层·手势识别)

notebooks/
└── sensor_demo.ipynb         # Python 演示程序集 (Colab 直接运行)
```

## 涵盖的传感器

| 类别 | 传感器 | 核心技术 |
|:-----|:-------|:---------|
| 运动 | 加速度计、陀螺仪、磁力计 | MEMS 电容/压阻、科氏力、霍尔效应 |
| 环境 | 气压计、环境光、温湿度 | MEMS 薄膜、光电二极管、NTC |
| 位置 | GNSS、接近传感器、ToF/LiDAR | 伪距定位、红外反射、dToF/iToF |
| 生物识别 | 指纹、面部识别、心率/血氧 | 电容/光学/超声波、结构光、PPG |
| 通信 | NFC、UWB | 电磁感应耦合、脉冲测距 |
| 其他 | 霍尔传感器、红外发射器 | 霍尔效应、PWM 调制 |

## 技术栈

| 组件 | 技术 |
|:-----|:-----|
| 文档框架 | [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| 部署 | GitHub Actions → GitHub Pages |
| 语言 | 中文 (zh) |
| 数学公式 | MathJax 3 |
| 代码示例 | Kotlin (Android)、Swift (iOS)、Python (数据分析) |
| 交互演示 | [Google Colab Notebook](notebooks/sensor_demo.ipynb) |
| 字体 | Noto Sans SC + JetBrains Mono |

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/Zebedee2021/Mobile-Sensor-2026.git
cd Mobile-Sensor-2026

# 安装依赖
pip install mkdocs mkdocs-material

# 本地预览 (热重载)
mkdocs serve

# 访问 http://127.0.0.1:8000
```

## 传感器数据采集（5G/公网穿透）

本项目支持通过 **ngrok** 实现公网穿透，让 5G 手机能够将传感器数据实时推送到本地电脑：

### 快速开始

1. **安装依赖**
   ```bash
   pip install flask pystray pillow
   ```

2. **下载 ngrok** (如需公网访问)
   - 访问 [ngrok.com](https://ngrok.com) 注册免费账号
   - 下载 Windows 版 `ngrok.exe` 放到项目根目录
   - 配置: `ngrok config add-authtoken <你的token>`

3. **启动采集服务**

   **方式一：双击启动（推荐）**
   ```
   启动托盘程序.vbs   ← 无窗口，只在系统托盘显示
   启动托盘程序.bat   ← 显示命令行窗口
   ```

   **方式二：命令行启动**
   ```bash
   # 系统托盘管理
   python scripts/tray.py
   
   # 或纯命令行
   python scripts/server.py -p 8080
   ngrok http 8080
   ```

4. **手机端配置**
   - **右键系统托盘图标** → 「复制 Push URL (局域网)」
   - 打开 Sensor Logger APP → 设置 → Push URL
   - **粘贴**复制的地址 (格式: `http://<电脑IP>:8080/data`)
     - ⚠️ **注意**: IP 地址由托盘程序自动检测，每台电脑不同，必须从菜单复制
   - **5G/公网**: 同样从托盘菜单复制 ngrok URL (`https://xxx.ngrok-free.dev/data`)
   - 点击 **Tap to Test Pushing** 验证连通性

5. **查看仪表盘**
   - 右键系统托盘图标 → 「打开仪表盘 (本地)」
   - 或浏览器访问: `http://localhost:8080/dashboard`

### 功能特点

| 功能 | 说明 |
|:-----|:-----|
| 局域网模式 | 同一 WiFi 下直接访问 `http://<电脑IP>:8080` |
| 5G/公网模式 | 通过 ngrok 隧道，手机使用移动网络也能推送数据 |
| 实时仪表盘 | 浏览器访问 `/dashboard` 查看传感器波形 |
| 多设备支持 | 同时接入多个手机，支持设备切换和数据过滤 |
| 数据来源标识 | 自动区分局域网(LAN)和5G公网数据来源 |
| 数据存储 | 自动保存为 CSV 文件到 `data/` 目录 |
| 系统托盘管理 | 一键启动/停止服务，智能IP检测，避免VPN干扰 |

> **注意**：ngrok 免费版每次启动会分配新的公网 URL，适合教学和测试使用。

### 项目脚本说明

| 脚本 | 功能 |
|:-----|:-----|
| `scripts/server.py` | Flask 数据接收服务 + 实时仪表盘 + SSE实时推送 |
| `scripts/tray.py` | 系统托盘管理程序（智能IP检测、多设备追踪） |
| `scripts/dashboard.html` | 实时可视化仪表盘（多设备切换、数据来源显示） |
| `启动托盘程序.vbs` | 无窗口启动托盘程序 |
| `启动托盘程序.bat` | 带命令行窗口启动 |

### 最新改进 (2025)

- **智能IP检测**: 自动识别真实局域网IP，避免VPN虚拟IP干扰
- **多设备管理**: 支持同时接入多个手机，仪表盘可切换查看
- **数据来源标识**: 自动标记数据来自局域网还是5G公网
- **托盘程序优化**: 修复退出残留、状态显示、一键启停逻辑
- **仪表盘增强**: 设备选择器、实时统计、GitHub链接

### 未来开发方向

- [ ] **实时数据分析**: 仪表盘显示统计值（均值、方差、峰值）
- [ ] **3D姿态可视化**: 用 Three.js 实时显示手机姿态
- [ ] **频谱分析**: 对加速度/陀螺仪数据进行FFT频谱显示
- [ ] **历史回放**: 支持暂停、回放、慢动作查看历史数据
- [ ] **动作识别**: 实时识别走路、跑步、跳跃等动作
- [ ] **手势识别**: 识别特定手势触发事件
- [ ] **云端存储**: 数据自动上传到云数据库
- [ ] **体育训练分析**: 运动员动作姿态分析
- [ ] **健康监测**: 步态分析、跌倒检测

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages：

```
git push → GitHub Actions (mkdocs build) → GitHub Pages
```

工作流配置见 [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)。

## 适用对象

- 高校传感器/物联网/移动开发相关课程的教学辅助
- 对智能手机硬件感兴趣的工程师和学生
- 需要了解手机传感器 API 的移动开发者

## 许可证

本项目文档内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可证，代码示例采用 MIT 许可证。

---

**作者**: Zhiguo Zhou &nbsp;|&nbsp; **2026**
