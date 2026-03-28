# 面部识别传感器

<figure markdown="span">
  ![Face ID TrueDepth 系统](../../assets/images/face-id-truedepth.png){ width="680" }
  <figcaption>Apple Face ID TrueDepth 结构光系统原理</figcaption>
</figure>

## Apple Face ID (TrueDepth 系统)

### 硬件组成

Apple Face ID 使用前置 **TrueDepth 摄像头系统**,包含多个传感器协同工作:

<figure markdown="span">
  ![TrueDepth 模组布局](../../assets/images/truedepth-module.png){ width="680" }
  <figcaption>Apple TrueDepth 模组硬件布局：红外接近传感器、泛光感应器、点阵投影器、前置相机、红外相机</figcaption>
</figure>

| 组件 | 功能 | 技术 |
|:-----|:-----|:-----|
| **泛光感应器** | 红外 LED,均匀照亮面部 | 940 nm 近红外 |
| **点阵投影器** | 投射 ~30,000 个红外光点到面部 | VCSEL + DOE |
| **红外相机** | 接收面部反射的红外点阵图案 | 红外 CMOS |
| **前置 RGB 相机** | 辅助检测,拍照 | 可见光 CMOS |

### 结构光原理

<figure markdown="span">
  ![结构光工作原理](../../assets/images/structured-light-principle.png){ width="640" }
  <figcaption>结构光 3D 成像原理：点阵投影器投射已知图案，红外相机捕捉面部形变后的点阵进行三角测量</figcaption>
</figure>

1. 点阵投影器投射已知规则的红外点阵
2. 点阵打在 3D 面部表面后发生形变
3. 红外相机捕捉形变后的点阵图案
4. 通过三角测量原理,从点阵形变恢复面部 3D 几何
5. Neural Engine 将 3D 几何与注册时的面部模型比对

### 安全性

| 指标 | 数值 |
|:-----|:-----|
| FAR (误识率) | < 1/1,000,000 |
| 对比: Touch ID | < 1/50,000 |
| 活体检测 | 红外+注意力检测 (眼睛注视) |
| 防照片/视频攻击 | 3D 深度信息,无法被 2D 图像欺骗 |
| 防面具攻击 | 红外纹理 + 深度精度 |

---

## Android 面部识别方案

Android 阵营的面部识别方案多样:

### 1. 结构光方案

与 Face ID 原理类似,使用红外点阵投影:

- **搭载机型**: 华为 Mate 20 Pro, OPPO Find X
- **安全性**: 可用于支付级认证

### 2. ToF 方案

使用前置 ToF 传感器获取面部深度信息:

- **搭载机型**: 三星 Galaxy S10 5G, LG G8
- **安全性**: 可用于支付级认证

### 3. 2D RGB 方案

仅使用前置 RGB 相机进行面部识别:

- **搭载机型**: 大部分中低端 Android 手机
- **安全性**: 较低,可能被照片欺骗,通常不可用于支付

---

## 关键参数解析

### FAR 与 FRR

面部识别系统的安全性由两个核心指标衡量:

$$FAR = \frac{\text{错误接受次数}}{\text{冒充尝试总数}}$$

$$FRR = \frac{\text{错误拒绝次数}}{\text{合法尝试总数}}$$

- **FAR (False Acceptance Rate, 误识率)**: 非本人被错误接受的概率
- **FRR (False Rejection Rate, 拒识率)**: 本人被错误拒绝的概率
- FAR 和 FRR 通常此消彼长 — 提高安全性 (降低 FAR) 会增加误拒率 (升高 FRR)

### 深度精度与点阵密度

结构光深度测量基于三角测量:

$$Z = \frac{f \cdot B}{d}$$

其中 $f$ 为焦距, $B$ 为基线距离 (投影器与相机间距), $d$ 为视差。Face ID 投射 ~30,000 个点,在 25-50 cm 的典型使用距离上,深度分辨率约为 **0.5-1 mm**,足以区分面部的精细 3D 结构。

