"""
Process and visualize Sensor Logger orientation data.

Usage:
    python analyze_data.py                          # use sample data
    python analyze_data.py path/to/your_data.csv    # use your own data
"""
import csv, json, sys, os, glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

# Determine input file
if len(sys.argv) > 1:
    csv_path = sys.argv[1]
elif os.path.isdir('data'):
    # Find largest CSV in data/ (most data)
    csvs = glob.glob('data/*.csv')
    csv_path = max(csvs, key=os.path.getsize) if csvs else None
else:
    csv_path = 'sample_data/orientation_sample.csv'

if not csv_path or not os.path.exists(csv_path):
    print(f"No data file found. Run server.py first to collect data.")
    sys.exit(1)

print(f"Input: {csv_path}")

# Load data
rows = []
with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['sensor'] == 'orientation' and row['extra']:
            try:
                vals = json.loads(row['extra'])
                vals['time_ns'] = int(row['time_ns'])
                rows.append(vals)
            except:
                pass

print(f"Loaded {len(rows)} orientation samples")

# Extract arrays
times_ns = np.array([r['time_ns'] for r in rows])
t = (times_ns - times_ns[0]) / 1e9  # seconds from start

yaw = np.array([r.get('yaw', 0) for r in rows])
pitch = np.array([r.get('pitch', 0) for r in rows])
roll = np.array([r.get('roll', 0) for r in rows])

# Convert to degrees
yaw_deg = np.degrees(yaw)
pitch_deg = np.degrees(pitch)
roll_deg = np.degrees(roll)

# Stats
print(f"\nDuration: {t[-1]:.1f} seconds")
print(f"Sample rate: {len(rows)/t[-1]:.1f} Hz")
print(f"\n{'Axis':<8} {'Mean':>8} {'Std':>8} {'Min':>8} {'Max':>8}  (degrees)")
print("-" * 50)
for name, data in [("Yaw", yaw_deg), ("Pitch", pitch_deg), ("Roll", roll_deg)]:
    print(f"{name:<8} {data.mean():>8.1f} {data.std():>8.1f} {data.min():>8.1f} {data.max():>8.1f}")

# Plot
fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

axes[0].plot(t, yaw_deg, linewidth=0.8, color='#e74c3c')
axes[0].set_ylabel('Yaw (deg)')
axes[0].set_title('Sensor Logger - Phone Orientation Data (HTTP POST)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, pitch_deg, linewidth=0.8, color='#2ecc71')
axes[1].set_ylabel('Pitch (deg)')
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, roll_deg, linewidth=0.8, color='#3498db')
axes[2].set_ylabel('Roll (deg)')
axes[2].set_xlabel('Time (s)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
out_dir = os.path.dirname(csv_path) or '.'
out_path = os.path.join(out_dir, 'orientation_plot.png')
plt.savefig(out_path, dpi=150)
print(f"\nPlot saved to {out_path}")

# Quaternion norm check (should be ~1.0)
qw = np.array([r.get('qw', 0) for r in rows])
qx = np.array([r.get('qx', 0) for r in rows])
qy = np.array([r.get('qy', 0) for r in rows])
qz = np.array([r.get('qz', 0) for r in rows])
norms = np.sqrt(qw**2 + qx**2 + qy**2 + qz**2)
print(f"\nQuaternion norm: mean={norms.mean():.6f}, std={norms.std():.2e} (should be ~1.0)")
