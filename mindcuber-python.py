from turtle import speed
import ev3_dc as ev3
import time

from scanner.scan import Cube
import kociemba


def wait():
    while rotate.busy:
        pass
    time.sleep(0.1)


def waitT():
    while turnn.busy:
        pass
    time.sleep(0.1)


def release():
    rotate.start_move_to(20, speed=35, brake=True)
    wait()
    rotate.start_move_for(1, speed=5, direction=-1)
    wait()

def rot(dir=1, release=0):
    # print(dir, release)
    for i in range(dir):
        cube.flip()

    if release == 0 or release == 1:
        cube.push_flipper_away()


def hold_cube():
    current_position = rotate.position
    if (current_position <= 90 or current_position >= 110):
        rotate.start_move_to(100, speed=30)
    cube.wait_flipper()

def turn(dir=1, times=1):
    if times == 1:
        turnn.start_move_by(-270*dir, speed=100, brake=True)
        waitT()
    if times == 2:
        turnn.start_move_by(-540*dir, speed=100, brake=True)
        waitT()
    if times == 3:
        turnn.start_move_by(270*dir, speed=100, brake=True)
        waitT()
    if times == 4:
        turnn.start_move_by(2160*dir, speed=100, brake=True)
        waitT()


def fix_rotate():
    pass
    # turnn.start_move_by(10,speed=80, brake=True)

# solve the cube


def solve():
    print("-------------------------")

    stepCount = 1

    steps = stepstr.split()

    faceDown = "D"

    hold_cube()

    stepIndex = 0

    for step in steps:
        print("Step: "+str(stepCount) + " of "+str(len(steps)) + " - " + step)
        stepCount += 1

        if step.endswith("'"):
            turnTimes = 3
        elif step.endswith("2"):
            turnTimes = 2
        else:
            turnTimes = 1

        try:
            if faceDown == "D":
                if step.startswith("D"):
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("U"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("F"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "U"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "U"

            elif faceDown == "U":
                if step.startswith("U"):
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("D"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("F"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "D"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "D"

            elif faceDown == "F":
                if step.startswith("F"):
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("B"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("U"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("D"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "B"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "B"

            elif faceDown == "B":
                if step.startswith("B"):
                    turn(1, turnTimes)
                    faceDown = "B"
                elif step.startswith("F"):
                    rot(2, -1)
                    turn(1, turnTimes)
                    faceDown = "F"
                elif step.startswith("D"):
                    rot(1, -1)
                    turn(1, turnTimes)
                    faceDown = "D"
                elif step.startswith("U"):
                    rot(3, -1)
                    turn(1, turnTimes)
                    faceDown = "U"
                elif step.startswith("R"):
                    release()
                    turn(-1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(-1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "F"
                elif step.startswith("L"):
                    release()
                    turn(1, 1)
                    rot(1, -1)
                    turn(1, turnTimes)
                    rot(1, 1)
                    turn(1, 1)
                    if not (steps[stepIndex+1].startswith("R") or steps[stepIndex+1].startswith("L")):
                        hold_cube()
                    faceDown = "F"
        except:
            pass
        time.sleep(0.1)
        stepIndex += 1

    seconds = time.time()-timeItTakes
    minutes, seconds = divmod(seconds, 60)
    if str(seconds)[1] == ".":
        seconds = "0"+str(seconds)[0]
    else:
        seconds = str(seconds)[:2]
    print("Final time = " + str(minutes)[0] + ":" + str(seconds))

    release()


if __name__ == "__main__":
    ev3device = ev3.EV3(protocol=ev3.USB, host='00:16:53:83:D8:4D')

    rotate = ev3.Motor(ev3.PORT_A, ev3_obj=ev3device)  # big motor (arm)
    turnn = ev3.Motor(ev3.PORT_B, ev3_obj=ev3device)  # big motor (platform)
    ultrasonic = ev3.Ultrasonic(ev3.PORT_1, ev3_obj=ev3device)

    cube = Cube(ev3device, rotate, turnn)
    patternchoice = input("Enter 1 to solve. Enter 2 for checkerboard. Enter 3 for cube in cube in cube. Enter 4 for cross:")

    while patternchoice != '1'and patternchoice != '2' and patternchoice != '3' and patternchoice != '4':
        patternchoice = input("Invalid input! Please enter again: ")

    print("Please insert cube!")

    while True:
        if ultrasonic.distance < 1.5:
            break
        time.sleep(0.1)

    print("Cube detected!")
    time.sleep(1)

    timeItTakes = time.time()
    cubestr = cube.scan()
    if patternchoice == '1':
        stepstr = kociemba.solve(cubestr)
    elif patternchoice == '2':
        stepstr = kociemba.solve(cubestr,"UDUDUDUDURLRLRLRLRFBFBFBFBFDUDUDUDUDLRLRLRLRLBFBFBFBFB")
    elif patternchoice == '3':
        stepstr = kociemba.solve(cubestr,"LUBUUBBBBDDDRRDFRDRRRRFFRFDFDRFDDFFFBLULLUUUULBULBBLLL")
    elif patternchoice == '4':
        stepstr = kociemba.solve(cubestr,"DUDUUUDUDBRBRRRBRBLFLFFFLFLUDUDDDUDUFLFLLLFLFRBRBBBRBR")

    print(stepstr)
    solve()
    turn(dir=1,times=4)
    time.sleep(5)
