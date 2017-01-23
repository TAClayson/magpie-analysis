import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import scipy.integrate
import math

class Liner:
    def __init__(self, material="steel", length=20, diameter=10.5, thickness=200):
        self.material=material
        self.length=length
        self.diameter=diameter
        self.thickness=thickness
        
        #calculate resistance
        resistivity = 75e-8
        self.initRes = resistivity * length/1000 / 2 / math.pi / (diameter/2000) / (thickness/1e6)