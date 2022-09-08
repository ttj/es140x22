# DJI/Ryze Tello Simulator
# Author: Taylor Johnson, Vanderbilt, Fall 2020
# This is a minimalistic simulator for the Tello.
# It presents a graphical view of one Tello from 
# overhead. Control programs (e.g., tello_controller.py) 
# can be used with minor modification to control a 
# simulated Tello drone or an actual physical Tello 
# drone. 

# This minimal approach does not require any external libraries except 
# for the tellopy one needed to talk with the Tello drone, and 
# instead uses the tkinter library.

# ES140x students do not need to understand everything in this file, but 
# advanced students may be interested to understand it or modify it adding features.

# To install the tellopy library, from a console/terminal:
#
# pip install tellopy

from tkinter import *
import tellopy
import socket
from time import sleep
# these next imports make it
# so that we don't have to do like 
# tellopy.internal.protocol.TAKEOFF_CMD
# and can instead refer to it as
# just TAKEOFF_CMD
from tellopy._internal import *
from tellopy._internal.protocol import *

TELLO_COLOR = "#0492CF"
COLOR_TEXT = "#000000"

tello_size_x = 10 # width of tello at ground
tello_size_y = 10 # height of tello at ground
board_x = 400 # size of canvas/board
board_y = 400 # size of canvas/board
min_height = 0 # minimum altitude (ground)
max_height = 100 # maximum altitude
max_v = 7 # maximum velocity

