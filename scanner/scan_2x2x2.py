# credit: https://github.com/cavenel/ev3dev_examples/blob/master/python/pyev3/rubiks.py
# Modified to use ev3_dc
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import ev3_dc as ev3
from time import sleep, time
from scanner.read_rgb import RGB
from rubikscolorresolver import resolve_colors


class ScanError(Exception):
    pass


class Cube():
    def __init__(self, ev3device, flipper, rotate):
        self.flipper = flipper
        self.rotate = rotate
        self.sensor_arm = ev3.Motor(ev3.PORT_C, ev3_obj=ev3device)

        self.rotate_ratio = 3

        self.color_sensor = ev3.Color(ev3.PORT_2, ev3_obj=ev3device)
        self.distance_sensor = ev3.Ultrasonic(ev3.PORT_1, ev3_obj=ev3device)

        self.rgb = RGB(ev3device)
        self.scan_order = [
            2, 1, 3, 4,
            10,9,11,12,
            22,21,23,24,
            7,8,6,5,
            20,18,17,19,
            16,14,13,15
        ]

        self.cube = {}
        self.rotate_speed = 40
        self.hold_cube_pos = 100
        self.corner_to_edge_diff = 10

        self.init_motors()

        self.white = []

        self.colors = {}
        self.k = 0

    def wait_rotate(self):
        while self.rotate.busy:
            pass
        sleep(0.1)

    def wait_flipper(self):
        while self.flipper.busy:
            pass
        sleep(0.1)

    def wait_sensor_arm(self):
        while self.sensor_arm.busy:
            pass
        sleep(0.1)

    def init_motors(self):
        print("Initializing motors")
        self.rotate.position = 0  # reset

        self.flipper.start_move(direction=-1, speed=30)
        self.sensor_arm.start_move(direction=1, speed=30)
        sleep(2)

        self.flipper.stop(brake=True)
        self.flipper.position = 0  # reset

        self.sensor_arm.stop(brake=True)
        self.sensor_arm.position = 0  # reset

        print("Motors initialized")

    def calibrate_rgb(self):
        self.rotate.start_move_to(45*self.rotate_ratio, speed=40, brake=True)
        sleep(2)
        self.white = self.rgb.read_rgb(calibrate=True)
        self.rotate.start_move_to(0*self.rotate_ratio, speed=40, brake=True)
        print("White: ", self.white)
        sleep(2)

    def scan(self):
        self.scan_face(1)

        self.flip()
        self.scan_face(2)

        self.flip()
        self.scan_face(3)

        self.rotate_cube(-1, 1)
        self.flip()
        self.scan_face(4)

        self.rotate_cube(1, 1)
        self.flip()
        self.scan_face(5)

        self.flip()
        self.scan_face(6)

        self.rotate_cube(-1, 1)
        self.flip()
        self.rotate_cube(-1, 1)
        #self.rotate_cube(-1, 1)
        # self.flip()

        self.push_flipper_away()
        #self.rotate_cube(1, 2)

        colors_str = str(self.colors)
        colors_str = colors_str.replace("'", '"')
        # print(colors)
        with open("output.json", "w") as output_file:
            output_file.write(colors_str)
        solve_steps = resolve_colors(["", "--filename", "output.json"])
        return solve_steps

    def flip(self):
        current_position = self.flipper.position
        self.rotate.stop(brake=True)
        if (current_position <= self.hold_cube_pos-10 or current_position >= self.hold_cube_pos+10):
            self.flipper.start_move_to(
                self.hold_cube_pos, speed=30, brake=True)
            self.wait_flipper()

        self.flipper.start_move_to(185, speed=60, brake=True)
        self.wait_flipper()

        sleep(0.2)

        self.flipper.start_move_to(self.hold_cube_pos, speed=20, brake=True)
        #self.flipper.start_move_to(0, speed=30, brake=True)
        self.wait_flipper()

    def rotate_cube(self, direction, nb):
        if self.flipper.position > 35:
            self.push_flipper_away()

        final_dest = 135 * \
            round((self.rotate.position + 270 * direction * nb) / 135.0)

        self.rotate.start_move_to(
            final_dest, speed=self.rotate_speed, brake=True)
        self.wait_rotate()
        self.rotate.stop(brake=True)

    def scan_face(self, index):
        print("Scanning face", index)

        if self.flipper.position > 35:
            self.push_flipper_away()

        i = 1
        self.put_color_sensor_edge()
        if index == 1:
            self.calibrate_rgb()
            

        self.wait_rotate()
        self.rotate.stop(brake=True)
        self.rotate.position = 0
        self.rotate.start_move_to(360*self.rotate_ratio, speed=40, brake=True)

        while self.rotate.busy:
            current_position = self.rotate.position
            if current_position >= (i*270)-135:
                # sleep(0.1)
                current_color = self.rgb.read_rgb(self.white)
                self.colors[str(self.scan_order[self.k])] = current_color
                print("Face:", index, "current position:",
                      i, "current color:", current_color)
                i += 1
                self.k += 1

                if i == 5:
                    if index == 6:
                        self.remove_arm()
                    else:
                        self.remove_arm_halfway()
        if i < 5:
            raise ScanError("i is %d..should be 4" % i)

        self.wait_rotate()
        self.rotate.stop(brake=True)
        self.rotate.start_move_to(360*self.rotate_ratio, speed=40, brake=True)
        self.rotate.position = 0

    def push_flipper_away(self):
        self.flipper.start_move(direction=-1, speed=30)
        sleep(1)

        self.flipper.stop(brake=True)
        self.flipper.position = 0

    def put_color_sensor_edge(self):
        self.sensor_arm.start_move_to(-660, speed=50, brake=True)
        self.wait_sensor_arm()

    def remove_arm(self):
        self.sensor_arm.start_move(direction=1, speed=40)
        sleep(2)
        self.sensor_arm.stop(brake=True)
        self.sensor_arm.position = 0

    def remove_arm_halfway(self):
        self.sensor_arm.start_move_to(-400, speed=50, brake=True)
        self.wait_sensor_arm()

    def disable_brake(self):
        self.rotate.stop(brake=False)
        self.flipper.stop(brake=False)
        self.sensor_arm.stop(brake=False)


if(__name__ == "__main__"):
    ev3device = ev3.EV3(protocol=ev3.USB, host='00:16:53:83:D8:4D')

    rotate = ev3.Motor(ev3.PORT_A, ev3_obj=ev3device)  # big motor (arm)
    turnn = ev3.Motor(ev3.PORT_B, ev3_obj=ev3device)  # big motor (platform)

    cube = Cube(ev3device, rotate, turnn)
    cube.flip()
    cube.disable_brake()
