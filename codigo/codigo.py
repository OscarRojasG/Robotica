import serial
import time
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Timer

app = Flask(__name__)
CORS(app)

json_data = None

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(json_data)


############################# ARDUINO #############################


SPEED = 130
lock = False
arduino = serial.Serial('COM5', 9600, timeout=3)

def write_speed(speed1, speed2):
    global arduino
    arduino.write(f"{speed1},{speed2}\n".encode())

def request_lock():
    global lock
    lock = True

def release_lock():
    global lock
    lock = False

def move_forward():
    write_speed(SPEED, SPEED)

def move_right():
    write_speed(1.2 * SPEED, SPEED)

def move_left():
    write_speed(SPEED, 1.2 * SPEED)

def turn_right():
    def rotate():
        write_speed(SPEED, -SPEED)
        Timer(0.26, release_lock).start()

    request_lock()
    stop()
    Timer(0.25, rotate).start()

def turn_back():
    write_speed(8,8)

def stop():
    write_speed(0,0)


if __name__ == "__main__":
    #threading.Thread(target=lambda: app.run()).start()
    start_time = time.time()
    time.sleep(1)

    while True:
        try:
            line = arduino.readline().decode().strip()

            data = line.split(',')
            data = list(map(int, data))

            fl = data[0]
            cl = data[1]
            cc = data[2]
            cr = data[3]
            fr = data[4]
            ls = data[5]
            rs = data[6]

            if not lock:
                if fr == 0:
                    turn_right()
                elif fl == 1 and cl == 1 and cr == 0 and fr == 1:
                    move_left()
                elif fl == 1 and cl == 0 and cr == 1 and fr == 1:
                    move_right()
                elif cc == 0:
                    move_forward()
                else:
                    stop()

            json_data = {
                "sensors": [fl, cl, cc, cr, fr],
                "speed": {
                    "left": ls,
                    "right": rs
                },
                "timestamp": round(time.time() - start_time, 2)
            }

            print(data)

        except Exception as e:
            print(e)
            print("Error de lectura")