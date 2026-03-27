# ToF 与 LiDAR

## ToF 传感器 (Time of Flight)

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 距离 (深度) |
| 量程 | 0.02-5 m (典型) |
| 单位 | mm |
| 精度 | ±1-5% |
| 帧率 | 15-60 fps |
| Android 类 | `CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_DEPTH_OUTPUT` |

### 工作原理

ToF 传感器通过测量光脉冲从发射到返回的时间来计算距离:

$$d = \frac{c \cdot t}{2}$$

其中 $c$ 为光速,$t$ 为往返时间。

#### dToF (Direct ToF)

直接测量光脉冲的往返时间:

```
发射 ──┤├──────────────────────────────┤├── 接收
       t₁                              t₂
       
       d = c × (t₂ - t₁) / 2
```

- 使用 **SPAD (单光子雪崩二极管)** 检测器
- 精度高,抗环境光干扰能力强
- Apple LiDAR 采用此方案

#### iToF (Indirect ToF)

发射连续调制光波,测量反射光的**相位差**:

$$d = \frac{c \cdot \Delta\varphi}{4\pi f}$$

- 结构相对简单
- 受多径干扰影响较大
- 早期 Android ToF 相机多用此方案

### 典型芯片

| 芯片型号 | 厂商 | 类型 | 特点 |
|:---------|:-----|:-----|:-----|
| VL53L5CX | ST | dToF (8×8 区域) | 多区域测距,FOV 63° |
| VL53L1X | ST | dToF (单点) | 4m 量程,小体积 |
| S5K33D | Samsung | iToF (VGA) | 高分辨率深度图 |
| IMX316 | Sony | iToF (CIF) | 背照式 ToF 像素 |

---

## LiDAR 扫描仪

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 类型 | dToF 面阵激光雷达 |
| 量程 | 0-5 m |
| 精度 | ~1% (约 mm 级) |
| 扫描点数 | 数万点/帧 |
| 帧率 | ~15-30 fps |
| 搭载设备 | iPhone 12 Pro+, iPad Pro 2020+ |

### 硬件结构

Apple LiDAR 扫描仪由三个核心组件构成:

```
  ┌─────────────────────────────────┐
  │        LiDAR Scanner            │
  │                                 │
  │  ┌──────────┐   ┌──────────┐  │
  │  │  VCSEL   │   │   SPAD   │  │
  │  │  阵列    │   │  阵列    │  │
  │  │ (发射端) │   │ (接收端) │  │
  │  └──────────┘   └──────────┘  │
  │         │             ▲       │
  │         │  光脉冲     │ 反射  │
  │         ▼             │       │
  │  ┌────────────────────────┐   │
  │  │   光学衍射元件 (DOE)    │   │
  │  │   将单束扩展为点阵     │   │
  │  └────────────────────────┘   │
  └─────────────────────────────────┘
```

- **VCSEL (垂直腔面发射激光器)**: 发射 940nm 近红外激光脉冲
- **DOE (衍射光学元件)**: 将激光分成数千个点,覆盖整个视场
- **SPAD 阵列**: 单光子灵敏度的探测器阵列,精确记录每个点的返回时间

### 与结构光的对比

| 特性 | LiDAR (dToF) | 结构光 (Structured Light) |
|:-----|:-------------|:-------------------------|
| 原理 | 激光飞行时间 | 红外点阵投影 + 三角测量 |
| 量程 | 0-5 m | 0.2-0.8 m |
| 环境适应 | 室内外均可 | 强光下性能下降 |
| 精度 | mm 级 | 亚 mm 级 (近距) |
| 主要用途 | AR、3D 扫描 | Face ID 面部识别 |
| 搭载位置 | 后置摄像头模组 | 前置 TrueDepth 模组 |

### 应用场景

| 应用 | 说明 |
|:-----|:-----|
| AR 遮挡 | 虚拟物体被真实物体遮挡的正确渲染 |
| 场景重建 | 实时 3D mesh 生成 |
| 家具预览 | AR 购物中的家具放置 |
| 夜间对焦 | 暗光环境下辅助相机快速对焦 |
| 测量工具 | Apple 测距仪 App 精确测量物体尺寸 |

---

## 延伸阅读

- [ST VL53L5CX 数据手册](https://www.st.com/en/imaging-and-photonics-solutions/vl53l5cx.html)
- [Apple LiDAR Scanner 技术概述](https://developer.apple.com/augmented-reality/)
- [Apple ARKit 深度 API](https://developer.apple.com/documentation/arkit/arframe/3566299-scenedepth)
