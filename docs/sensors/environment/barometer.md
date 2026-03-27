# 气压计 (Barometer)

## 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 大气压力 |
| 量程 | 300-1100 hPa |
| 单位 | hPa (百帕) 或 mbar |
| 分辨率 | 0.01-0.06 hPa |
| 精度 | ±0.5-±1 hPa (绝对), ±0.06-±0.12 hPa (相对) |
| 采样率 | 1-200 Hz |
| 功耗 | ~3-5 μA |
| Android 常量 | `Sensor.TYPE_PRESSURE` |
| iOS 框架 | `CMAltimeter` (Core Motion) |

---

## 工作原理

### MEMS 压阻式气压计

在硅基片上刻蚀出一个密封的真空腔,上方覆盖一层薄膜。薄膜上布有压阻桥路:

```
    大气压力 P
    ↓ ↓ ↓ ↓ ↓ ↓
  ┌────────────────┐
  │  硅薄膜 (含压阻)  │  ← 大气压力使薄膜形变
  ├────────────────┤
  │   真空参考腔     │  ← 密封真空 (参考压力 ≈ 0)
  ├────────────────┤
  │    硅基片       │
  └────────────────┘
```

薄膜在大气压力下弯曲,引起压阻阻值变化,通过惠斯通电桥检测:

$$\frac{\Delta R}{R} = \pi \cdot \sigma$$

其中 $\pi$ 为压阻系数,$\sigma$ 为应力。

### MEMS 电容式气压计

用两个平行极板构成电容,其中一个极板为可形变的薄膜:

$$C = \varepsilon \frac{A}{d}$$

大气压力使薄膜形变,改变极板间距 $d$,从而改变电容值。

---

## 典型芯片

| 芯片型号 | 厂商 | 类型 | 精度 (相对) | 噪声 (RMS) | 尺寸 |
|:---------|:-----|:-----|:----------|:----------|:-----|
| BMP390 | Bosch | 压阻式 | ±0.03 hPa | 0.02 hPa | 2.0×2.0×0.76 mm |
| BMP581 | Bosch | 压阻式 | ±0.02 hPa | 0.017 hPa | 2.0×2.0×1.0 mm |
| LPS22HH | ST | 压阻式 | ±0.025 hPa | 0.015 hPa | 2.0×2.0×0.73 mm |
| ICP-10111 | TDK | 电容式 | ±0.04 hPa | 0.04 hPa | 2.0×2.0×0.72 mm |

---

## 气压与海拔的关系

### 气压高度公式

在标准大气条件下,海拔每升高约 8.4 m,气压下降约 1 hPa:

$$h = 44330 \times \left(1 - \left(\frac{P}{P_0}\right)^{0.1903}\right)$$

其中:

- $h$ — 海拔高度 (m)
- $P$ — 当前气压 (hPa)
- $P_0$ — 海平面标准气压 (1013.25 hPa)

### 楼层检测

一层楼 (约 3m) 对应的气压差约 **0.36 hPa**,这就要求气压计有足够高的相对精度。

```python
def pressure_to_altitude(pressure, sea_level_pressure=1013.25):
    """将气压转换为海拔高度 (m)"""
    return 44330.0 * (1.0 - (pressure / sea_level_pressure) ** 0.1903)

def detect_floor_change(p1, p2, floor_height=3.0):
    """检测楼层变化"""
    h1 = pressure_to_altitude(p1)
    h2 = pressure_to_altitude(p2)
    delta_floors = (h2 - h1) / floor_height
    return round(delta_floors)
```

---

## 延伸阅读

- [Bosch BMP390 数据手册](https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp390/)
- [Android TYPE_PRESSURE 文档](https://developer.android.com/reference/android/hardware/Sensor#TYPE_PRESSURE)
- [Apple CMAltimeter 文档](https://developer.apple.com/documentation/coremotion/cmaltimeter)
