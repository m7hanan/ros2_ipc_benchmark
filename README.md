# ROS2 IPC Benchmark — Fast DDS Baseline

**Custom Zero-Copy IPC Middleware in Rust for Real-Time LiDAR-IMU Sensor Fusion on Resource-Constrained Robots**

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

To ensure a fair comparison, the ROS2 workload is designed to exactly mirror the Rust middleware's message profile.

| Parameter | Value | Notes |
|:---|:---|:---|
| Message type | sensor_msgs/LaserScan | Standard ROS2 LiDAR message |
| Array size | 720 ranges | Matches LaserScan struct in Rust middleware |
| Publish rate | 10 Hz | Matches real LiDAR driver rate |
| Data content | Random float32 values (0.5-10.0 m) | Simulates realistic indoor scan |
| Transport | Fast DDS (ROS2 Jazzy default) | Industry-standard DDS middleware |

---

## Repository Structure

ros2_ipc_benchmark/
- src/benchmark_nodes/benchmark_nodes/__init__.py
- src/benchmark_nodes/benchmark_nodes/dummy_lidar_pub.py (720-range LaserScan publisher)
- src/benchmark_nodes/benchmark_nodes/latency_sub.py (latency measurement subscriber)
- src/benchmark_nodes/benchmark_nodes/resource_monitor.py (CPU + memory monitor)
- src/benchmark_nodes/package.xml
- src/benchmark_nodes/setup.py
- results_baseline.txt (baseline benchmark results)
- .gitignore (excludes build/install/log artifacts)
- README.md (this file)

---

## Quick Start (Docker)

### Prerequisites
- Docker installed and running
- Ubuntu 22.04/24.04 or WSL2

### 1. Pull ROS2 Jazzy image

docker pull ros:jazzy-ros-base

### 2. Clone and enter repository

git clone https://github.com/m7hanan/ros2_ipc_benchmark.git
cd ros2_ipc_benchmark

### 3. Run container with volume mount

docker run -it --rm --name ros2_benchmark -v $(pwd):/ros2_ws --network host ros:jazzy-ros-base bash

### 4. Build package (inside container)

cd /ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select benchmark_nodes
source install/setup.bash

---

## Running the Benchmark

### Terminal 1 - Publisher

docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes dummy_lidar_pub

### Terminal 2 - Latency Subscriber

docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes latency_sub

The subscriber collects 1,000 messages and prints latency statistics.

### Terminal 3 - Resource Monitor (optional)

docker exec -it ros2_benchmark bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run benchmark_nodes resource_monitor

---

## Baseline Results

Benchmark run: development machine (Docker) | ROS2 Jazzy + Fast DDS | 1,000 samples

### Latency (microseconds)

| Metric | Value |
|:---|:---|
| Mean | 3,826.19 us (~3.83 ms) |
| Median | 3,634.08 us |
| Std Dev | 4,286.94 us |
| Min | 2,699.32 us |
| Max | 134,642.61 us (~135 ms) |

### Resource Usage

| Metric | Value |
|:---|:---|
| Memory (RSS) | ~65 MB |
| CPU (subscriber idle) | ~1% |
| CPU (spike) | ~20% |

### Throughput

| Metric | Value |
|:---|:---|
| Publish rate | 10.0 Hz sustained |
| Message size | ~2.9 KB (720 x float32 + header) |

Note: This run was captured on a development machine under Docker, not the target embedded hardware. The high standard deviation (4.3 ms) and the 135 ms max outlier are consistent with DDS discovery overhead and non-deterministic host scheduling rather than the transport itself. The final thesis comparison will be run on the dedicated target hardware alongside the Rust middleware benchmark, under matched conditions.

---

## Thesis Context

This benchmark serves as the industry baseline in Chapter 5 of the thesis. The custom Rust middleware (zero-copy POSIX SHM + lock-free ring buffer) is measured against these same four metrics under identical workload conditions.

| Aspect | ROS2 Fast DDS (this repo) | Rust Middleware (thesis) |
|:---|:---|:---|
| Transport | DDS over UDP/SHM | POSIX shm_open + ring buffer |
| Serialization | CDR (Common Data Representation) | repr(C) zero-copy |
| Memory safety | Runtime | Compile-time (Rust ownership) |
| Measured latency (dev machine) | ~3.8 ms | To be measured under the same conditions |
| Memory footprint | ~65 MB | To be measured under the same conditions |

---

## Scope Note

Per the confirmed thesis scope boundaries:
- In scope: IPC layer benchmark (latency, CPU, memory, throughput)
- Out of scope: Full SLAM with occupancy-grid mapping, EKF sensor fusion, A* planning, camera/vision integration, multi-robot coordination

---

## License

MIT - for academic and research use.
