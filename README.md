

```markdown
# ROS2 IPC Benchmark — Fast DDS Baseline

 Custom Zero-Copy IPC Middleware in Rust for Real-Time LiDAR-IMU Sensor Fusion on Resource-Constrained Robots  

---

## Purpose

This repository contains the **ROS2 Jazzy + Fast DDS baseline benchmark** used to compare against the custom Rust zero-copy shared-memory middleware developed in the main thesis repository.

> **Main thesis repo:** [github.com/m7hanan/amr_middleware](https://github.com/m7hanan/amr_middleware)

The benchmark measures **four key metrics** (per thesis Chapter 5):
- **Latency** (end-to-end, microseconds)
- **CPU usage** (%)
- **Memory footprint** (RSS, MB)
- **Throughput** (messages/sec sustained)

---

## Benchmark Design

To ensure a **fair comparison**, the ROS2 workload is designed to exactly mirror the Rust middleware's message profile:

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
ros2_ipc_benchmark/
├── src/
│   └── benchmark_nodes/
│       ├── benchmark_nodes/
│       │   ├── __init__.py
│       │   ├── dummy_lidar_pub.py      # Dummy 720-range LaserScan publisher
│       │   ├── latency_sub.py          # Latency measurement subscriber
│       │   └── resource_monitor.py     # CPU + memory monitor
│       ├── package.xml
│       └── setup.py
├── results_baseline.txt              # Baseline benchmark results
├── .gitignore                        # Excludes build/install/log artifacts
└── README.md                         # This file
```

---

## Quick Start (Docker)

### Prerequisites
- Docker installed and running
- Ubuntu 22.04/24.04 or WSL2

### 1. Pull ROS2 Jazzy image
```bash
docker pull ros:jazzy-ros-base
```

### 2. Clone and enter repository
```bash
git clone https://github.com/m7hanan/ros2_ipc_benchmark.git
cd ros2_ipc_benchmark
```

### 3. Run container with volume mount
```bash
docker run -it --rm \
  --name ros2_benchmark \
  -v $(pwd):/ros2_ws \
  --network host \
  ros:jazzy-ros-base \
  bash
```

### 4. Build package (inside container)
```bash
cd /ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select benchmark_nodes
source install/setup.bash
```

---

## Running the Benchmark

### Terminal 1 — Publisher
```bash
docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes dummy_lidar_pub
```

### Terminal 2 — Latency Subscriber
```bash
docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes latency_sub
```

The subscriber collects **1,000 messages** and prints latency statistics.

### Terminal 3 — Resource Monitor (optional)
```bash
docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes resource_monitor
```

### Verify publish rate
```bash
docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
ros2 topic hz /scan
```

---

## Baseline Results

Benchmark run: **2026-09-02** | Platform: Laptop (Docker) | ROS2 Jazzy + Fast DDS

### Latency (microseconds)
| Metric | Value |
|:---|:---|
| Mean | **3,826.19 µs** (~3.83 ms) |
| Median | 3,634.08 µs |
| Std Dev | 4,286.94 µs |
| Min | 2,699.32 µs |
| Max | **134,642.61 µs** (~135 ms) |

### Resource Usage
| Metric | Value |
|:---|:---|
| Memory (RSS) | ~65 MB |
| CPU (subscriber idle) | ~1% |
| CPU (spike) | ~20% |

### Throughput
| Metric | Value |
|:---|:---|
| Publish rate | **10.0 Hz** sustained |
| Message size | ~2.9 KB (720 × float32 + header) |

> **Note:** The high standard deviation (4.3 ms) and 135 ms max outlier reflect DDS discovery overhead, garbage collection, and non-deterministic scheduling — precisely the jitter the thesis middleware aims to eliminate via zero-copy shared memory.

---

## Thesis Context

This benchmark serves as the **industry baseline** in Chapter 5 of the thesis. The custom Rust middleware (zero-copy POSIX SHM + lock-free ring buffer) will be measured against these same four metrics under identical workload conditions.

| Aspect | ROS2 Fast DDS (this repo) | Rust Middleware (thesis) |
|:---|:---|:---|
| Transport | DDS over UDP/SHM | POSIX `shm_open` + ring buffer |
| Serialization | CDR (Common Data Representation) | `#[repr(C)]` zero-copy |
| Memory safety | Runtime | Compile-time (Rust ownership) |
| Target latency | ~3.8 ms (measured) | **Target: <100 µs** |
| Memory footprint | ~65 MB | **Target: <1 MB** |

---

## Scope Note

Per the confirmed thesis scope boundaries:
- ✅ **In scope:** IPC layer benchmark (latency, CPU, memory, throughput)
- ❌ **Out of scope:** Gazebo simulation, full SLAM, EKF fusion, A* planning, camera integration — these are deferred to the post-graduation ROgistics conference paper.

---

## License

MIT — For academic and research use.
```
