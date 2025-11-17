# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle
import eml4806.sensor.keyboard as keyboard
import eml4806.robot.skidsteer as skidsteer

from eml4806.graphics.workspace import Workspace
from eml4806.geometry.transform import Transform
from eml4806.graphics.style import Color, Stroke, Fill, Style
from eml4806.graphics.shape import Group, Rectangle, Circle

def main():

    # Land
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0
    
    workspace = Workspace(xmin, xmax, ymin, ymax)
    c1 = Circle(workspace, 3, 4, 0.5)
    r1 = Rectangle(workspace, 2, 1, 1.2, 0.5)
    c2 = Circle(workspace, 3, 3, 2)
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
            r1.rotate(angle)
            print(angle)
        #elif key == 'm':
        #    c1.shift(0,d)
        #    r1.shift(0,d)
        #    c2.shift(0,d)
        #elif key == 'g':
        #    g.move(4, 4)
           
        workspace.update()
    
    print("Bye!")

if __name__ == "__main__":
    main()
