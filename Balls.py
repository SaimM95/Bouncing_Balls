from graphics import *
from time import sleep
from _thread import start_new_thread
from random import randint
from math import sqrt

def main():
    win = GraphWin("Balls",500,500)
    runThread = True
    runDrawThread = True
    circles = []

    start_new_thread(drawShapes,(circles,win,runDrawThread))

    win.getMouse()
    runDrawThread = False

    for c in circles:
        start_new_thread(animation,(c,runThread,circles))

    win.getMouse()
    runThread = False

    win.close()

def drawShapes(circles,win,runDrawThread):
    pX = randint(50,450)
    pY = randint(50,450)
    pXYs = []

    for i in range(5):
        pXYs.append([pX,pY])

        while runDrawThread == True:
            if check(pX,pY,pXYs) == True: break
            else:
                pX = randint(50,450)
                pY = randint(50,450)

        circles.append(Circle(Point(pX,pY),30))
        circles[i].draw(win)
        txt = Text(Point(pX,pY),i+1)
        txt.draw(win)


def animation(c,runThread,circles):
    xs = [2,-2]
    ys = [3,-3]

    x = xs[randint(0,1)]
    y = ys[randint(0,1)]

    while runThread == True:
        sleep(0.01)

        x1, y1 = c.getCenter().getX(), c.getCenter().getY()

        for circ in circles:
            if circ != c:
                x2, y2 = circ.getCenter().getX(), circ.getCenter().getY()
                distance = round(sqrt(((x2-x1)**2)+((y2-y1)**2)))
                if abs(distance) <= 60:
                    x = -1*x
                    y = -1*y
                    break

        cBottom = (c.getCenter().getY()) + 30
        cTop = (c.getCenter().getY()) - 30
        cRight = (c.getCenter().getX()) + 30
        cLeft = (c.getCenter().getX()) - 30

        if cBottom >= 500 or cTop <= 0: y = -1*y
        if cRight >= 500 or cLeft <= 0: x = -1*x
        c.move(x,y)

def check1(lstX,lstY,circ):
    leftEdge = circ.getP1().getX()
    rightEdge = circ.getP2().getX()
    topEdge = circ.getP1().getY()
    bottomEdge = circ.getP2().getY()

    ans = False
    for x in lstX:
        if ((leftEdge <= x+30) and (leftEdge >= x-30)) or ((rightEdge <= x+30) and (rightEdge >= x-30)):
            ans = True
##            for y in lstY:
##                if ((numY-30 <= ly+30) and (numY-30 >= ly-30)) or ((numY+30 <= ly+30) and (numY+30 >= ly-30)):
##                    print(True)
##                    ans = True
##                    break
##        break

    return ans

def check(x1,y1,x2y2):
    ans = True
    for xy in x2y2:
        x2,y2 = xy[0],xy[1]
        form = round(sqrt(((x2-x1)**2)+((y2-y1)**2)))
        if abs(form) <= 60:
            ans = False
            break
    return ans

if __name__ == '__main__':
    main()