# definition for tello simulation and gui
# note: to do this fully properly, we would make this 
# concurrent with e.g. threads, but keeping it simple so it's 
# at least partially understandable
# if we did it that way, we'd have threads for the gui redrawing, 
# threads for the networking send/receives, etc.
# however, this is sufficient as is for our purposes
class TelloSim(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.canvas = Canvas(self.master, width=board_x, height=board_y)
        self.canvas.pack()

        self.master.update()

        # starts up simulation
        self.simulationLoop()
        
    # sets up connection to tello program
    def startupConnection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 8889))
        self.sock.settimeout(2.0)

        # probably for the video data, unused
        self.sock_setup = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_setup.bind(('127.0.0.1', 9617))
        self.sock_setup.settimeout(2.0)

        # initial connection receipt
        data, addr = self.sock.recvfrom(2000)
        print(data)
        print(addr) # ok so far, has received, need to reply back
        s = "conn_ack: ok" # first part must be conn_ack: (with the colon)
        self.sock.sendto(s.encode(), addr)

    # main simulation loop, starts connection then proceeds
    def simulationLoop(self):
        # initialize connection to tello program
        self.startupConnection()

        # x,y,z positions of drone, and orientation theta
        x = board_x/2
        y = board_y/2
        z = 0 # height, todo: will need to pull into appropriate values for tello data
        theta = 0 # orientation

        # x,y,z velocities of drone, and angular velocity vtheta
        vx = 0
        vy = 0
        vz = 0
        vtheta = 0
        
        # last stick command from tello, ignores updates if same
        # as prior (this gets sent periodically)
        lastStick = None
        
        # repeatedly receive/send data to tello application program
        # interpret tello commands
        # update physical simulation variables (positions, angles, velocities)
        while True:
            # update positions based on received velocity commands
            x = x + vx
            y = y + vy
            z = z + vz
            theta = theta + vtheta
            
            try:
                # receive command from tello
                data, addr = self.sock.recvfrom(2000)

                # check data for command types
                pkt = Packet(data)
                cmd = uint16(data[5], data[6])

                if cmd == TAKEOFF_CMD:
                    print('TAKEOFF RECV')
                    # abstracted to just set height
                    z = 20
                    # TODO: could use +vz velocity
                elif cmd == LAND_CMD:
                    print('LAND RECV')
                    # abstracted to just set height
                    z = 0
                    # TODO: could use -vz velocity
                elif cmd == STICK_CMD:
                    # only update if stick command differs from last receipt
                    if not lastStick == None:
                        if not lastStick == pkt.get_buffer():
                            print('STICK CMD RECV')
                            print(pkt.get_data())
                            stick_cmd = pkt.get_data()

                            # convert back to 11-bit representation from packed bytes
                            # 8 bits + 3 bits
                            axis1 = stick_cmd[0] | ((stick_cmd[1] & 0x07) << 8)
                            # 5 bits + 6 bits
                            axis2 = ((stick_cmd[1] & 0xf8) >> 3) | ((stick_cmd[2] & 0x3f) << 5)
                            # 2 bits + 8 bits + 1 bit
                            axis3 = ((stick_cmd[2] & 0xc0) >> 6) | ((stick_cmd[3] & 0xff) << 2) | ((stick_cmd[4] & 0x01) << 10)
                            # 7 bits + 4 bits
                            axis4 = ((stick_cmd[4] & 0xfe) >> 1) | ((stick_cmd[5] & 0x0f) << 7)
                            # ignore axis 5
                
                            # convert 11-bit representation back to percentage
                            right_x = int(100 * (axis1 - 1024)/660.0)
                            right_y = int(100 * (axis2 - 1024)/660.0)
                            left_y = int(100 * (axis3 - 1024)/660.0)
                            left_x = int(100 * (axis4 - 1024)/660.0)
                            
                            # convert to 20% specified percentage in appropriate velocity
                            vx = int(right_x * 0.2)
                            vy = int(right_y * 0.2)
                            vz = int(left_y * 0.2)
                            vtheta = int(left_x * 0.2)

                    lastStick = pkt.get_buffer()
                else:
                    print('COMMAND UNSUPPORTED')

                # periodic flight info, most fields currently bogus
                # TODO: could link to simulation parameters (speed, height, etc.)
                # and add a function that creates the packet bits
                # based on that info (e.g., flightMsg(speed,height))
                m = [START_OF_PACKET, 2, 3, 4, 5, FLIGHT_MSG, 0x00, 8, 9, 10]
                self.sock.sendto(bytearray(m), addr)
                sleep(0.1)
            except Exception as e:
                print(e)

            # constrain velocities            
            if vx > max_v:
                vx = max_v
            if vx < -max_v:
                vx = -max_v
            if vy > max_v:
                vy = max_v
            if vy < -max_v:
                vy = -max_v
            if vz > max_v:
                vz = max_v
            if vz < -max_v:
                vz = -max_v
            if vtheta > max_v:
                vtheta = max_v
            if vtheta < -max_v:
                vtheta = max_v

            # constraint positions                
            if x > (board_x - tello_size_x):
                x = board_x - tello_size_x
            if x < 0:
                x = 0
            if y > (board_y - tello_size_y):
                y = board_y - tello_size_y
            if y < 0:
                y = 0
            
            if z > max_height:
                z = max_height
            if z < min_height:
                z = min_height

            # TODO: handle rotations based on theta, would also need to transform velocities
            xrot = x
            yrot = y
            xrotSize = x+tello_size_x+z
            yrotSize = y+tello_size_y+z
            
            # redraw canvas showing new tello position
            self.canvas.delete("all")
            self.canvas.create_rectangle(xrot,yrot,xrotSize,yrotSize, fill=TELLO_COLOR, outline=TELLO_COLOR)
            text_status = 'x: ' + str(int(x)) + ' y: ' + str(int(y)) + ' z: ' + str(int(z)) + ' th: ' + str(int(theta))
            self.canvas.create_text(
                    150,
                    25,
                    font="cmr 18 bold",
                    fill=COLOR_TEXT,
                    text=text_status,
            )
            text_status = 'vx: ' + str(int(vx)) + ' vy: ' + str(int(vy)) + ' vz: ' + str(int(vz)) + ' vth: ' + str(int(vtheta))
            self.canvas.create_text(
                    150,
                    40,
                    font="cmr 18 bold",
                    fill=COLOR_TEXT,
                    text=text_status,
            )
            # update after delay of 100ms
            self.master.after(100, self.master.update())

    # create other gui elements
    def create_widgets(self):
        self.quit = Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

# main startup of gui and simulation
root = Tk()
sim = TelloSim(master=root)
sim.mainloop()
