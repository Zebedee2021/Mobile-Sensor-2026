"""
Sensor Logger HTTP POST 接收服务 + 实时 Dashboard
启动: python server.py
手机 Sensor Logger Push URL 填: http://<你的电脑IP>:8000/data
仪表盘: http://<你的电脑IP>:8000/dashboard

数据流:
  手机 → ngrok → server.py (8000)
                    ├─ 写入 CSV (data/ 目录)
                    └─ 转发 → Digital Twin 托盘程序 (localhost:8081/data)
"""
from flask import Flask, request, jsonify, Response
import json, csv, os, queue, threading, math, argparse
from datetime import datetime

# ── 转发配置 ──────────────────────────────────────
FORWARD_URL = "http://localhost:8081/data"   # Digital Twin 托盘程序端口
FORWARD_ENABLED = True                        # 设为 False 可关闭转发
# ─────────────────────────────────────────────────

app = Flask(__name__)
os.makedirs("data", exist_ok=True)

def _forward(data: dict):
    """后台线程转发，不阻塞主请求"""
    try:
        import urllib.request as _req
        body = json.dumps(data).encode("utf-8")
        req  = _req.Request(FORWARD_URL, data=body,
                            headers={"Content-Type": "application/json"})
        with _req.urlopen(req, timeout=1):
            pass
    except Exception:
        pass  # 托盘程序未启动时静默忽略

def get_client_source():
    """判断数据来源: 'lan' (局域网) 或 '5g' (ngrok公网)"""
    forwarded = request.headers.get('X-Forwarded-For', '')
    host = request.headers.get('Host', '')
    # ngrok 请求通常带有 X-Forwarded-For 或特定 Host
    if forwarded or 'ngrok' in host.lower():
        return '5g'
    # 检查是否是本地网络IP
    client_ip = request.remote_addr
    if client_ip and (client_ip.startswith('192.168.') or 
                      client_ip.startswith('10.') or 
                      client_ip.startswith('172.')):
        return 'lan'
    return 'unknown'


@app.route("/data", methods=["POST"])
def receive():
    data = request.get_json()
    sid = data.get("sessionId", "unknown")
    did = data.get("deviceId", "unknown")
    source = get_client_source()
    
    # 更新活跃设备列表
    with devices_lock:
        active_devices[did] = {
            'session_id': sid,
            'last_seen': datetime.now().isoformat(),
            'source': source,
            'ip': request.remote_addr
        }

    # ── 写 CSV ──────────────────────────────────
    filepath = f"data/{sid}.csv"
    is_new = not os.path.exists(filepath)

    count = 0
    with open(filepath, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["time_ns", "device", "sensor", "x", "y", "z", "extra"])
        for item in data.get("payload", []):
            v = item.get("values", {})
            if isinstance(v, list):
                w.writerow([
                    item.get("time", ""), did, item.get("name", ""),
                    "", "", "",
                    json.dumps(v, ensure_ascii=False)
                ])
            elif isinstance(v, dict):
                w.writerow([
                    item.get("time", ""), did, item.get("name", ""),
                    v.get("x", v.get("latitude", v.get("pressure", ""))),
                    v.get("y", v.get("longitude", v.get("relativeAltitude", ""))),
                    v.get("z", v.get("altitude", "")),
                    json.dumps({k: v2 for k, v2 in v.items()
                               if k not in ("x", "y", "z")}, ensure_ascii=False) or ""
                ])
            else:
                w.writerow([
                    item.get("time", ""), did, item.get("name", ""),
                    str(v), "", "", ""
                ])
            count += 1

    now = datetime.now().strftime("%H:%M:%S")
    source_label = "5G" if source == '5g' else "LAN"
    print(f"[{now}] [{source_label}] {did} | {count} samples | -> {filepath}")

    # ── 转发到 Digital Twin 托盘程序 ────────────
    if FORWARD_ENABLED:
        threading.Thread(target=_forward, args=(data,), daemon=True).start()

    # Broadcast downsampled data to SSE clients (包含设备和来源信息)
    downsample_and_broadcast(sid, did, source, data.get("payload", []))

    return jsonify(status="ok"), 200

# ── SSE real-time broadcast ──────────────────────────────
DOWNSAMPLE_STRIDE = 5        # 100Hz -> 20Hz for browser display
MAX_QUEUE_SIZE = 50           # max buffered events per client
clients = []                  # list of queue.Queue, one per SSE client
clients_lock = threading.Lock()
_t0 = {}                      # session_id -> first timestamp (ns)

# ── Multi-device tracking ────────────────────────────────
# 追踪活跃设备: device_id -> {session_id, last_seen, source}
active_devices = {}
devices_lock = threading.Lock()
DEVICE_TIMEOUT = 30           # 设备超时时间(秒)

