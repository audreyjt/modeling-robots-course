# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle
import eml4806.graphics.workspace as workspace
import eml4806.sensor.keyboard as keyboard
import eml4806.robot.skidsteer as skidsteer
import eml4806.graphics.shape as shape
import eml4806.geometry.transform as transform

def main():

    # Land
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0
    
    yard = workspace.Area(xmin, xmax, ymin, ymax)
    ax = yard.axis

    #c1 = shape.Circle(ax, -1, 0, 0.5, color="blue", opacity=0.5)
    r1 = shape.Rectangle(ax, 1.2, 0.5)
    #c2 = shape.Circle(ax, 1, 0, 0.5, color="green", opacity=0.5)
    #g = shape.Group([c1, c2])

    angle = 0.0
    d = 0.1
    
    while True:
        # Commands
        key = keyboard.key()

        if key == 'q':
            break
        elif key == 'r':
            angle += 0.1
            r1.transform = transform.Transform(orientation=angle)
            print(angle)
        #elif key == 'm':
        #    c1.shift(0,d)
        #    r1.shift(0,d)
        #    c2.shift(0,d)
        #elif key == 'g':
        #    g.move(4, 4)
           
        yard.update()
    
    print("Bye!")

if __name__ == "__main__":
    main()
