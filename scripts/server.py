"""
Sensor Logger HTTP POST 接收服务
启动: python server.py
手机 Sensor Logger Push URL 填: http://<你的电脑IP>:8000/data
"""
from flask import Flask, request, jsonify
import json, csv, os
from datetime import datetime

app = Flask(__name__)
os.makedirs("data", exist_ok=True)

@app.route("/data", methods=["POST"])
def receive():
    data = request.get_json()
    sid = data.get("sessionId", "unknown")
    did = data.get("deviceId", "unknown")

    filepath = f"data/{sid}.csv"
    is_new = not os.path.exists(filepath)

    count = 0
    with open(filepath, "a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["time_ns", "device", "sensor", "x", "y", "z", "extra"])
        for item in data.get("payload", []):
            v = item.get("values", {})
            # values 可能是 dict 也可能是 list，统一处理
            if isinstance(v, list):
                # list 格式: 直接存为 JSON
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
    print(f"[{now}] {did} | {count} samples | -> {filepath}")
    return jsonify(status="ok"), 200

@app.route("/", methods=["GET"])
def index():
    return "<h2>Sensor Logger Server Running</h2><p>POST data to <code>/data</code></p>", 200

if __name__ == "__main__":
    print("=" * 50)
    print("Sensor Logger HTTP Server")
    print("Push URL: http://<your-ip>:8000/data")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8000)
