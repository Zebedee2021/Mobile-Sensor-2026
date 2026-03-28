# 霍尔传感器与红外发射器

## 霍尔传感器 (Hall Sensor)

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 物理量 | 磁场 (有/无) |
| 输出 | 数字开关量 (高/低) 或模拟电压 |
| 功耗 | ~1-10 μA |
| 响应时间 | ~μs 级 |

### 工作原理

基于 **霍尔效应**: 电流通过导体时,若存在垂直于电流方向的磁场,载流子受洛伦兹力偏转,在导体横向产生电位差 (霍尔电压)。

<figure markdown="span">
  ![霍尔效应原理](../../assets/images/hall-effect.png){ width="560" }
  <figcaption>霍尔效应原理：磁场使载流子偏转，产生霍尔电压</figcaption>
</figure>

$$V_H = \frac{I \cdot B}{n \cdot e \cdot d}$$

### 在手机中的应用

| 应用 | 说明 |
|:-----|:-----|
| **翻盖/保护壳检测** | 保护壳内嵌磁铁,合上时霍尔传感器检测到磁场,自动锁屏 |
| **折叠屏铰链检测** | 检测折叠屏的开合角度和状态 |
| **磁吸配件** | 检测 MagSafe 配件的连接状态 |

!!! note "不要混淆"
    霍尔传感器检测的是 **近距离磁铁的有无**,而磁力计测量的是 **地磁场方向**,两者用途完全不同。

### 典型芯片

| 芯片型号 | 厂商 | 类型 | 灵敏度/阈值 | 功耗 |
|:---------|:-----|:-----|:-----------|:-----|
| AH3662 | Allegro | 全极性开关 | ±30 Gauss | 3.5 μA |
| DRV5032 | TI | 超低功耗开关 | ±4.4 mT | 0.54 μA |
| Si7210 | Silicon Labs | 线性+开关 | 0.5 mT 分辨率 | 4 μA |
| AH1815 | Diodes | 微功耗开关 | ±25 Gauss | 2.5 μA |

---

## 红外发射器 (IR Blaster)

### 基本信息

| 属性 | 值 |
|:-----|:---|
| 类型 | 红外 LED |
| 波长 | 940 nm |
| 调制频率 | 36-40 kHz (通常 38 kHz) |
| 发射角度 | 15-45° |
| 有效距离 | 3-10 m |

### 工作原理

红外遥控使用 **脉宽调制 (PWM)** 编码:

<figure markdown="span">
  ![红外遥控 PWM 编码](../../assets/images/ir-pwm-encoding.png){ width="640" }
  <figcaption>红外遥控 38kHz 载波脉宽调制编码 (NEC 协议)</figcaption>
</figure>

### 常见遥控协议

| 协议 | 厂商 | 编码方式 |
|:-----|:-----|:---------|
| NEC | 通用 | 脉冲间距编码 |
| RC5/RC6 | Philips | 曼彻斯特编码 |
| SIRC | Sony | 脉宽编码 |
| 格力/美的 | 国产空调 | 自定义编码 |

### 搭载情况

| 厂商 | 代表机型 | 状态 |
|:-----|:---------|:-----|
| **小米** | 几乎全系列 | 持续保留 |
| **华为** | Mate/P 系列 (早期) | 部分保留 |
| **三星** | Galaxy S6 及以前 | 已取消 |
| **Apple** | — | 从未搭载 |

小米是目前仍在旗舰手机上保留红外发射器的主要厂商,配合"万能遥控"App 可控制空调、电视、机顶盒等家电。

### 典型芯片

| 芯片型号 | 厂商 | 类型 | 波长 | 特点 |
|:---------|:-----|:-----|:-----|:-----|
| VSMY2850G | Vishay | 发射 LED | 940 nm | 高功率, ±17° 发射角 |
| SFH4059 | ams-OSRAM | 发射 LED | 860 nm | 窄角 ±3°, 远距离 |
| TSOP382 | Vishay | 接收模块 | 950 nm | 集成解调, 38kHz |

