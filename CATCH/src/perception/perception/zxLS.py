import rclpy
from rclpy.node import Node
from catch_custom_msgs.msg import PointVel
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class zxLS(Node):
    def __init__(self):
        super().__init__('zxLS')

        # Subscribe to ball state topic
        self.sub = self.create_subscription(
            PointVel,
            '/ball_state',
            self.ball_callback,
            10
        )

        # History storage (exact same as BallTrajectoryEstimator)
        self.positions = deque(maxlen=5)  # matches estimator

        # Matplotlib setup
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("x (meters)")
        self.ax.set_ylabel("z (depth meters)")
        self.ax.set_title("Depth Noise Visualization (z vs x)")

        self.get_logger().info("zxLS node started.")

    def ball_callback(self, msg: PointVel):
        # Append current measurement
        pos = [msg.x, msg.y, msg.z]
        self.positions.append(pos)
        self.update_plot()

    def update_plot(self):
        if len(self.positions) < 2:
            return

        data = np.array(self.positions)
        xs = data[:, 0]
        zs = data[:, 2]

        self.ax.clear()
        self.ax.scatter(xs, zs, s=20, label="Measured points")  # matches estimator

        # Linear fit (least squares)
        if len(xs) >= 2:
            a, b = np.polyfit(xs, zs, 1)
            x_line = np.linspace(xs.min(), xs.max(), 100)
            z_line = a * x_line + b
            self.ax.plot(x_line, z_line, label=f"Linear fit: z = {a:.2f}x + {b:.2f}", linewidth=2)

        # Labels + formatting
        self.ax.set_xlabel("x (meters)")
        self.ax.set_ylabel("z (depth meters)")
        self.ax.set_title("Depth Noise Visualization (z vs x)")
        self.ax.legend(loc="upper left")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main(args=None):
    rclpy.init(args=args)
    node = zxLS()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
