# 加速度计 (Accelerometer)

## 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 线性加速度 (含重力分量) |
| 量程 | 通常 ±2g / ±4g / ±8g / ±16g 可选 |
| 单位 | m/s² |
| 自由度 | 3轴 (X, Y, Z) |
| 采样率 | 通常 50-400 Hz,部分芯片可达 6.4 kHz |
| 功耗 | ~150 μA (低功耗模式可低至 ~3 μA) |
| Android 常量 | `Sensor.TYPE_ACCELEROMETER` |
| iOS 框架 | `CMAccelerometerData` (Core Motion) |

---

## 工作原理

### 物理基础

加速度计基于**牛顿第二定律** ($F = ma$) 工作。当设备运动时,内部的惯性质量块因惯性而相对于芯片壳体产生位移,这个位移与加速度成正比。

### MEMS 电容式加速度计

现代手机使用的是 **MEMS 电容式** 加速度计,其核心结构为差分电容:

```
  固定极板 A          可动质量块(梳齿)         固定极板 B
  ┌────────┐        ┌─────────────┐        ┌────────┐
  │ │ │ │ │◄── d₁ ──│ │ │ │ │ │ │ │── d₂ ──►│ │ │ │ │
  │ │ │ │ │        │ │ │ │ │ │ │ │        │ │ │ │ │
  │ │ │ │ │◄── d₁ ──│ │ │ │ │ │ │ │── d₂ ──►│ │ │ │ │
  └────────┘        └──────┬──────┘        └────────┘
                           │
                      弹性悬挂梁
```

**工作过程:**

1. **静止时**: 质量块居中,$d_1 = d_2$,两侧电容相等 $C_1 = C_2$
2. **加速时**: 质量块因惯性偏移,$d_1 \neq d_2$,产生差分电容变化:

$$\Delta C = C_1 - C_2 = \varepsilon A \left(\frac{1}{d_1} - \frac{1}{d_2}\right)$$

3. **信号处理**: ASIC 电路检测 $\Delta C$,经放大、ADC 转换后输出数字加速度值

### 三轴检测

单个 MEMS 结构只能检测一个方向的加速度。三轴加速度计通过在芯片上正交排列三组独立的检测结构,分别检测 X、Y、Z 三个方向的加速度。

---

## 典型芯片

| 芯片型号 | 厂商 | 类型 | 量程 | 分辨率 | 尺寸 |
|:---------|:-----|:-----|:-----|:-------|:-----|
| BMA456 | Bosch | 3轴加速度计 | ±2/4/8/16g | 16-bit | 2.0×2.0×0.65 mm |
| LIS2DW12 | ST | 3轴加速度计 | ±2/4/8/16g | 14-bit | 2.0×2.0×0.7 mm |
| BMI260 | Bosch | 6轴 IMU | ±2/4/8/16g | 16-bit | 2.5×3.0×0.83 mm |
| LSM6DSO | ST | 6轴 IMU | ±2/4/8/16g | 16-bit | 2.5×3.0×0.83 mm |
| ICM-42688-P | TDK | 6轴 IMU | ±2/4/8/16g | 16-bit | 2.5×3.0×0.91 mm |

!!! note "趋势"
    现代手机几乎不再使用独立的加速度计芯片,而是采用集成了加速度计+陀螺仪的 **6轴 IMU**,节省空间和功耗。

---

## 关键参数解析

### 量程 (Full Scale Range)

量程决定了传感器能测量的最大加速度。1g ≈ 9.81 m/s²。

| 量程 | 等效加速度 | 适用场景 |
|:-----|:----------|:---------|
| ±2g | ±19.6 m/s² | 倾斜检测、低速运动 |
| ±4g | ±39.2 m/s² | 日常运动、计步 |
| ±8g | ±78.5 m/s² | 剧烈运动、碰撞检测 |
| ±16g | ±157 m/s² | 跌落检测、高冲击场景 |

### 灵敏度与分辨率

灵敏度 = 量程 / 2^(bit数)

以 ±2g 量程、16-bit 分辨率为例:

$$\text{灵敏度} = \frac{4g}{2^{16}} = \frac{4 \times 9.81}{65536} \approx 0.6 \text{ mg} \approx 0.006 \text{ m/s}^2$$

### 噪声密度

噪声密度 (Noise Density) 衡量传感器的本底噪声水平,单位为 $\mu g/\sqrt{Hz}$。

典型值: 100-200 $\mu g/\sqrt{Hz}$

---

## 静态标定

加速度计出厂时已有基本标定,但在实际使用中可能需要现场标定。最常用的方法是 **六面体标定法**:

1. 将手机分别放置在 6 个面朝上的位置 (+X, -X, +Y, -Y, +Z, -Z)
2. 每个位置静止记录数据,理论值应为 ±1g
3. 通过最小二乘法拟合出偏置 (bias) 和比例因子 (scale factor)

标定模型:

$$\vec{a}_{true} = \mathbf{S} \cdot (\vec{a}_{raw} - \vec{b})$$

其中 $\mathbf{S}$ 为 3×3 比例/正交矩阵,$\vec{b}$ 为偏置向量。

---

## 应用实例

### 1. 屏幕旋转检测

通过检测重力加速度在 X、Y 轴上的分量判断手机朝向:

```python
import math

def detect_orientation(ax, ay, az):
    """根据加速度计数据判断屏幕方向"""
    angle = math.atan2(ay, ax) * 180 / math.pi

    if 45 < angle < 135:
        return "竖屏正向 (Portrait)"
    elif -135 < angle < -45:
        return "竖屏反向 (Portrait Inverted)"
    elif -45 < angle < 45:
        return "横屏右转 (Landscape Right)"
    else:
        return "横屏左转 (Landscape Left)"
```

### 2. 简易计步器

利用加速度合成量的周期性波峰检测步态:

```python
import math

def compute_magnitude(ax, ay, az):
    """计算加速度合成量"""
    return math.sqrt(ax**2 + ay**2 + az**2)

def simple_step_counter(data, threshold=10.5, min_interval=0.3):
    """
    简易峰值检测计步
    data: [(timestamp, ax, ay, az), ...]
    """
    steps = 0
    last_step_time = 0

    for t, ax, ay, az in data:
        mag = compute_magnitude(ax, ay, az)
        if mag > threshold and (t - last_step_time) > min_interval:
            steps += 1
            last_step_time = t

    return steps
```

---

## 延伸阅读

- [Bosch BMA456 数据手册](https://www.bosch-sensortec.com/products/motion-sensors/accelerometers/bma456/)
- [Android Sensor.TYPE_ACCELEROMETER 文档](https://developer.android.com/reference/android/hardware/Sensor#TYPE_ACCELEROMETER)
- [Apple CMAccelerometerData 文档](https://developer.apple.com/documentation/coremotion/cmaccelerometerdata)
