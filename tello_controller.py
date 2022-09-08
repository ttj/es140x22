# This is a simple control program for the DJI/Ryze Tello 
# drone, using the tellopy library. This one in 
# particular is configured to demonstrate the 
# interface to the simulator in tello_simulator.py.

# To use it with the physical Tello hardware, one needs 
# to simply comment out the IP address override, on 
# the line with "drone.tello_addr = ('127.0.0.1', 8889)".

# the sleep function is used to 
# add a wait, built-in to Python
from time import sleep

# include the Tello library we are using
# will only work after executing the installation 
# via pip install tellopy
import tellopy

# event handler for showing received messages 
# from the Tello
def handler(event, sender, data, **args):
    drone = sender
    # display flight data received 
    # from the Tello
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

# main tello function
def telloProgram():
    # instantiate the Tello drone object
    drone = tellopy.Tello()

    # override ip address for physical tello drone to 
    # localhost (127.0.0.1) for simulation
    # if using the physical drone, comment out
    # this next line
    drone.tello_addr = ('127.0.0.1', 8889)
    
    # try to run, if there's an error, handle exceptions
    try:
        # set up event handler above to be called when 
        # we receive data from the Tello
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        # set up the connection to the Tello
        drone.connect()
        # wait a little
        drone.wait_for_connection(60.0)
        
        # take off
        drone.takeoff()
        
        # wait about 1 second so drone is in the air
        sleep(1)

        # use a variable wait (in seconds) for a common wait between commands
        wait = 5
        
        # use a variable v for the velocity
        # this is a percentage of the maximum velocity, 
        # so v should be between 0 and 100
        v = 50
        
        drone.left(v) # send command to go left with velocity v
        sleep(wait) # continue going left for wait seconds
        
        drone.right(v) # send command to go right with velocity v
        sleep(2) # wait for 2 seconds
        
        drone.forward(v) # send command to go forward with velocity v
        # commands are ADDITIVE: the drone is now going right and forward, 
        # so these vectors (right at velocity v, forward at velocity v) have 
        # been added together
        sleep(2) # wait 2 seconds
        
        drone.left(v)
        sleep(2)
        
        # stop x and y velocities
        # to stop the drone, send a 0 velocity along all axes
        # stop left/right movement: send a left/right with 0 velocity
        # stop forward/backward movement: send a forward/backward with 0 velocity
        # stop up/down, clockwise/counter_clockwise similarly
        
        # opposite command
        drone.right(0)
        sleep(0.1) # wait about 0.1 seconds
        drone.backward(0)
        sleep(0.1)
        
        
        # land
        drone.land()
        
        # wait some time for drone to land
        sleep(3)
    # if an error occurs during execution, 
    # display what happened
    except Exception as ex:
        print(ex)
    # even if an error occurs, execute next part
    # this closes the network connection, which 
    # we always need to do even if there is 
    # an error
    finally:
        # close connection and destroy objects
        drone.quit()

# call the telloProgram function above as the main entry point
if __name__ == '__main__':
    telloProgram()
