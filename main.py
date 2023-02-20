from DisplayModel import *
from Model import *
from Animal import *
import sys


if __name__ == "__main__":
    model = Model(0.5 ,4, 100, 200, 100)
    """Animal.Cow(4, 100, 150, 332.75, 200, 100)"""
    display = Display(model)
    sys.exit(display.show())
    
