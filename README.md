# 手机传感器技术

> 智能手机内置传感器 —— 原理、硬件与编程实践

[![Deploy](https://github.com/Zebedee2021/Mobile-Sensor-2026/actions/workflows/deploy.yml/badge.svg)](https://github.com/Zebedee2021/Mobile-Sensor-2026/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://zebedee2021.github.io/Mobile-Sensor-2026/)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

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
    └── data-collection.md    #   数据采集实验 (计步器·指南针·气压楼层·手势识别)
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
