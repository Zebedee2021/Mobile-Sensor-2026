# SensorLog 使用指南

<figure markdown="span">
  ![SensorLog 工作流程](../assets/images/sensorlog-workflow.png){ width="720" }
  <figcaption>SensorLog 数据采集工作流程：配置 → 记录 → 导出 → 分析</figcaption>
</figure>

## App 简介

| 属性 | 值 |
|:-----|:---|
| 名称 | SensorLog |
| 平台 | iOS (iPhone / iPad / Apple Watch) |
| 开发者 | Bernd Thomas |
| App Store ID | 388014573 |
| 价格 | 付费 (~CHF 3.00 / ¥22) |

---

## 支持的传感器

| 传感器 | iOS 框架类 | 数据字段 |
|:-------|:----------|:---------|
| 加速度计 | `CMAccelerometerData` | accelerometerAccelerationX/Y/Z |
| 陀螺仪 | `CMGyroData` | gyroRotationX/Y/Z |
| 磁力计 | `CMMagnetometerData` | magnetometerX/Y/Z |
| 设备运动 | `CMDeviceMotion` | attitude (roll/pitch/yaw), userAcceleration, gravity, heading |
| GPS 位置 | `CLLocation` | latitude, longitude, altitude, speed, course |
| 气压计 | `CMAltimeter` | pressure, relativeAltitude |
| 音频 | `AVAudioEngine` | audioLevel (dB) |

---

## 基本操作

### 1. 配置采集参数

启动 App 后进入设置页面:

- **采样率 (Sample Rate)**: 建议 50 Hz 用于运动类实验,10 Hz 用于 GPS 实验
- **选择传感器**: 勾选需要采集的传感器类型
- **输出格式**: CSV 或 JSON

### 2. 开始/停止记录

- 点击 **Record** 按钮开始记录
- 运动过程中保持 App 在前台
- 点击 **Stop** 结束记录

### 3. 数据导出

- 记录完成后,在历史记录中选择数据文件
- 通过 **Share** 按钮导出:
    - AirDrop 传到电脑
    - 邮件发送
    - 保存到 iCloud Drive / Files

### 4. 网络流式传输

SensorLog 支持实时推送数据到服务器:

| 协议 | 配置 |
|:-----|:-----|
| TCP | 设置目标 IP 和端口 |
| UDP | 设置目标 IP 和端口 |
| HTTP POST | 设置 URL 端点 |
| HTTP GET | 设置 URL (数据作为查询参数) |

---

## CSV 数据格式

导出的 CSV 文件示例:

```csv
loggingTime,accelerometerAccelerationX,accelerometerAccelerationY,accelerometerAccelerationZ,gyroRotationX,gyroRotationY,gyroRotationZ
2026-03-27T10:00:00.000+0800,0.0234,-0.9812,0.0456,0.0012,-0.0034,0.0078
2026-03-27T10:00:00.020+0800,0.0256,-0.9798,0.0445,0.0015,-0.0031,0.0082
```

---

## Python 数据加载

```python
import pandas as pd
import matplotlib.pyplot as plt

# 加载 CSV
df = pd.read_csv("sensorlog_data.csv")

# 解析时间戳
df['loggingTime'] = pd.to_datetime(df['loggingTime'])
df['elapsed'] = (df['loggingTime'] - df['loggingTime'].iloc[0]).dt.total_seconds()

# 绘制加速度计数据
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

for i, axis in enumerate(['X', 'Y', 'Z']):
    col = f'accelerometerAcceleration{axis}'
    if col in df.columns:
        axes[i].plot(df['elapsed'], df[col], linewidth=0.5)
        axes[i].set_ylabel(f'Accel {axis} (g)')
        axes[i].grid(True, alpha=0.3)

axes[2].set_xlabel('时间 (s)')
fig.suptitle('加速度计原始数据')
plt.tight_layout()
plt.savefig('accelerometer_plot.png', dpi=150)
plt.show()
```

---

## 替代方案: Sensor Logger (免费)

如果不想购买 SensorLog,可以使用免费的 **Sensor Logger** (iOS/Android):

| 特性 | SensorLog | Sensor Logger |
|:-----|:----------|:-------------|
| 价格 | 付费 | 免费 |
| 平台 | iOS | iOS + Android |
| 传感器覆盖 | 全面 | 全面 |
| 导出格式 | CSV / JSON | CSV / JSON |
| 网络流式 | TCP/UDP/HTTP | HTTP POST |
| Apple Watch | 支持 | 支持 |
| Core ML | 支持 | 不支持 |

Sensor Logger 官网: [https://www.tszheichoi.com/sensorlogger](https://www.tszheichoi.com/sensorlogger)

---

## 延伸阅读

- [SensorLog App Store 页面](https://apps.apple.com/app/sensorlog/id388014573)
- [Sensor Logger GitHub 社区](https://github.com/tszheichoi/awesome-sensor-logger)
