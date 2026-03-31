# 多设备传感器数据采集系统开发

## 概述

本技能记录从单设备到多设备传感器数据采集系统的完整开发过程，包括系统托盘程序、多设备数据隔离、LAN/5G 双模式接入等核心功能的实现经验。

## 核心功能

### 1. 系统托盘管理程序

**技术栈**: Python + pystray + PIL

**关键实现**:
```python
class SensorTray:
    def __init__(self):
        self.flask_proc = None
        self.ngrok_proc = None
        self.ngrok_url = None
        self.icon = None
        self._local_ip = None
```

**核心方法**:
- `get_local_ip()`: VPN-safe IP 检测，排除虚拟网卡
- `ngrok_running()`: 双重检测（自有进程 + API 检测）
- `quit_app()`: 先停图标再停进程，避免残留
- `build_menu()`: 动态菜单，根据状态显示不同选项

**最佳实践**:
- 使用 `subprocess.CREATE_NO_WINDOW` 避免命令行窗口弹出
- 菜单项使用 lambda 实现动态标签
- 移除 `default=True` 确保左右键行为一致

### 2. 多设备数据隔离

**服务端实现** (`server.py`):
```python
# 设备追踪
active_devices = {}
devices_lock = threading.Lock()

# 来源识别
def get_client_source():
    forwarded = request.headers.get('X-Forwarded-For', '')
    host = request.headers.get('Host', '')
    # 排除虚拟网卡
    if client_ip.startswith('192.168.56.'):  # VirtualBox
        return 'virtual'
    # 识别 5G/LAN
    if forwarded or 'ngrok' in host.lower():
        return '5g'
    return 'lan'
```

**设备加入条件**:
1. 排除虚拟网卡来源
2. 必须有实际传感器数据（payload 非空）

### 3. 前端设备选择

**关键设计决策**:
- **移除"所有设备"模式**: 避免多设备数据混淆
- **强制单选**: 必须选择特定设备才能查看数据
- **严格隔离**: 只处理当前选中设备的数据

**实现代码**:
```javascript
// 设备过滤
if (!currentDeviceFilter || currentDeviceFilter === '') {
    return; // 未选择设备，不显示数据
}
if (deviceId !== currentDeviceFilter) {
    return; // 跳过非当前选中设备
}

// 统计更新条件
if (currentDeviceFilter === deviceId) {
    // 只更新当前选中设备的统计
}
```

### 4. LAN/5G 双模式接入

**架构特点**:
- 同一服务器同时监听局域网（WiFi）和公网（ngrok）请求
- 自动识别数据来源，标记 [LAN] 或 [5G]
- 支持双模式同时接入，独立显示

**使用流程**:
1. 启动托盘程序
2. 右键复制 Push URL（局域网或 5G）
3. Sensor Logger 粘贴 URL，测试推送
4. 仪表盘选择设备查看数据

## 常见问题与解决方案

### 问题 1: 设备列表显示无关设备

**原因**: 任何 HTTP POST 请求都会被加入设备列表

**解决**: 
```python
# 只有发送实际传感器数据的设备才加入
payload = data.get("payload", [])
has_sensor_data = payload and len(payload) > 0
if has_sensor_data:
    # 加入设备列表
```

### 问题 2: 虚拟网卡 IP 干扰

**原因**: VirtualBox/VMware 虚拟网卡使用 192.168.56.x 等网段

**解决**:
```python
if client_ip.startswith('192.168.56.') or \
   client_ip.startswith('192.168.99.') or \
   client_ip.startswith('172.16.'):
    return 'virtual'  # 标记为虚拟，不加入设备列表
```

### 问题 3: 多设备数据互相干扰

**原因**: "所有设备"模式下数据混合显示

**解决**: 
- 移除"所有设备"选项
- 强制用户选择单个设备
- 严格过滤，只处理选中设备的数据

### 问题 4: 统计栏显示错误设备信息

**原因**: 收到任何设备数据都更新统计显示

**解决**:
```javascript
// 只有当前选中的设备数据，才更新统计显示
if (currentDeviceFilter === deviceId) {
    document.getElementById('currentDevice').textContent = deviceId.substring(0, 8);
    document.getElementById('dataSource').textContent = sourceLabel;
}
```

### 问题 5: 托盘程序退出后图标残留

**原因**: 先等待进程结束，再停止图标，可能阻塞

**解决**:
```python
def quit_app(self, icon=None, item=None):
    # 先停止托盘图标
    if self.icon:
        icon_obj = self.icon
        self.icon = None
        icon_obj.stop()
    # 再停止进程
    if self.ngrok_proc:
        self.ngrok_proc.terminate()
        self.ngrok_proc.wait(timeout=2)
```

## 文件结构

```
scripts/
├── server.py          # Flask 服务 + 多设备追踪
├── tray.py            # 系统托盘管理程序
└── dashboard.html     # 实时仪表盘 + 设备选择器

启动脚本/
├── 启动托盘程序.vbs   # 无窗口启动
└── 启动托盘程序.bat   # 带窗口启动
```

## 关键配置

**托盘程序** (`tray.py`):
- `PORT = 8080`: 服务端口
- `NGROK_EXE`: ngrok 可执行文件路径
- `FORWARD_URL = "http://localhost:8081/data"`: 可选转发地址

**服务器** (`server.py`):
- `DEVICE_TIMEOUT = 30`: 设备超时时间（秒）
- `DOWNSAMPLE_STRIDE = 5`: 数据降采样率
- `MAX_QUEUE_SIZE = 50`: SSE 客户端队列大小

## 测试清单

- [ ] 托盘程序启动/停止正常
- [ ] 局域网设备接入显示 [LAN]
- [ ] 5G 设备接入显示 [5G]
- [ ] 虚拟网卡请求被忽略
- [ ] 无数据设备不加入列表
- [ ] 设备切换时数据隔离
- [ ] 多页面独立选择设备
- [ ] 退出后无图标残留

## 相关文件

- [tray.py](file://scripts/tray.py)
- [server.py](file://scripts/server.py)
- [dashboard.html](file://scripts/dashboard.html)
- [README.md](file://README.md)
