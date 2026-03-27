# 实验实践

本章提供基于手机传感器的动手实验指南,帮助学生从"知道"到"做到"。

---

## 实验环境

### 推荐工具

| 工具 | 平台 | 用途 | 费用 |
|:-----|:-----|:-----|:-----|
| **SensorLog** | iOS | 专业传感器数据记录与流式传输 | 付费 (~¥22) |
| **Sensor Logger** | iOS / Android | 传感器记录,CSV 导出 | 免费 |
| **phyphox** | iOS / Android | 物理实验平台,自带分析工具 | 免费 |
| **Physics Toolbox** | iOS / Android | 传感器可视化与记录 | 免费 |
| **Python** | PC | 数据分析与可视化 | 免费 |

### 数据处理工具链

```
手机传感器 App → CSV/JSON 导出 → Python 分析 → 可视化/报告
                    │
                    ├── pandas (数据处理)
                    ├── matplotlib (绑图)
                    ├── scipy (信号处理)
                    └── numpy (数值计算)
```
