import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("fibonacci_action_client")
        self._client = ActionClient(self, Fibonacci, "fibonacci")

    def send_goal(self, order: int):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info("Waiting for action server...")
        self._client.wait_for_server()

        self.get_logger().info(f"Sending goal: order={order}")
        self._send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected :(")
            rclpy.shutdown()
            return

        self.get_logger().info("Goal accepted :)")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        seq = feedback_msg.feedback.sequence
        self.get_logger().info(f"Feedback received: {seq}")

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Result: {result.sequence}")
        rclpy.shutdown()


def main():
    rclpy.init()
    node = FibonacciActionClient()
    node.send_goal(order=10)
    rclpy.spin(node)
    node.destroy_node()


if __name__ == "__main__":
    main()
