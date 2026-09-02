#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import psutil

class ResourceMonitor(Node):
    def __init__(self):
        super().__init__('resource_monitor')
        self.timer = self.create_timer(1.0, self.log_usage)
        self.process = psutil.Process()
        self.cpu_samples = []
        self.mem_samples = []
        
    def log_usage(self):
        cpu = self.process.cpu_percent()
        mem_mb = self.process.memory_info().rss / 1024 / 1024
        self.cpu_samples.append(cpu)
        self.mem_samples.append(mem_mb)
        self.get_logger().info(f'CPU: {cpu:.1f}% | Memory: {mem_mb:.2f} MB')

def main():
    rclpy.init()
    node = ResourceMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
