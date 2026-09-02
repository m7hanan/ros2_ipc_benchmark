#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import statistics

class LatencySubscriber(Node):
    def __init__(self):
        super().__init__('latency_sub')
        self.sub = self.create_subscription(LaserScan, '/scan', self.on_scan, 10)
        self.latencies_us = []
        self.msg_count = 0
        self.max_samples = 1000
        
    def on_scan(self, msg):
        send_ns = msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec
        recv_ns = self.get_clock().now().nanoseconds
        latency_us = (recv_ns - send_ns) / 1000.0
        self.latencies_us.append(latency_us)
        self.msg_count += 1
        
        if self.msg_count % 100 == 0:
            self.get_logger().info(f'Messages: {self.msg_count}, Last: {latency_us:.2f} us')
        
        if self.msg_count >= self.max_samples:
            self.print_stats()
            rclpy.shutdown()
            
    def print_stats(self):
        print("\n=== LATENCY STATISTICS ===")
        print(f"Samples: {len(self.latencies_us)}")
        print(f"Mean: {statistics.mean(self.latencies_us):.2f} us")
        print(f"Median: {statistics.median(self.latencies_us):.2f} us")
        print(f"Std Dev: {statistics.stdev(self.latencies_us):.2f} us")
        print(f"Min: {min(self.latencies_us):.2f} us")
        print(f"Max: {max(self.latencies_us):.2f} us")
        print("==========================\n")

def main():
    rclpy.init()
    node = LatencySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
