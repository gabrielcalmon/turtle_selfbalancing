import rclpy
from rclpy.node import Node
import sensor_msgs.msg
import std_msgs.msg
import geometry_msgs.msg

import math, time


class ImuCustomNode(Node):

    def __init__(self):
        super().__init__('imu_custom_node')
        #self.publisherAngle = self.create_publisher(std_msgs.msg.Float32, '/rotation_angle', 10)
        self.publisherController = self.create_publisher(geometry_msgs.msg.Twist, '/cmd_vel', 10)
        timer_period = 0.05  # seconds (1/20hz = 0.05s)
        self.timer = self.create_timer(timer_period, self.publish_callback)
        self.i = 0

        self.subscription = self.create_subscription(
          sensor_msgs.msg.Imu, 
          '/imu', 
          self.listener_callback, 
          10)
        self.subscription # prevent unused variable warning
        self.quaternion=[0,0,0,0] # inicializa com valores arbitrarios
        self.euler=[0,0,0]


    def listener_callback(self, data):
        """
        Callback function.
        """
        self.quaternion=[data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
        self.euler = self.euler_from_quaternion(data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
        

    def publish_callback(self):
        """
        Publish the data
        """
        # value = std_msgs.msg.Float32()
        # value.data = self.euler[0]
        # self.publisherAngle(value)

        velocity = geometry_msgs.msg.Twist()
        #velocity.linear.x=1

        #print(f'Angle = {self.euler[0]}')
        #print(velocity)
        print(self.euler)

        # TO DO: calcular controlador
        #self.publisherController.publish()
        


    def euler_from_quaternion(self, x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.degrees(math.atan2(t0, t1))
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.degrees(math.asin(t2))
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.degrees(math.atan2(t3, t4))
             
        return [roll_x, pitch_y, yaw_z] # in radians


def main(args=None):
    rclpy.init(args=args)

    imu_node = ImuCustomNode()

    rclpy.spin(imu_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    imu_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    try:
        main()
    except:
        pass