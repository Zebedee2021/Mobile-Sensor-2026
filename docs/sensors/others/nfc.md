# NFC (Near Field Communication)

## 基本信息

| 属性 | 值 |
|:-----|:---|
| 工作频率 | 13.56 MHz |
| 通信距离 | ≤ 10 cm |
| 数据速率 | 106 / 212 / 424 kbps |
| 标准 | ISO 14443, ISO 18092, ISO 15693 |
| 功耗 | ~15-50 mA (活跃) |
| 典型芯片 | NXP SN220, ST ST25 |

---

## 工作原理

NFC 基于**电磁感应耦合**,工作在 13.56 MHz 频段:

```
   NFC 主设备 (手机)              NFC 从设备 (卡片/读卡器)
  ┌──────────────┐              ┌──────────────┐
  │ ┌──────────┐ │   磁场耦合   │ ┌──────────┐ │
  │ │  NFC     │ │  ◄═══════►  │ │  NFC     │ │
  │ │  线圈    │ │  (≤ 10cm)   │ │  线圈    │ │
  │ └──────────┘ │              │ └──────────┘ │
  │ NFC 控制器   │              │ NFC 标签     │
  └──────────────┘              └──────────────┘
```

### 三种工作模式

| 模式 | 说明 | 应用 |
|:-----|:-----|:-----|
| **读写模式** | 手机读写 NFC 标签 | 读取公交卡余额、NFC 标签 |
| **点对点模式** | 两个 NFC 设备相互通信 | Android Beam (已淘汰) |
| **卡模拟模式** | 手机模拟为 NFC 卡片 | Apple Pay、Google Pay、门禁模拟 |

### 安全元件 (Secure Element)

NFC 支付需要安全元件存储密钥和支付凭证:

| 方案 | 说明 | 使用者 |
|:-----|:-----|:-------|
| **eSE** | 嵌入式安全元件 (独立芯片) | Apple (Apple Pay) |
| **SIM-SE** | SIM 卡内安全元件 | 运营商方案 |
| **HCE** | 主机卡模拟 (软件方案) | Android (Google Pay) |

---

## 延伸阅读

- [NFC Forum 技术规范](https://nfc-forum.org/learn/specifications-and-application-documents/)
- [Android NFC 开发指南](https://developer.android.com/develop/connectivity/nfc)
- [Apple Core NFC 文档](https://developer.apple.com/documentation/corenfc)
