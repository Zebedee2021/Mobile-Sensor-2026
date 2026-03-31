"""
Sensor Logger 系统托盘启动器
双击运行，在系统托盘管理 Flask 服务和 ngrok 隧道。
"""
import sys, os, subprocess, socket, webbrowser, threading, time, json
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem, Menu

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
SERVER_SCRIPT = os.path.join(SCRIPT_DIR, "server.py")
NGROK_EXE = os.path.join(PROJECT_DIR, "ngrok.exe")
PORT = 8080


class SensorTray:
    def __init__(self):
        self.flask_proc = None
        self.ngrok_proc = None
        self.ngrok_url = None
        self.icon = None
        self._local_ip = None

    # ── Local IP (VPN-safe) ──────────────────────────────
    def get_local_ip(self):
        """获取真实局域网IP，优先192.168.x.x或10.x.x.x，避免VPN虚拟IP"""
        if self._local_ip:
            return self._local_ip
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, encoding='gbk', errors='ignore')
            lines = result.stdout.split('\n')
            current_adapter = None
            for line in lines:
                line = line.strip()
                if '适配器' in line or 'Adapter' in line:
                    current_adapter = line
                if 'IPv4' in line and '地址' in line:
                    ip = line.split(':')[-1].strip()
                    if ip.startswith('192.168.') or ip.startswith('10.'):
                        if current_adapter and not any(x in current_adapter.lower() for x in 
                                                       ['vmware', 'virtualbox', 'vbox', 'vpn', 'virtual']):
                            self._local_ip = ip
                            return self._local_ip
        except Exception:
            pass
        # Fallback to socket method
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self._local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            self._local_ip = "127.0.0.1"
        return self._local_ip

    # ── Notification helper ──────────────────────────────
    def notify(self, msg):
        if self.icon:
            try:
                self.icon.notify(msg, "Sensor Logger")
            except Exception:
                pass

    # ── Flask server ─────────────────────────────────────
    def server_running(self):
        return self.flask_proc is not None and self.flask_proc.poll() is None

    def toggle_server(self, icon=None, item=None):
        if self.server_running():
            self.flask_proc.terminate()
            try:
                self.flask_proc.wait(timeout=5)
            except Exception:
                self.flask_proc.kill()
            self.flask_proc = None
            self.notify("本地服务已停止")
        else:
            self.flask_proc = subprocess.Popen(
                [sys.executable, SERVER_SCRIPT, "-p", str(PORT)],
                cwd=PROJECT_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            # Check if it actually started
            time.sleep(1)
            if self.flask_proc.poll() is not None:
                self.flask_proc = None
                self.notify(f"启动失败! 端口 {PORT} 可能被占用\n尝试关闭占用程序后重试")
            else:
                ip = self.get_local_ip()
                self.notify(f"本地服务已启动 (端口 {PORT})\nPush URL: http://{ip}:{PORT}/data")

    # ── ngrok tunnel ─────────────────────────────────────
    def _check_ngrok_api(self):
        """检测外部已运行的 ngrok 进程"""
        try:
            r = urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2)
            data = json.loads(r.read())
            for t in data.get("tunnels", []):
                url = t.get("public_url", "")
                if url.startswith("https://"):
                    self.ngrok_url = url
                    return True
        except Exception:
            pass
        return False

    def ngrok_running(self):
        if self.ngrok_proc is not None and self.ngrok_proc.poll() is None:
            return True
        if self.ngrok_url and self._check_ngrok_api():
            return True
        return False

    def toggle_ngrok(self, icon=None, item=None):
        if self.ngrok_running():
            self.ngrok_proc.terminate()
            try:
                self.ngrok_proc.wait(timeout=5)
            except Exception:
                self.ngrok_proc.kill()
            self.ngrok_proc = None
            self.ngrok_url = None
            self.notify("ngrok 隧道已停止")
        else:
            if not os.path.exists(NGROK_EXE):
                self.notify("ngrok.exe 未找到!\n请先下载 ngrok 到项目根目录")
                return
            self.ngrok_proc = subprocess.Popen(
                [NGROK_EXE, "http", str(PORT)],
                cwd=PROJECT_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            self.notify("ngrok 隧道启动中...")
            threading.Thread(target=self._fetch_ngrok_url, daemon=True).start()

    def _fetch_ngrok_url(self):
        for _ in range(20):
            time.sleep(1)
            if not self.ngrok_running():
                return
            try:
                r = urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3)
                data = json.loads(r.read())
                for t in data.get("tunnels", []):
                    url = t.get("public_url", "")
                    if url.startswith("https://"):
                        self.ngrok_url = url
                        self.notify(f"ngrok 就绪!\n{url}/data")
                        return
            except Exception:
                pass
        if self.ngrok_running():
            self.notify("ngrok 启动超时, 请检查网络或 authtoken")

    # ── Detect existing ngrok tunnel ────────────────────
    def _detect_existing_ngrok(self):
        """Probe ngrok local API to detect an already-running tunnel."""
        try:
            r = urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3)
            data = json.loads(r.read())
            for t in data.get("tunnels", []):
                url = t.get("public_url", "")
                if url.startswith("https://"):
                    self.ngrok_url = url
                    return True
        except Exception:
            pass
        return False

    # ── Open dashboard ───────────────────────────────────
    def open_local(self, icon=None, item=None):
        webbrowser.open(f"http://localhost:{PORT}/dashboard")

    def open_public(self, icon=None, item=None):
        if not self.ngrok_url:
            self._detect_existing_ngrok()
        if self.ngrok_url:
            webbrowser.open(f"{self.ngrok_url}/dashboard")

    # ── Copy to clipboard ────────────────────────────────
    def _copy(self, text):
        try:
            import tkinter as tk
            r = tk.Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(text)
            r.update()
            r.destroy()
            self.notify(f"已复制: {text}")
        except Exception:
            pass

    def copy_lan_url(self, icon=None, item=None):
        self._copy(f"http://{self.get_local_ip()}:{PORT}/data")

    def copy_5g_url(self, icon=None, item=None):
        if not self.ngrok_url:
            self._detect_existing_ngrok()
        if self.ngrok_url:
            self._copy(f"{self.ngrok_url}/data")

    # ── Quit ─────────────────────────────────────────────
    def start_all(self, icon=None, item=None):
        """Start Flask then ngrok sequentially."""
        if not self.server_running():
            self.toggle_server()
        if not self.ngrok_running():
            self.toggle_ngrok()

    def stop_all(self, icon=None, item=None):
        """Stop ngrok then Flask."""
        if self.ngrok_running():
            self.toggle_ngrok()
        if self.server_running():
            self.toggle_server()

    def all_running(self):
        return self.server_running() and self.ngrok_running()

    def any_running(self):
        return self.server_running() or self.ngrok_running()

    def quit_app(self, icon=None, item=None):
        """退出应用：先停图标，再停进程，避免残留"""
        # 先停止托盘图标
        if self.icon:
            icon_obj = self.icon
            self.icon = None
            icon_obj.stop()
        # 停止 ngrok
        if self.ngrok_proc is not None:
            try:
                self.ngrok_proc.terminate()
                self.ngrok_proc.wait(timeout=2)
            except:
                try:
                    self.ngrok_proc.kill()
                except:
                    pass
            self.ngrok_proc = None
        # 停止 Flask
        if self.flask_proc is not None:
            try:
                self.flask_proc.terminate()
                self.flask_proc.wait(timeout=3)
            except:
                try:
                    self.flask_proc.kill()
                except:
                    pass
            self.flask_proc = None

    # ── Dynamic menu (using callables for labels/enabled) ─
    def build_menu(self):
        return Menu(
            MenuItem(
                lambda item: "■ 一键停止全部" if self.server_running()
                             else "▶ 一键启动全部 (服务+隧道)",
                lambda icon, item: self.stop_all() if self.server_running() else self.start_all(),
                enabled=lambda item: os.path.exists(NGROK_EXE),
            ),
            Menu.SEPARATOR,
            MenuItem(
                lambda item: "■ 停止本地服务 (运行中)" if self.server_running()
                             else f"▶ 启动本地服务 (端口 {PORT})",
                self.toggle_server,
            ),
            MenuItem(
                lambda item: "■ 停止 ngrok (运行中)" if self.ngrok_running()
                             else "▶ 启动 ngrok 隧道",
                self.toggle_ngrok,
                enabled=lambda item: os.path.exists(NGROK_EXE),
            ),
            Menu.SEPARATOR,
            MenuItem(
                "打开仪表盘 (本地)",
                self.open_local,
                enabled=lambda item: self.server_running(),
            ),
            MenuItem(
                lambda item: f"打开仪表盘 (公网)" if not self.ngrok_url
                             else f"打开仪表盘 ({self.ngrok_url[:35]}...)",
                self.open_public,
                enabled=lambda item: bool(self.ngrok_url),
            ),
            Menu.SEPARATOR,
            MenuItem(
                lambda item: f"复制 Push URL (局域网: {self.get_local_ip()}:{PORT})",
                self.copy_lan_url,
            ),
            MenuItem(
                lambda item: "复制 Push URL (5G)" if not self.ngrok_url
                             else f"复制 Push URL ({self.ngrok_url[:35]}...)",
                self.copy_5g_url,
                enabled=lambda item: bool(self.ngrok_url),
            ),
            Menu.SEPARATOR,
            MenuItem("退出", self.quit_app),
        )

    # ── Icon ─────────────────────────────────────────────
    def create_icon_image(self):
        size = 64
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.ellipse([2, 2, size - 3, size - 3], fill="#1976d2", outline="#ffffff", width=2)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        d.text((size // 2, size // 2), "S", fill="#ffffff", font=font, anchor="mm")
        return img

    # ── Run ──────────────────────────────────────────────
    def run(self):
        # Auto-detect any already-running ngrok tunnel
        if self._detect_existing_ngrok():
            print(f"[tray] 检测到已运行的 ngrok 隧道: {self.ngrok_url}")
        self.icon = pystray.Icon(
            name="SensorLogger",
            icon=self.create_icon_image(),
            title="Sensor Logger 服务管理",
            menu=self.build_menu(),
        )
        self.icon.run()


if __name__ == "__main__":
    app = SensorTray()
    app.run()