---

## 应用实例

### 1. 霍尔传感器翻盖检测

```python
def hall_magnet_detector(readings, threshold_on=5.0, threshold_off=2.0):
    """霍尔传感器磁铁检测：模拟翻盖开合事件 (迟滞阈值)
    readings — 磁场强度列表 (mT)
    threshold_on  — 检测到磁铁的阈值 (翻盖合上)
    threshold_off — 磁铁移开的阈值 (翻盖打开)
    """
    is_closed = False
    events = []
    for i, b in enumerate(readings):
        if not is_closed and abs(b) >= threshold_on:
            is_closed = True
            events.append((i, "翻盖关闭"))
        elif is_closed and abs(b) <= threshold_off:
            is_closed = False
            events.append((i, "翻盖打开"))
    return events

# 示例: 模拟磁场读数
readings = [0.1, 0.3, 3.5, 6.2, 8.0, 7.5, 3.0, 1.5, 0.5, 0.2]
for idx, event in hall_magnet_detector(readings):
    print(f"  采样 {idx}: {event} (B={readings[idx]:.1f} mT)")
```

### 2. NEC 红外协议编码

```python
def encode_nec_ir(address, command):
    """NEC 红外协议编码：将地址和命令编码为脉冲持续时间序列 (μs)
    返回 [(mark, space), ...] 列表
    """
    pulses = [(9000, 4500)]    # 引导码: 9ms mark + 4.5ms space
    # 组装 32-bit 数据: address + ~address + command + ~command
    data = (address | ((address ^ 0xFF) << 8) |
            (command << 16) | (((command ^ 0xFF) & 0xFF) << 24))
    for bit in range(32):
        mark = 562              # 所有 bit 的 mark 时长相同
        if (data >> bit) & 1:
            space = 1687        # 逻辑 '1': 562μs mark + 1687μs space
        else:
            space = 562         # 逻辑 '0': 562μs mark + 562μs space
        pulses.append((mark, space))
    pulses.append((562, 0))     # 结束位
    return pulses

# 示例: 编码地址=0x04, 命令=0x08
pulses = encode_nec_ir(0x04, 0x08)
total_us = sum(m + s for m, s in pulses)
print(f"脉冲序列: {len(pulses)} 段, 总时长: {total_us/1000:.1f} ms")
```

### 3. NEC 红外协议解码

```python
def decode_nec_ir(pulses):
    """NEC 红外协议解码：从脉冲序列还原地址和命令
    pulses — [(mark, space), ...] 列表 (μs)
    返回 (address, command) 或 None
    """
    if len(pulses) < 34:
        return None
    # 跳过引导码 (第 0 段)
    data = 0
    for bit in range(32):
        mark, space = pulses[bit + 1]
        if space > 1000:       # space > 1ms → 逻辑 '1'
            data |= (1 << bit)
    address = data & 0xFF
    addr_inv = (data >> 8) & 0xFF
    command = (data >> 16) & 0xFF
    cmd_inv = (data >> 24) & 0xFF
    # 校验取反
    if (address ^ addr_inv) != 0xFF or (command ^ cmd_inv) != 0xFF:
        print("校验失败!")
        return None
    return address, command

# 验证: 构造一个已知脉冲序列再解码
test_pulses = [(9000, 4500)]   # 引导码
data = 0x04 | (0xFB << 8) | (0x08 << 16) | (0xF7 << 24)
for bit in range(32):
    test_pulses.append((562, 1687 if (data >> bit) & 1 else 562))
test_pulses.append((562, 0))
result = decode_nec_ir(test_pulses)
print(f"解码结果: address=0x{result[0]:02X}, command=0x{result[1]:02X}")
```

---

## 延伸阅读

- [Allegro 霍尔传感器技术](https://www.allegromicro.com/en/insights-and-innovations/technical-documents/hall-effect-sensor-ic-publications)
- [NEC 红外协议详解](https://www.sbprojects.net/knowledge/ir/nec.php)
