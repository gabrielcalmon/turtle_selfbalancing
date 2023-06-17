import rclpy
from rclpy.node import Node
import sensor_msgs.msg
import std_msgs.msg
import geometry_msgs.msg

import math, time


class ImuCustomNode(Node):

    def __init__(self):
        super().__init__('bag_recorder_node')

        self.subscriptionImu = self.create_subscription(
          sensor_msgs.msg.Imu, 
          '/imu', 
          self.imu_callback, 
          10)
        self.subscriptionImu # prevent unused variable warning
        self.quaternion=[0,0,0,0] # inicializa com valores arbitrarios
        self.euler=[0,0,0]


        self.subscriptionVel = self.create_subscription(
          geometry_msgs.msg.Twist, 
          '/cmd_vel', 
          self.vel_callback, 
          10)
        self.vel=0

        timer_period = 0.05  # periodo de amostragem (1/20hz = 0.05s)
        self.timer = self.create_timer(timer_period, self.record_csv)
        self.i = 0


    def imu_callback(self, data):
        self.quaternion=[data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
        self.euler = self.euler_from_quaternion(data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)


    def vel_callback(self, data):
        self.vel = data.linear.x
        print(self.vel)  


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


def record_csv(self):
    pass
    rclpy.loginfo(rclpy.get_caller_id() + "I heard %s", data)
    # Abre o arquivo CSV e adiciona uma nova linha com os dados atuais
    with open(filename, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # cria o cabecalho do csv CASO o arquivo esteja vazio
        if csv_file.tell() == 0:
            writer.writerow(['time', 'pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5', 'pos_6', 'vel_1', 'vel_2', 'vel_3', 'vel_4', 'vel_5', 'vel_6', 'eff_1', 'eff_2', 'eff_3', 'eff_4', 'eff_5', 'eff_6'])
        #write_list=list(data.position) + list(data.velocity) + list(data.effort)
        #formattedList = [data.header.stamp.to_sec()] + [f'%.{float_precision}f' % x for x in write_list]
        
        # concatena os dados da mensagem numa lista
        formattedList = [data.header.stamp.to_sec()] + list(data.position) + list(data.velocity) + list(data.effort)
        #formattedList = map(float, formattedList)
        writer.writerow(formattedList)


def main(args=None):
    rclpy.init(args=args)

    bag_node = ImuCustomNode()

    rclpy.spin(bag_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    bag_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    try:
        main()
    except:
        pass