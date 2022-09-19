import math
from tkinter import *
import tellopy 
from threading import Thread
#import cv2 # to enable opencv, run pip install opencv-python, then uncomment
import time
from time import sleep # so we can call sleep(x) and not have to use time.sleep(x)
import os, numpy
from main_students import *

#Global Variables
# to refer to global variables inside a function, need the following:
# global var1, var2, var3 # where the varN are different variables separated by commas
distanceEntry = None
sideLengthEntry = None
drone = tellopy.Tello()
stream_on = False
frameRead = None
capture = None

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        self.waitControl = 2 # time to wait in seconds between control commands (up, down, etc.)
        self.velocity = 25

        self.pack(fill=BOTH, expand=1)
        # Initializing the Buttons for the GUI
        exitButton = Button(self, text="Exit", command=self.clickExitButton) # Exit button 
        takeoffButton = Button(self, text="Takeoff",command=self.clickTakeoffButton) # Takeoff button 
        landButton = Button(self, text="Land", command=self.clickLandButton) # Land button 
        shapesButton = Button(self, text="Shapes", command=self.clickShapesButton) # Shapes Menu button 
        cameraButton = Button(self, text="Camera", command=self.clickCameraButton) # Camera Menu button 
        generalControlButton = Button(self,text="General Controls", command=self.clickControlButton) # General Drone Control Menu button 
        # Placing the buttons for the GUI in a grid layout
        takeoffButton.grid(row=0,column=1)
        landButton.grid(row=0,column=3)
        generalControlButton.grid(row=1,column=2)
        shapesButton.grid(row=2, column=1)
        cameraButton.grid(row=2, column=3)
        exitButton.grid(row=3,column=2)
        
    # Lands the drone and quits the program on the press of the Exit button   
    def clickExitButton(self):
        global frameRead
        drone.land()
        drone.quit()
        exit()

    # Loads the drone basic control window 
    def clickControlButton(self):
        global root, drone, distanceEntry
        # Brings the window to the front
        controlWindow = Toplevel(root)
        # Titles the window "Drone Control Interface"
        controlWindow.title("Drone Control Interface")
        # Sets the geometry of the window to 320 x 200
        controlWindow.geometry("320x200")
        # Creating the label and entry box for getting the desired distance
        distanceLabel = Label(controlWindow, text="Distance:")
        distanceEntry = Entry(controlWindow)
        # Initializing the Buttons for the basic drone controls: Up, Down, Left, Right, Forward, Backward
        upButton = Button(controlWindow, text="Up", command=self.clickUpButton)
        downButton = Button(controlWindow, text="Down", command=self.clickDownButton)
        leftButton = Button(controlWindow, text="Left", command=self.clickLeftButton)
        rightButton = Button(controlWindow, text="Right", command=self.clickRightButton)
        forwardButton = Button(controlWindow, text="Forward",command=self.clickForwardButton)
        backwardButton = Button(controlWindow, text="Backward",command=self.clickBackwardButton)
        returnButton = Button(controlWindow, text="Return to Main", command=self.clickReturnButton)
        # Place the label and entry box for getting the desired distance
        distanceLabel.grid(row=0, column=1)
        distanceEntry.grid(row=0, column=2)
        # Placing the buttons in a grid layout
        upButton.grid(row=1,column=2)
        downButton.grid(row=3, column=2)
        leftButton.grid(row=2, column=1)
        rightButton.grid(row=2, column=3)
        forwardButton.grid(row=4, column=1)
        backwardButton.grid(row=4, column=3)
        returnButton.grid(row=5, column=2)
        self.controlWindow= controlWindow
        self.shapesWindow = None
        self.cameraWindow = None
        self.circleWindow = None
        self.triangleWindow = None
        self.cubeWindow = None
        self.squareWindow = None

    # Function that activates when you click the up button
    def clickUpButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Up {}".format(length))
        drone.connect()
        drone.takeoff()
        time.sleep(1) 
        self.moveUp(length)
        drone.land()

    # Function that tells the drone to move upward, called by the clickUpButton
    def moveUp(self, distance):
        # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance upward command using the drone SDK command
        
        #upDist = "up {}".format(distance)
        #drone.sock.sendto(upDist.encode('utf-8'), drone.tello_addr)
        drone.up(self.velocity)
        time.sleep(self.waitControl)
        drone.down(0)

    # Function that activates when you click the down button
    def clickDownButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Down %d" %(length))
        drone.connect()
        drone.takeoff()
        time.sleep(1)
        self.moveDown(length)
        drone.land()

    # Function that tells the drone to move downward, called by the clickDownButton
    def moveDown(self, distance):
       # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance downward command using the drone SDK command
        
        
        print('unsupported')

    # Function that activates when you click the left button
    def clickLeftButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Left {}".format(length))
        drone.connect()
        drone.takeoff()
        time.sleep(1)
        self.moveLeft(length)
        drone.land()


    # Function that tells the drone to move left, called by the clickLeftButton
    def moveLeft(self, distance):
       # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance left command using the drone SDK command
        
        
        print('unsupported')

    # Function that activates when you click the right button
    def clickRightButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Right {}".format(length))
        drone.connect()
        drone.takeoff()
        self.moveRight(length)
        drone.land()

    # Function that tells the drone to move right, called by the clickRightButton
    def moveRight(self, distance):
        # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance right command using the drone SDK command
        
        print('unsupported')

    # Function that activates when you click the forward button
    def clickForwardButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Forward {}".format(length))
        drone.connect()
        drone.takeoff()
        time.sleep(1)
        self.moveForward(length)
        drone.land()

    # Function that tells the drone to move forward, called by the clickForwardButton
    def moveForward(self, distance):
        # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance forward command using the drone SDK command
        
        print('unsupported')


    # Function that activates when you click the backward button
    def clickBackwardButton(self):
        global drone, distanceEntry
        length = int(distanceEntry.get())
        print("Going Backward {}".format(length))
        drone.connect()
        drone.takeoff()
        time.sleep(5)
        self.moveBackward(length)
        time.sleep(1)
        drone.land()

    # Function that tells the drone to move backward, called by the clickBackwardButton
    def moveBackward(self, distance):
        # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to distance backward command using the drone SDK command
        
        print('unsupported')

    # Function that tells the drone to move clockwise
    def moveClockwise(self, angle):
        # Using the global variable drone to communicate with the drone
        global drone
        # Set variable to angle to rotate clockwise command using the drone SDK command
        
        print('unsupported')

    # Function that activates when you click the takeoff button
    def clickTakeoffButton(self):
        global drone
        drone.connect()
        drone.takeoff()
        time.sleep(2)
        print("Takeoff")

    # Function that activates when you click the land button
    def clickLandButton(self):
        global drone
        print("Land")
        drone.connect()
        sleep(1)
        
        # send zero velocities along all degrees of freedom
        drone.up(0)
        sleep(0.1)
        drone.forward(0)
        sleep(0.1)
        drone.left(0)
        sleep(0.1)
        drone.clockwise(0)
        sleep(0.1)
        
        # send land
        drone.land()
        sleep(2)

    # Function that activates when you click the shapes button
    def clickShapesButton(self):
        global root
        shapesWindow = Toplevel(root)
        shapesWindow.title("Shapes Interface")
        shapesWindow.geometry("320x200")
        circleButton = Button(shapesWindow, text="Circle", command=self.clickCircleButton)
        squareButton = Button(shapesWindow, text="Square", command=self.clickSquareButton)
        cubeButton = Button(shapesWindow, text="Cube", command=self.clickCubeButton)
        triangleButton = Button(shapesWindow, text="Triangle", command=self.clickTriangleButton)
        returnButton = Button(shapesWindow, text="Return to Main", command=self.clickReturnButton)
        returnButton.place(x=105, y=180)
        circleButton.place(x=103, y=30)
        squareButton.place(x=173, y=30)
        triangleButton.place(x=103, y=80)
        cubeButton.place(x=173, y=80)
        self.shapesWindow= shapesWindow
        self.cameraWindow = None
        self.circleWindow = None
        self.triangleWindow = None
        self.cubeWindow = None
        self.squareWindow = None

    # Function that activates when you click the camera button
    def clickCameraButton(self):
        global root
        cameraWindow = Toplevel(root)
        cameraWindow.title("Camera Interface")
        cameraWindow.geometry("320x200")
        photoButton = Button(cameraWindow, text="Take a Photo", command=self.clickPhotoButton)
        videoButton = Button(cameraWindow, text="Record a Video", command=self.clickVideoButton)
        returnButton = Button(cameraWindow, text="Return to Main", command=self.clickReturnButton)
        photoButton.place(x=75,y=75)
        videoButton.place(x=175,y=75)
        returnButton.place(x=115, y=180)
        self.shapesWindow = None
        self.cameraWindow = cameraWindow
        self.cubeWindow = None
        self.triangleWindow = None
        self.squareWindow = None
        self.circleWindow = None

    # Function that activates when you click the circle button
    def clickCircleButton(self):
        global root, drone, sideLengthEntry
        # drone = drone.drone()
        circleWindow = Toplevel(root)
        circleWindow.title("Circle Interface")
        circleWindow.geometry("320x200")
        sideLengthLabel = Label(circleWindow, text="Radius:")
        sideLengthEntry = Entry(circleWindow)
        returnButton = Button(circleWindow, text="Return to Shapes Main", command=self.clickReturnButton)
        drawButton = Button(circleWindow, text="Draw Circle", command=self.drawCircle)
        sideLengthLabel.grid(row=0, column=0)
        sideLengthEntry.grid(row=0, column=1)
        drawButton.grid(row=1, column=1)
        returnButton.grid(row=4, column=1)
        self.shapesWindow = None
        self.cubeWindow = None
        self.triangleWindow = None
        self.squareWindow = None
        self.circleWindow  = circleWindow
        self.cameraWindow = None

    # Function that activates when you click the square button
    def clickSquareButton(self):
        global root, drone, sideLengthEntry
        squareWindow = Toplevel(root)
        squareWindow.title("Square Interface")
        squareWindow.geometry("320x200")
        sideLengthLabel = Label(squareWindow, text="Side Length:")
        sideLengthEntry = Entry(squareWindow)
        returnButton = Button(squareWindow, text="Return to Shapes Main", command=self.clickReturnButton)
        drawButton = Button(squareWindow, text="Draw Square", command=self.drawSquare)
        sideLengthLabel.grid(row=0, column=0)
        sideLengthEntry.grid(row=0, column=1)
        drawButton.grid(row=1, column=1)
        returnButton.grid(row=4, column=1)
        self.shapesWindow = None
        self.cubeWindow = None
        self.triangleWindow = None
        self.squareWindow = squareWindow
        self.circleWindow = None
        self.cameraWindow = None

    # Function that activates when you click the triangle button
    def clickTriangleButton(self):
        global root, drone, sideLengthEntry
        triangleWindow = Toplevel(root)
        triangleWindow.title("Triangle Interface")
        triangleWindow.geometry("320x200")
        sideLengthLabel = Label(triangleWindow, text="Side Length:")
        sideLengthEntry = Entry(triangleWindow)
        returnButton = Button(triangleWindow, text="Return to Shapes Main", command=self.clickReturnButton)
        drawButton = Button(triangleWindow, text="Draw Triangle", command=self.drawTriangle)
        sideLengthLabel.grid(row=0, column=0)
        sideLengthEntry.grid(row=0, column=1)
        drawButton.grid(row=1, column=1)
        returnButton.grid(row=4, column=1)
        self.shapesWindow = None
        self.cubeWindow = None
        self.triangleWindow = triangleWindow
        self.squareWindow = None
        self.circleWindow = None
        self.cameraWindow = None

    # Function that activates when you click the cube button
    def clickCubeButton(self):
        global root, drone, sideLengthEntry
        cubeWindow = Toplevel(root)
        cubeWindow.title("Cube Interface")
        cubeWindow.geometry("320x200")
        sideLengthLabel = Label(cubeWindow,text="Side Length:")
        sideLengthEntry = Entry(cubeWindow)
        returnButton = Button(cubeWindow, text="Return to Shapes Main", command=self.clickReturnButton)
        drawButton = Button(cubeWindow, text="Draw Cube", command=self.drawCube)
        sideLengthLabel.grid(row=0, column=0)
        sideLengthEntry.grid(row=0, column=1)
        drawButton.grid(row=1, column=1)
        returnButton.grid(row=4, column=1)
        self.shapesWindow = None
        self.cubeWindow = cubeWindow
        self.triangleWindow = None
        self.squareWindow = None
        self.circleWindow = None
        self.cameraWindow = None

    # Function that tells the drone to draw a Triangle 
    def drawTriangle(self):
        # Using the global variable drone to communicate with the drone, and sideLengthEntry to get the value from the GUI
        global drone, sideLengthEntry

        if sideLengthEntry is None:
            sideLengthEntry = 1

        triangle(drone)
        
    # Function that tells the drone to draw a Circle
    def drawCircle(self):
        # Using the global variable drone to communicate with the drone, and sideLengthEntry to get the value from the GUI
        global drone, sideLengthEntry
        
        if sideLengthEntry is None:
            sideLengthEntry = 1

        circle(drone)

    # Function that tells the drone to draw a Square    
    def drawSquare(self):
        # Using the global variable drone to communicate with the drone, and sideLengthEntry to get the value from the GUI
        global drone, sideLengthEntry
        
        if sideLengthEntry is None:
            sideLengthEntry = 1

        square(drone)

    # Function that tells the drone to draw a Cube
    def drawCube(self):
        # Using the global variable drone to communicate with the drone, and sideLengthEntry to get the value from the GUI
        global drone, sideLengthEntry
        
        if sideLengthEntry is None:
            sideLengthEntry = 1
        
        cube(drone)
        

    # Function that activates when you click the Photo button 
    def clickPhotoButton(self):
        print('unsupported')
#        import takePictureStudent
        

    # Function that activates when you click the Video button 
    def clickVideoButton(self):
        print('unsupported')
#        import recordVideoStudent
               

    # Function executed when return to previous menu
    def clickReturnButton(self):
        if self.cameraWindow is not None:
            self.cameraWindow.destroy()
            self.cameraWindow = None
        elif self.shapesWindow is not None:
            self.shapesWindow.destroy()
            self.shapesWindow = None
        elif self.cubeWindow is not None:
            self.cubeWindow.destroy()
            self.cubeWindow = None
        elif self.triangleWindow is not None:
            self.triangleWindow.destroy()
            self.triangleWindow = None
        elif self.squareWindow is not None:
            self.squareWindow.destroy()
            self.squareWindow = None
        elif self.circleWindow is not None:
            self.circleWindow.destroy()
            self.circleWindow = None
        elif self.controlWindow is not None:
            self.controlWindow.destroy()
            self.controlWindow = None

