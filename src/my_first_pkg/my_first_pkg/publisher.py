import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime


class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')

        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.count = 0

        # ✅ publish period in seconds (1.0 = once per second)
        self.declare_parameter('period', 1.0)
        period = self.get_parameter('period').value

        self.timer = self.create_timer(period, self.timer_callback)

        self.get_logger().info(f"Publisher started (period={period} sec)")

    def timer_callback(self):
        now_str = datetime.now().strftime("%H:%M:%S")

        msg = String()
        msg.data = f"{now_str} | Hello from Bryson #{self.count}"

        self.publisher_.publish(msg)
        self.get_logger().info(f"Publishing: {msg.data}")

        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = MyPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
