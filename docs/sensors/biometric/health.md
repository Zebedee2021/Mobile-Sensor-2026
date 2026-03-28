# 心率与血氧传感器

## 心率传感器

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 心率 (脉搏频率) |
| 单位 | BPM (次/分钟) |
| 技术 | PPG (光电容积脉搏波描记法) |
| 精度 | ±2-5 BPM (静息), ±5-10 BPM (运动) |
| Android 常量 | `Sensor.TYPE_HEART_RATE` |
| 搭载设备 | Samsung Galaxy S5-S10, 智能手表 |

### PPG 工作原理

**PPG (Photoplethysmography)** 利用光照射皮肤,检测因血液脉动引起的光吸收变化:

<figure markdown="span">
  ![PPG 心率传感器原理](../../assets/images/ppg-heart-rate.png){ width="640" }
  <figcaption>PPG 光电容积脉搏波传感器工作原理：LED 照射皮肤，检测血液脉动引起的反射光变化</figcaption>
</figure>

**原理:**

1. **心脏收缩期 (Systole)**: 血液充盈毛细血管,血容量增大,光吸收增加,反射光减少
2. **心脏舒张期 (Diastole)**: 血液回流,血容量减小,光吸收减少,反射光增加
3. 光电探测器检测反射光的周期性变化,提取脉搏频率

### 光源选择

| 光源 | 波长 | 穿透深度 | 优点 | 用途 |
|:-----|:-----|:---------|:-----|:-----|
| 绿光 | 525 nm | 浅 (~1mm) | 对血容量变化最敏感 | 心率检测 (手腕) |
| 红光 | 660 nm | 中 (~3mm) | 对氧合血红蛋白敏感 | 血氧检测 |
| 红外 | 940 nm | 深 (~5mm) | 对脱氧血红蛋白敏感 | 血氧检测 |

### 信号处理流程

<figure markdown="span">
  ![PPG 信号处理流程](../../assets/images/ppg-signal-processing.png){ width="680" }
  <figcaption>PPG 信号处理管线：从原始信号到心率 BPM</figcaption>
</figure>

心率计算:

$$HR = \frac{60}{RR_{interval}} \text{ (BPM)}$$

其中 $RR_{interval}$ 为相邻两个脉搏波峰之间的时间间隔 (秒)。

---

## 血氧传感器 (SpO2)

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 血氧饱和度 |
| 单位 | %SpO2 |
| 正常范围 | 95-100% |
| 精度 | ±2% |
| 搭载设备 | Apple Watch S6+, Samsung Galaxy Watch 3+ |

### 工作原理

血氧检测利用 **氧合血红蛋白 (HbO₂)** 和 **脱氧血红蛋白 (Hb)** 对不同波长光的吸收特性差异:

| 波长 | HbO₂ 吸收 | Hb 吸收 |
|:-----|:----------|:--------|
| 红光 (660 nm) | 低 | **高** |
| 红外 (940 nm) | **高** | 低 |

通过计算红光与红外光吸收的比值 $R$:

$$R = \frac{AC_{red} / DC_{red}}{AC_{ir} / DC_{ir}}$$

$$SpO_2 = a - b \times R$$

其中 $a, b$ 为经验校准常数 (通常 $a \approx 110, b \approx 25$)。

### 反射式 vs 透射式

| 方式 | 原理 | 设备 |
|:-----|:-----|:-----|
| 透射式 | LED 在一侧,探测器在另一侧 | 传统指夹式血氧仪 |
| 反射式 | LED 和探测器在同一侧 | 智能手表、手机 |

手机/手表采用反射式,精度相对较低但使用方便。

---

## 典型芯片

| 芯片型号 | 厂商 | LED 通道 | 支持 SpO2 | 采样率 | 尺寸 |
|:---------|:-----|:---------|:----------|:-------|:-----|
| MAX86150 | Maxim (ADI) | 绿+红+红外 | ✓ | 50-3200 Hz | 3.3×5.6 mm |
| SFH7072 | ams-OSRAM | 绿+红+红外 | ✓ | 最高 400 Hz | 4.7×2.5 mm |
| ADPD4101 | ADI | 8 通道可配 | ✓ | 最高 4000 Hz | 3.5×7.4 mm |
| BH1792GLC | ROHM | 绿光 | ✗ | 32/64/1024 Hz | 2.8×2.8 mm |

!!! note "趋势"
    新一代 PPG 芯片普遍集成加速度计接口,用于运动伪影消除 (Motion Artifact Removal),提升运动状态下的心率测量精度。

---

## 关键参数解析

### 信噪比 (SNR)

PPG 信号的主要噪声来源是 **运动伪影 (Motion Artifact)**。手腕佩戴设备在运动中,传感器与皮肤之间的相对位移会引入比心搏信号更大的干扰。

