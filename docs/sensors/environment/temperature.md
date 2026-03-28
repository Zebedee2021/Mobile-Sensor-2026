# 温湿度传感器

<figure markdown="span">
  ![温度传感器原理](../../assets/images/temperature-sensor.png){ width="680" }
  <figcaption>PN 结温度传感器与 NTC 热敏电阻工作原理</figcaption>
</figure>

## 温度传感器

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 温度 |
| 量程 | -40°C 至 +85°C |
| 单位 | °C |
| 精度 | ±0.5-±1°C |
| Android 常量 | `Sensor.TYPE_AMBIENT_TEMPERATURE` |

### 工作原理

手机中的温度传感器通常有两种实现:

**1. PN 结温度传感器**

利用 PN 结正向压降随温度变化的特性:

$$V_f = V_0 - k \cdot T$$

其中 $k$ 约为 -2 mV/°C。集成在 SoC 内部,主要用于监控芯片温度。

**2. 热敏电阻 (NTC/PTC)**

| 类型 | 特性 | 用途 |
|:-----|:-----|:-----|
| NTC | 温度升高,电阻减小 | 电池温度监控 |
| PTC | 温度升高,电阻增大 | 过流保护 |

!!! warning "注意"
    手机内部的温度传感器测量的是 **芯片/电池温度**,受 SoC 发热影响严重,不能准确反映环境温度。只有少数机型 (如早期三星 Galaxy S4) 配备了独立的环境温度传感器。

---

## 湿度传感器

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 相对湿度 |
| 量程 | 0-100% RH |
| 单位 | %RH |
| 精度 | ±3-±5% RH |
| Android 常量 | `Sensor.TYPE_RELATIVE_HUMIDITY` |

### 工作原理

**电容式湿度传感器**: 两个电极之间填充吸湿性高分子材料,当环境湿度变化时,材料吸附/释放水分子,介电常数改变,从而改变电容值:

$$C = \varepsilon_r(RH) \cdot \varepsilon_0 \cdot \frac{A}{d}$$

### 搭载情况

湿度传感器在智能手机中 **较为罕见**,仅少数机型搭载:

| 机型 | 年份 | 芯片 |
|:-----|:-----|:-----|
| Samsung Galaxy S4 | 2013 | Sensirion SHTC1 |
| Samsung Galaxy S5 | 2014 | Sensirion SHTC1 |
| Samsung Galaxy Note 4 | 2014 | Sensirion SHTC1 |

此后主流手机基本不再搭载独立温湿度传感器。

---

## 典型芯片

| 芯片型号 | 厂商 | 温度精度 | 湿度精度 | 接口 | 尺寸 |
|:---------|:-----|:---------|:---------|:-----|:-----|
| SHTC3 | Sensirion | ±0.2°C | ±2% RH | I²C | 2×2 mm |
| HDC2080 | TI | ±0.2°C | ±2% RH | I²C | 1.5×1.5 mm |
| BME280 | Bosch | ±1.0°C | ±3% RH | I²C/SPI | 2.5×2.5 mm |
| AHT20 | Aosong | ±0.3°C | ±2% RH | I²C | 4×5 mm |

!!! note "BME280"
    Bosch BME280 是少见的温度+湿度+气压三合一传感器,常用于气象站和户外设备。

---

## 关键参数解析

### 精度与分辨率

温度精度和分辨率是两个不同概念:

| 参数 | 定义 | 典型值 |
|:-----|:-----|:-------|
| **精度** | 测量值与真实值的偏差上限 | ±0.2 至 ±1°C |
| **分辨率** | 能区分的最小温度变化 | 0.01 至 0.1°C |

高分辨率传感器可以敏感地检测微小变化,即使绝对精度不高。

### 热时间常数

传感器从一个温度过渡到新温度的响应速度,定义为达到 63.2% 变化所需时间:

| 封装方式 | 热时间常数 | 说明 |
|:---------|:----------|:-----|
| PCB 集成 | 5-30 s | 受 PCB 热容量影响大 |
| 独立探头 | 1-5 s | 直接接触空气,响应快 |
| 液体浸没 | <1 s | 热传导效率最高 |

### 自热效应

传感器工作电流会产生焦耳热,导致测量值偏高:

$$\Delta T = P_{dissipated} \times R_{thermal}$$

例如传感器功耗 1 mW、热阻 100°C/W 时,$\Delta T$ = 0.1°C。低功耗传感器 (如 DRV5032 的 0.54 μA) 自热效应可忽略不计。

---

## 应用实例

### 1. NTC 热敏电阻温度换算

```python
import math

def ntc_resistance_to_temp(R, R0=10000, T0=298.15, B=3950):
    """NTC 热敏电阻阻值转温度 (B 参数方程)
    R  — 当前电阻值 (Ω)
    R0 — 参考温度 T0 下的标称电阻 (默认 10kΩ)
    T0 — 参考温度 (默认 298.15K = 25°C)
    B  — B 常数 (默认 3950K)
    """
    # Steinhart-Hart 简化式: 1/T = 1/T0 + (1/B)*ln(R/R0)
    inv_T = 1.0 / T0 + (1.0 / B) * math.log(R / R0)
    T_kelvin = 1.0 / inv_T
    return T_kelvin - 273.15    # 转为摄氏度

# 示例: 不同电阻值对应的温度
for r in [33000, 10000, 3300, 1200]:
    print(f"  R = {r:>6} Ω → T = {ntc_resistance_to_temp(r):>6.1f} °C")
```

### 2. 露点温度计算

```python
import math

def dewpoint_from_temp_humidity(T, RH):
    """根据温度和相对湿度计算露点温度 (Magnus 公式)
    T  — 环境温度 (°C)
    RH — 相对湿度 (%, 范围 1-100)
    """
    # Magnus 公式常数 (适用于 -45°C 至 60°C)
    a = 17.625
    b = 243.04   # °C
    gamma = (a * T) / (b + T) + math.log(RH / 100.0)
    T_dew = (b * gamma) / (a - gamma)
    return T_dew

# 示例: 不同温湿度条件下的露点
conditions = [(25, 60), (25, 30), (10, 90), (35, 80)]
for t, rh in conditions:
    dp = dewpoint_from_temp_humidity(t, rh)
    print(f"  T={t}°C, RH={rh}% → 露点={dp:.1f}°C")
```

---

## 延伸阅读

- [Sensirion SHTC3 温湿度传感器](https://sensirion.com/products/catalog/SHTC3/)
- [Android TYPE_AMBIENT_TEMPERATURE 文档](https://developer.android.com/reference/android/hardware/Sensor#TYPE_AMBIENT_TEMPERATURE)
