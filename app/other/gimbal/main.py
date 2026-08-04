'''
# Copyright (c) [2026] [01Studio]. Licensed under the MIT License.

实验名称：二维舵机云台两路舵机控制
实验平台：01Studio cybercam + 二维舵机云台（含pyMotors驱动板）
说明：控制二维舵机云台的两路舵机
'''

#导入相关模块
import busio, board
import os,sys

# 当前文件夹下相对路径，绝对路径（app离线部署）
local_lib_path = "./lib"
system_lib_path = "/data/app/gimbal/lib"

# 判断优先使用路径
if os.path.exists(os.path.join(local_lib_path, "adafruit_motor")) or os.path.exists(os.path.join(local_lib_path, "adafruit_pca9685")):
    target_path = os.path.abspath(local_lib_path)
# 使用系统绝对路径（IDE运行调试）
elif os.path.exists(os.path.join(system_lib_path, "adafruit_motor")) or os.path.exists(os.path.join(system_lib_path, "adafruit_pca9685")):
    target_path = system_lib_path
else:
    raise FileNotFoundError("文件缺失，请检查当前路径与系统路径下的文件是否存在。")

# 找到的路径插入到 sys.path 最前面（确保优先加载它）
sys.path.insert(0, target_path)

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

#构建I2C对象，推荐频率小于10KHz
i2c = busio.I2C(board.SCL2, board.SDA2)

#构建PCA9685对象
pca = PCA9685(i2c, address=0x40)
#设置pwm输出频率
pca.frequency = 50

#构建二维云台2路舵机对象
servo_x = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500, actuation_range=270)
servo_y= servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500, actuation_range=180)

#初始位置，可以修改角度观察现象
servo_x.angle = 135 #水平（X轴）使用使用端口0，转到135°
servo_y.angle = 90 #垂直（Y轴）使用使用端口1，转到90°

while True:
    pass