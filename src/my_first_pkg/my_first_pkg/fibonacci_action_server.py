import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse

from example_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__("fibonacci_action_server")

        self._action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )

        self.get_logger().info("Fibonacci action server ready on /fibonacci")

    def goal_callback(self, goal_request):
        self.get_logger().info(f"Received goal request: order={goal_request.order}")
        if goal_request.order < 0:
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info("Received cancel request")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info("Executing goal...")

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        goal_handle.publish_feedback(feedback_msg)

        for i in range(2, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = Fibonacci.Result()
                result.sequence = feedback_msg.sequence
                return result

            next_number = feedback_msg.sequence[i - 1] + feedback_msg.sequence[i - 2]
            feedback_msg.sequence.append(next_number)

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"Feedback: {feedback_msg.sequence}")

            time.sleep(0.5)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f"Goal succeeded. Result: {result.sequence}")
        return result


def main():
    rclpy.init()
    node = FibonacciActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
