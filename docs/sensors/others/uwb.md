# UWB (Ultra-Wideband)

## 基本信息

| 属性 | 值 |
|:-----|:---|
| 工作频段 | 6.5 GHz / 8 GHz (常用信道) |
| 带宽 | ≥ 500 MHz |
| 通信距离 | ≤ 200 m (视距) |
| 测距精度 | ±5-30 cm |
| 测角精度 | ±3° |
| 标准 | IEEE 802.15.4z |
| 典型芯片 | Apple U2, NXP SR150/SR040, Qorvo DW3720 |

---

## 工作原理

UWB 使用极短的时间脉冲 (纳秒级) 进行通信和测距:

### 脉冲信号特征

```
传统窄带信号:     ∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼∼  (连续正弦波)

UWB 脉冲信号:     ╷   ╷   ╷   ╷   ╷   ╷    (极短脉冲,宽带)
                   │   │   │   │   │   │
                   ▼   ▼   ▼   ▼   ▼   ▼
```

### 双向测距 (TWR)

```
  设备 A                              设备 B
    │                                    │
    │ ─── Poll 请求 ──────────────────► │
    │           t₁                       │  t₂
    │                                    │
    │ ◄── Response 响应 ──────────────── │
    │           t₄                       │  t₃
    │                                    │

    往返时间: T_round = t₄ - t₁
    响应延迟: T_reply = t₃ - t₂

    距离: d = c × (T_round - T_reply) / 2
```

### 到达角度 (AoA)

利用天线阵列检测信号到达的相位差,计算来波方向:

$$\theta = \arcsin\left(\frac{c \cdot \Delta t}{d_{antenna}}\right)$$

结合距离和角度,实现 **空间感知** — 不仅知道目标多远,还知道它在哪个方向。

---

## 与其他技术对比

| 技术 | 测距精度 | 测距范围 | 测角 | 功耗 | 穿透性 |
|:-----|:---------|:---------|:-----|:-----|:-------|
| **UWB** | cm 级 | ≤200 m | 支持 | 中 | 可穿墙 |
| Bluetooth | m 级 | ≤100 m | 有限 | 低 | 可穿墙 |
| Wi-Fi RTT | 1-2 m | ≤50 m | 不支持 | 高 | 可穿墙 |
| NFC | — | ≤10 cm | 不支持 | 低 | 不可 |

---

## 应用场景

| 应用 | 说明 |
|:-----|:-----|
| **AirTag / SmartTag 精确查找** | 显示物品的精确方向和距离 |
| **数字车钥匙** | 靠近车门自动解锁,精确判断用户位置 |
| **空间音频** | 追踪头部位置,实现 3D 音效 |
| **近距离文件传输** | 指向对方设备即可传输 |
| **室内定位** | 配合 UWB 锚点实现厘米级室内定位 |

---

## 延伸阅读

- [Apple Nearby Interaction 框架](https://developer.apple.com/documentation/nearbyinteraction)
- [Android UWB API](https://developer.android.com/develop/connectivity/uwb)
- [FiRa Consortium (UWB 标准组织)](https://www.firaconsortium.org/)
