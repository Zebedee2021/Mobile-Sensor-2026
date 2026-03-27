# 编程接口

Android 和 iOS 提供了完善的传感器编程框架,开发者可以通过标准 API 访问各类传感器数据。

---

## 平台对比

| 特性 | Android | iOS |
|:-----|:--------|:----|
| 传感器框架 | `android.hardware.Sensor` | `CoreMotion` / `CoreLocation` |
| 语言 | Java / Kotlin | Swift / Objective-C |
| 传感器发现 | 运行时枚举可用传感器 | 框架级支持检测 |
| 采样率控制 | 4 级预设 + 自定义微秒 | 自定义秒级间隔 |
| 后台采集 | 受限 (需前台服务) | 受限 (需后台模式) |
| 传感器融合 | 系统级复合传感器 | Core Motion 内置融合 |
| 数据流模式 | 回调 (Listener) | 回调 (Handler) 或轮询 |
