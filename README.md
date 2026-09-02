# ROS2 IPC Benchmark — Fast DDS Baseline

**Custom Zero-Copy IPC Middleware in Rust for Real-Time LiDAR-IMU Sensor Fusion on Resource-Constrained Robots**

---

## Purpose

This repository contains the **ROS2 Jazzy + Fast DDS baseline benchmark** used to compare against the custom Rust zero-copy shared-memory middleware developed in the main thesis repository.

> **Main thesis repo:** [github.com/m7hanan/amr_middleware](https://github.com/m7hanan/amr_middleware)

The benchmark measures **four key metrics** (per thesis Chapter 5):

- **Latency** — end-to-end, microseconds
- **CPU usage** — percent
- **Memory footprint** — RSS, MB
- **Throughput** — messages/sec sustained

---

## Benchmark Design

To ensure a **fair comparison**, the ROS2 workload is designed to exactly mirror the Rust middleware's message profile.

| Parameter | Value | Notes |
|:---|:---|:---|
| Message type | `sensor_msgs/LaserScan` | Standard ROS2 LiDAR message |
| Array size | **720 ranges** | Matches `LaserScan` struct in Rust middleware |
| Publish rate | **10 Hz** | Matches real LiDAR driver rate |
| Data content | Random `float32` values (0.5–10.0 m) | Simulates realistic indoor scan |
| Transport | Fast DDS (ROS2 Jazzy default) | Industry-standard DDS middleware |

---

## Repository Structure

```
ros2_benchmark/
├── src/
│   └── laserscan_benchmark/
│       ├── package.xml
│       ├── CMakeLists.txt
│       ├── src/
│       │   ├── publisher_node.cpp     # Publishes synthetic LaserScan at 10 Hz
│       │   └── subscriber_node.cpp    # Subscribes and timestamps each message
│       └── launch/
│           └── benchmark.launch.py
├── scripts/
│   ├── run_latency_benchmark.sh       # Runs N trials, logs timestamps
│   ├── measure_cpu_mem.sh             # Samples CPU/RSS during a run
│   └── analyze_results.py             # Computes mean/std dev, generates plots
├── results/
│   ├── raw/                           # Per-trial CSV logs
│   └── summary/                       # Aggregated statistics + graphs
├── docker/
│   └── Dockerfile                     # Pre-built ROS2 Jazzy image
└── README.md
```

---

## Running the Benchmark

### 1. Build the ROS2 workspace

```bash
cd ros2_benchmark
colcon build --symlink-install
source install/setup.bash
```

### 2. Launch the publisher/subscriber pair

```bash
ros2 launch laserscan_benchmark benchmark.launch.py
```

### 3. Run the full trial set

```bash
./scripts/run_latency_benchmark.sh --trials 20
```

### 4. Generate the comparison report

```bash
python3 scripts/analyze_results.py --output results/summary/
```

---

## Methodology Notes

- Each trial runs for a fixed duration with the publisher and subscriber pinned to separate CPU cores where possible, matching the deployment conditions used for the Rust middleware benchmark.
- Latency is measured as the time delta between message publish and message receipt, using microsecond-resolution timestamps embedded in each message.
- CPU and memory are sampled at fixed intervals throughout each trial and averaged.
- All 20+ trials per metric are statistically summarised (mean, standard deviation) before comparison against the Rust middleware results.

---

## Related

- [Main thesis repository — Rust zero-copy middleware](https://github.com/m7hanan/amr_middleware)
