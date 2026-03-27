# 磁力计 (Magnetometer)

## 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 磁场强度 |
| 量程 | 通常 ±4900 μT |
| 单位 | μT (微特斯拉) |
| 自由度 | 3轴 (X, Y, Z) |
| 采样率 | 通常 10-100 Hz |
| 功耗 | ~100-300 μA |
| Android 常量 | `Sensor.TYPE_MAGNETIC_FIELD` |
| iOS 框架 | `CMMagnetometerData` (Core Motion) |

---

## 工作原理

手机磁力计的作用类似于电子指南针,通过测量地球磁场的三维分量来确定朝向。

### 霍尔效应型

当电流通过导体时,垂直于电流方向施加磁场,载流子受洛伦兹力偏转,在导体两侧产生电位差 (霍尔电压):

$$V_H = \frac{I \cdot B}{n \cdot e \cdot d}$$

其中:

- $I$ — 通过导体的电流
- $B$ — 磁感应强度
- $n$ — 载流子浓度
- $e$ — 电子电荷
- $d$ — 导体厚度

### 磁阻效应型 (AMR/TMR)

| 类型 | 全称 | 原理 | 灵敏度 |
|:-----|:-----|:-----|:-------|
| AMR | 各向异性磁阻 | 铁磁材料电阻随磁场方向变化 | 中等 |
| GMR | 巨磁阻 | 多层磁性薄膜结构 | 较高 |
| TMR | 隧道磁阻 | 磁性隧道结,量子隧穿效应 | 最高 |

!!! info "对比"
    霍尔效应型结构简单、成本低,但灵敏度较低;TMR 型灵敏度最高但成本较高。现代高端手机多采用 TMR 或 AMR 型磁力计。

---

## 典型芯片

| 芯片型号 | 厂商 | 技术 | 量程 | 分辨率 | 噪声 |
|:---------|:-----|:-----|:-----|:-------|:-----|
| AK09918 | AKM | 霍尔效应 | ±4912 μT | 0.15 μT | 低 |
| BMM150 | Bosch | 霍尔效应 | ±1300/±2500 μT | 0.3 μT | 低 |
| MMC5983MA | MEMSIC | AMR | ±800 μT | 0.0625 μT | 极低 |
| LIS2MDL | ST | AMR | ±5000 μT | 1.5 mGauss | 低 |

---

## 地磁场基础知识

地球磁场强度约 25-65 μT,可分解为:

- **水平分量 $B_H$**: 指向磁北方向
- **垂直分量 $B_V$**: 指向地心 (北半球向下)
- **磁倾角 (Inclination)**: 磁场与水平面的夹角
- **磁偏角 (Declination)**: 磁北与地理北的偏差

```
        地理北
        ↑
        │╲ 磁偏角 D
        │ ╲
        │  ╲ 磁北
        │   ↗
        │
```

| 地区 | 总磁场强度 | 水平分量 | 磁倾角 |
|:-----|:----------|:---------|:-------|
| 北京 | ~54 μT | ~30 μT | ~58° |
| 赤道 | ~35 μT | ~35 μT | ~0° |
| 伦敦 | ~50 μT | ~19 μT | ~67° |

---

## 磁力计标定

### 硬铁干扰 (Hard Iron)

手机内部的永磁材料 (扬声器磁铁、马达等) 会产生恒定的偏置磁场,使测量值整体偏移:

$$\vec{B}_{measured} = \vec{B}_{true} + \vec{B}_{hard}$$

在三维空间中,未标定的数据点会形成一个偏离原点的球面。

### 软铁干扰 (Soft Iron)

手机内部的铁磁材料 (金属外壳、电路板等) 会扭曲磁场分布,使球面变成椭球面:

$$\vec{B}_{measured} = \mathbf{A} \cdot \vec{B}_{true} + \vec{b}$$

### 标定方法

**"8"字标定**: 用户持手机在空中画"∞"形,使各方向均被采样,然后通过椭球拟合算法求解偏置向量 $\vec{b}$ 和变换矩阵 $\mathbf{A}^{-1}$。

```python
import numpy as np

def calibrate_magnetometer(raw_data):
    """
    椭球拟合标定 (简化版)
    raw_data: Nx3 数组 [(mx, my, mz), ...]
    返回: offset (硬铁偏置), scale (软铁校正)
    """
    # 求各轴最大最小值的中点作为偏置估计
    offset = np.mean([np.max(raw_data, axis=0),
                      np.min(raw_data, axis=0)], axis=0)

    # 求各轴范围作为比例因子
    ranges = np.max(raw_data, axis=0) - np.min(raw_data, axis=0)
    avg_range = np.mean(ranges)
    scale = avg_range / ranges

    return offset, scale

def apply_calibration(raw, offset, scale):
    """应用标定参数"""
    return (raw - offset) * scale
```

---

## 应用实例

### 电子指南针

```python
import math

def compass_heading(mx, my, mz, pitch, roll):
    """
    计算磁航向角 (需要倾斜补偿)
    mx, my, mz: 磁力计读数 (μT)
    pitch, roll: 由加速度计得到的倾斜角 (rad)
    """
    # 倾斜补偿
    mx_comp = (mx * math.cos(pitch)
               + mz * math.sin(pitch))
    my_comp = (mx * math.sin(roll) * math.sin(pitch)
               + my * math.cos(roll)
               - mz * math.sin(roll) * math.cos(pitch))

    # 计算航向角
    heading = math.atan2(-my_comp, mx_comp)
    heading_deg = math.degrees(heading)

    if heading_deg < 0:
        heading_deg += 360

    return heading_deg
```

---

## 延伸阅读

- [AKM AK09918 数据手册](https://www.akm.com/global/en/products/electronic-compass/ak09918/)
- [地磁场模型 — NOAA NCEI](https://www.ngdc.noaa.gov/geomag/WMM/)
- [Android TYPE_MAGNETIC_FIELD 文档](https://developer.android.com/reference/android/hardware/Sensor#TYPE_MAGNETIC_FIELD)