提升 SNR 的常见方法:

| 方法 | 原理 |
|:-----|:-----|
| 多波长补偿 | 利用不同波长对运动噪声和心搏信号的不同响应,自适应滤波 |
| 加速度计参考 | 利用 IMU 数据估计运动分量并从 PPG 中减去 |
| 多 PD 布局 | 多个光电探测器取差分信号,抑制共模噪声 |

### 采样率

PPG 信号的基频即心率频率,典型范围 0.7-3.3 Hz (对应 40-200 BPM)。

- **最低要求**: 根据奈奎斯特定理,采样率 ≥ 2 × 3.3 ≈ **7 Hz**
- **实际推荐**: 25-100 Hz (保留波形细节用于 HRV 分析)
- **高采样率场景**: >200 Hz (用于脉搏波传播时间 PTT 估计血压)

### 灌注指数 (PI)

$$PI = \frac{AC}{DC} \times 100\%$$

灌注指数反映检测部位的血液灌注程度,是评估 PPG **信号质量**的关键指标:

| PI 值 | 信号质量 | 说明 |
|:------|:---------|:-----|
| > 2% | 优秀 | 血流充足,波形清晰 |
| 0.5-2% | 一般 | 可用但噪声较大 |
| < 0.5% | 差 | 末梢循环不良,数据不可靠 |

---

## 应用实例

### 1. 合成 PPG 信号

```python
import numpy as np

def generate_ppg_signal(duration=10, heart_rate=72, fs=100):
    """合成模拟 PPG 脉搏波信号"""
    t = np.arange(0, duration, 1.0 / fs)
    f_hr = heart_rate / 60.0          # 心率基频 (Hz)
    # PPG 波形 = 基频 + 二次谐波 (模拟收缩期/舒张期不对称波形)
    signal = (0.6 * np.sin(2 * np.pi * f_hr * t)
              + 0.3 * np.sin(4 * np.pi * f_hr * t + 0.8)
              + 0.1 * np.sin(6 * np.pi * f_hr * t + 1.2))
    # 加入基线漂移和高斯噪声
    baseline = 0.2 * np.sin(2 * np.pi * 0.1 * t)
    noise = np.random.normal(0, 0.05, len(t))
    return t, signal + baseline + noise
```

### 2. 峰值检测计算心率

```python
import numpy as np

def compute_heart_rate(ppg_signal, fs=100, min_bpm=40, max_bpm=200):
    """从 PPG 信号中提取心率 (BPM)，返回 (平均心率, 逐拍心率列表)"""
    min_dist = int(fs * 60 / max_bpm)   # 最小峰间距 (采样点)
    threshold = np.mean(ppg_signal) + 0.3 * np.std(ppg_signal)
    # 简单峰值检测
    peaks = []
    for i in range(1, len(ppg_signal) - 1):
        if (ppg_signal[i] > ppg_signal[i-1] and
            ppg_signal[i] > ppg_signal[i+1] and
            ppg_signal[i] > threshold):
            if len(peaks) == 0 or (i - peaks[-1]) >= min_dist:
                peaks.append(i)
    # 计算逐拍心率
    if len(peaks) < 2:
        return 0, []
    rr_intervals = np.diff(peaks) / fs          # 秒
    beat_hr = 60.0 / rr_intervals               # BPM
    # 过滤生理范围外的值
    valid = (beat_hr >= min_bpm) & (beat_hr <= max_bpm)
    return float(np.mean(beat_hr[valid])), beat_hr[valid].tolist()
```

### 3. 血氧饱和度计算

```python
def compute_spo2(ac_red, dc_red, ac_ir, dc_ir):
    """根据红光/红外光信号计算血氧饱和度 (SpO2)
    参数: ac_red/dc_red — 红光 AC 和 DC 分量
          ac_ir/dc_ir   — 红外光 AC 和 DC 分量
    """
    R = (ac_red / dc_red) / (ac_ir / dc_ir)     # 比值 R
    spo2 = 110 - 25 * R                          # 经验公式
    return max(0, min(100, spo2))                # 钳位到 0-100%

# 示例
print(compute_spo2(ac_red=0.8, dc_red=50, ac_ir=1.2, dc_ir=55))  # ≈97.0%
```

---

## 延伸阅读

- [PPG 传感器原理 — Maxim Integrated](https://www.analog.com/en/technical-articles/guidelines-for-spo2-measurement.html)
- [Android TYPE_HEART_RATE 文档](https://developer.android.com/reference/android/hardware/Sensor#TYPE_HEART_RATE)
- [Apple HealthKit 文档](https://developer.apple.com/documentation/healthkit)
