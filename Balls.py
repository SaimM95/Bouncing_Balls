#-------------------------------------------------------------------------------
# Name:        Ball.py
#
# Author:      Saim Malik
#
# Description: This program simulates an animation of balls bouncing around
#              the window and off of each other using graphics.py.
#              (The collisions are somewhat unstable, any help is welcomed)
#-------------------------------------------------------------------------------

# Make all the necessary imports
from graphics import *
from time import sleep
from _thread import start_new_thread
from random import randint
from math import sqrt

# The Main function creates and displays everything
def main():
    # CHANGE THESE NUMBERS TO YOUR LIKING
    #####################################
    windowSize = [500,500]              # Size of window to draw (default: 500x500)
    numOfBalls = 5                      # Number of balls to draw (default: 5)
    ballRadius = 30                     # Radius of each ball (default: 30)
    ballSpeed = [2,3]                   # Speed of each ball in X and Y directions (default: 2,3)
    #####################################

    # Create a 500x500 window with the title "Balls"
    win = GraphWin("Balls",windowSize[0],windowSize[1])

    # Initialize the booleans for the threads and an empty list to store the balls in
    runThread = True
    runDrawThread = True
    circles = []

    # Start a new thread using the 'drawShapes' function and pass in the required arguments
    # (This basically draws the required number of balls (given by the user) on the window)
    start_new_thread(drawShapes,(circles,win,runDrawThread,numOfBalls,ballRadius,windowSize))

    # Get a mouse click from the user to que the animation to start
    win.getMouse()

    # Stop the drawing thread
    runDrawThread = False

    # Loop through all the balls inside the circles list and animate them (using 'animation' function)
    # Note: This makes each ball run on it own thread
    for c in circles:
        start_new_thread(animation,(c,runThread,circles,ballRadius,windowSize,ballSpeed))

    # Get a mouse click from the user to que the animation to stop and terminate the program
    win.getMouse()
    runThread = False

    win.close()

# Draws all the balls in random positions inside the window
def drawShapes(circles,win,runDrawThread,balls,radius,winSize):
    # Set upper and lower limits on x and y coordinates to assure the entire ball gets drawn inside the window
    xLower = radius + 20
    yLower = radius + 20
    xUpper = winSize[0] - radius - 20
    yUpper = winSize[1] - radius - 20

    # Initialize random x and y coordinates and an empty list to store them
    pX = randint(xLower,xUpper)
    pY = randint(yLower,yUpper)
    pXYs = []

    # Create a ball and place it somewhere randomly ('balls' represents the number of balls to draw)
    for i in range(balls):
        # Add the coordinates to the list 'pXY'
        pXYs.append([pX,pY])

        # Make sure the balls don't overlap using the 'check' function on each ball before drawing it
        # If it does overlap, generate new random coordinates for the ball
        while runDrawThread == True:
            if check(pX,pY,pXYs,radius) == True: break
            else:
                pX = randint(xLower,xUpper)
                pY = randint(yLower,yUpper)

        # Add the current ball to the 'circles' list and then draw it inside the window
        # ('radius' represents the radius of the ball being drawn)
        circles.append(Circle(Point(pX,pY),radius))
        circles[i].draw(win)

# Animates one ball in a way so it bounces off the edges of the window and off other balls
def animation(c,runThread,circles,radius,winSize,speed):
    # Put X, -X, Y and -Y speed vectors inside a list; pick a random one out of the 4 possible x,y
    # combinations to make each ball move in a random direction
    # Note: Doing this does not make balls move at different speeds, just in different directions
    xs = [speed[0],-1*speed[0]]
    ys = [speed[1],-1*speed[1]]

    x = xs[randint(0,1)]
    y = ys[randint(0,1)]

    # Keep animating the ball until the user asks for it to be stopped
    while runThread == True:
        # Update the state of the ball every 0.01 seconds
        sleep(0.01)

        # Get the x,y coordinates of the center of the ball
        x1, y1 = c.getCenter().getX(), c.getCenter().getY()

        # Loop through all the balls being animated and check for collisions
        for circ in circles:
            # If the ball being checked is not the current ball, then check the distance b/w that ball
            # and the current ball; if it is less than or equal to the diameter (2*radius), then there
            # is a collision

            ## Using this collision analogy causes somewhat of an unstable animation; any input on
            ## fixing this is welcomed

            # In case of a collision, move the current ball in the opposite direction (x=-x, y=-y)
            # NOTE: This works b/c each ball is running on its own thread so all the balls involved in
            #       the collision react the same way
            if circ != c:
                x2, y2 = circ.getCenter().getX(), circ.getCenter().getY()
                distance = round(sqrt(((x2-x1)**2)+((y2-y1)**2)))
                if abs(distance) <= (2*radius):
                    x = -1*x
                    y = -1*y
                    break

        # Get the center coordinates of the ball and get the distance b/w the center and boundaries
        centerX, centerY = c.getCenter().getX(), c.getCenter().getY()
        distanceX = round(winSize[0]-centerX)
        distanceY = round(winSize[1]-centerY)

        # Check if the ball is hitting the boundaries; change direction of the ball if it is
        if abs(distanceX) <= radius or centerX <= radius: x = -1*x
        if abs(distanceY) <= radius or centerY <= radius: y = -1*y

        # Move the ball based on the current (x,y) vector
        c.move(x,y)

# Checks if the coordinates of the ball being drawn overlap with any other ball already in the window
# Returns False if it does, True if there is no overlap
def check(x1,y1,x2y2,radius):
    # Loop through x,y coordinates of every ball currently in the window
    for xy in x2y2:
        # If the distance b/w the ball that is about to be drawn and the ball that is already there is less
        # than their radii combined, return False (i.e. Balls are touching or overlapping)
        x2,y2 = xy[0],xy[1]

        distance = round(sqrt(((x2-x1)**2)+((y2-y1)**2)))
        if abs(distance) <= (2*radius):
            return False

    # If the test passes with all balls, return True
    return True

# Run the main function
if __name__ == '__main__':
    main()