ORIENTATION_KEYS = {'yaw', 'pitch', 'roll', 'qw', 'qx', 'qy', 'qz'}
XYZ_SENSORS = {'accelerometer', 'gyroscope', 'gravity',
               'accelerometeruncalibrated', 'gyroscopeuncalibrated'}


def broadcast(event_data):
    """Push event to all connected SSE clients."""
    msg = json.dumps(event_data, ensure_ascii=False)
    with clients_lock:
        dead = []
        for q in clients:
            try:
                q.put_nowait(msg)
            except queue.Full:
                try:
                    q.get_nowait()   # drop oldest
                    q.put_nowait(msg)
                except Exception:
                    dead.append(q)
        for q in dead:
            clients.remove(q)


def downsample_and_broadcast(sid, device_id, source, payload):
    """Group payload by sensor, downsample, normalize, and broadcast via SSE."""
    if not clients:
        return

    # Group by sensor name
    groups = {}
    for item in payload:
        name = item.get("name", "")
        groups.setdefault(name, []).append(item)

    sensors = {}
    for name, items in groups.items():
        # Stride downsample
        sampled = items[::DOWNSAMPLE_STRIDE]
        if not sampled:
            continue

        # Determine t0 for this session
        first_t = int(sampled[0].get("time", 0))
        if sid not in _t0:
            _t0[sid] = first_t

        if name in XYZ_SENSORS:
            fields = ["t", "x", "y", "z"]
            data = []
            for s in sampled:
                v = s.get("values", {})
                if not isinstance(v, dict):
                    continue
                t = round((int(s.get("time", 0)) - _t0[sid]) / 1e9, 3)
                data.append([t,
                             round(v.get("x", 0), 4),
                             round(v.get("y", 0), 4),
                             round(v.get("z", 0), 4)])
            sensors[name] = {"fields": fields, "data": data}

        elif name == "orientation":
            fields = ["t", "yaw", "pitch", "roll"]
            data = []
            for s in sampled:
                v = s.get("values", {})
                if not isinstance(v, dict):
                    continue
                t = round((int(s.get("time", 0)) - _t0[sid]) / 1e9, 3)
                data.append([t,
                             round(math.degrees(v.get("yaw", 0)), 2),
                             round(math.degrees(v.get("pitch", 0)), 2),
                             round(math.degrees(v.get("roll", 0)), 2)])
            sensors[name] = {"fields": fields, "data": data}

        else:
            # Unknown sensor: pass raw values
            fields = ["t", "value"]
            data = []
            for s in sampled:
                v = s.get("values", {})
                t = round((int(s.get("time", 0)) - _t0[sid]) / 1e9, 3)
                data.append([t, v])
            sensors[name] = {"fields": fields, "data": data}

    if sensors:
        broadcast({
            "session": sid,
            "device": device_id,
            "source": source,
            "sensors": sensors
        })





@app.route("/stream")
def stream():
    """SSE endpoint: browser connects here for real-time sensor data."""
    q = queue.Queue(maxsize=MAX_QUEUE_SIZE)
    with clients_lock:
        clients.append(q)

    def generate():
        try:
            while True:
                try:
                    msg = q.get(timeout=15)
                    yield f"event: sensor_data\ndata: {msg}\n\n"
                except queue.Empty:
                    yield ": heartbeat\n\n"
        except GeneratorExit:
            pass
        finally:
            with clients_lock:
                if q in clients:
                    clients.remove(q)

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no"})


@app.route("/dashboard")
def dashboard():
    """Serve the real-time dashboard HTML."""
    html_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
    with open(html_path, encoding="utf-8") as f:
        return f.read(), 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/devices")
def get_devices():
    """获取当前活跃设备列表"""
    with devices_lock:
        # 清理超时设备
        now = datetime.now()
        expired = []
        for did, info in active_devices.items():
            last = datetime.fromisoformat(info['last_seen'])
            if (now - last).total_seconds() > DEVICE_TIMEOUT:
                expired.append(did)
        for did in expired:
            del active_devices[did]
        return jsonify(list(active_devices.items()))


@app.route("/", methods=["GET"])
def index():
    return ('<h2>Sensor Logger Server Running</h2>'
            '<p>POST data to <code>/data</code></p>'
            '<p><a href="/dashboard">Open Real-time Dashboard</a></p>'), 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8000)
    args = parser.parse_args()
    print("=" * 50)
    print("Sensor Logger HTTP Server")
    print(f"Push URL:   http://<your-ip>:{args.port}/data")
    print(f"Dashboard:  http://localhost:{args.port}/dashboard")
    print(f"Forward  : {FORWARD_URL}  ({'ON' if FORWARD_ENABLED else 'OFF'})")
    print("=" * 50)
    app.run(host="0.0.0.0", port=args.port, threaded=True)