### 活体检测 (PAD)

ISO 30107 定义了 **Presentation Attack Detection (PAD)** 标准,评估面部识别系统抵御呈现攻击的能力:

| 攻击方式 | 2D RGB | 结构光/ToF | Face ID |
|:---------|:-------|:----------|:--------|
| 打印照片 | ✗ 易被攻破 | ✓ 深度不匹配 | ✓ 深度+红外 |
| 屏幕视频 | ✗ 易被攻破 | ✓ 深度不匹配 | ✓ 深度+红外 |
| 3D 面具 | — | △ 部分可能通过 | ✓ 红外纹理检测 |
| 化妆伪装 | △ | ✓ 3D 结构不变 | ✓ 3D 结构不变 |

---

## 方案安全性对比

| 方案 | FAR | FRR | 活体检测 | 安全等级 | 可用于支付 |
|:-----|:----|:----|:---------|:---------|:----------|
| **Face ID** | 1/1,000,000 | ~3% | 红外+注意力+3D | 最高 | ✓ |
| Android 结构光 | ~1/500,000 | ~5% | 3D 深度 | 高 | ✓ |
| Android ToF | ~1/100,000 | ~5% | 3D 深度 | 中高 | ✓ (部分) |
| 2D RGB | 1/50,000 - 1/10,000 | ~8% | 有限 | 低 | ✗ |

---

## 应用实例

### 1. 模拟结构光深度图

```python
import numpy as np

def simulate_depth_map(rows=20, cols=20, face_center=(10, 10), face_radius=7):
    """模拟结构光面部深度图 (合成数据)
    返回 2D 深度数组 (单位: mm, 值越小越近)
    """
    depth = np.full((rows, cols), 800.0)       # 背景 800mm
    cx, cy = face_center
    for r in range(rows):
        for c in range(cols):
            dist = np.sqrt((r - cx)**2 + (c - cy)**2)
            if dist < face_radius:
                # 椭球体模型: 鼻子最近 (~400mm), 边缘渐远
                z = 400 + 50 * (dist / face_radius) ** 2
                depth[r, c] = z + np.random.normal(0, 2)
    # 文字可视化
    symbols = '█▓▒░·'
    d_min, d_max = depth.min(), depth.max()
    for row in depth:
        line = ''
        for d in row:
            idx = int((d - d_min) / (d_max - d_min + 1e-6) * (len(symbols) - 1))
            line += symbols[idx]
        print(line)
    return depth

simulate_depth_map()
```

### 2. FAR/FRR 计算

```python
import numpy as np

def compute_far_frr(genuine_scores, impostor_scores, threshold):
    """计算给定阈值下的误识率 (FAR) 和拒识率 (FRR)
    genuine_scores  — 本人匹配评分数组 (越高越匹配)
    impostor_scores — 冒充者匹配评分数组
    threshold       — 判定阈值 (>= threshold 则接受)
    """
    far = np.mean(impostor_scores >= threshold)     # 冒充者被错误接受
    frr = np.mean(genuine_scores < threshold)       # 本人被错误拒绝
    return float(far), float(frr)

# 示例: 模拟评分分布
np.random.seed(42)
genuine = np.random.normal(0.85, 0.08, 1000)       # 本人: 均值 0.85
impostor = np.random.normal(0.35, 0.12, 1000)      # 冒充者: 均值 0.35

print("阈值    FAR        FRR")
print("-" * 30)
for t in [0.4, 0.5, 0.6, 0.7, 0.8]:
    far, frr = compute_far_frr(genuine, impostor, t)
    print(f" {t:.1f}    {far:.4f}     {frr:.4f}")
```

---

## 延伸阅读

- [Apple Face ID 安全性白皮书](https://support.apple.com/guide/security/face-id-and-touch-id-security-sec067eb0c9e/web)
- [Apple TrueDepth 技术概述](https://developer.apple.com/documentation/arkit/arfacetrackingconfiguration)
