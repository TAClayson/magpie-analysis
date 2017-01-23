class Material:
    def __init__(self, material="steel"):
        self.material=material
        
        self.resTempAlpha
        
    def Conductivity(self, temperature=0):
        #temp in kelvin
        #linear approximation from "Magnetic Fields" Heinz E. Knoepfel page 473 onwards
        #if above debyeTemp
        debyeTemp = self.DebyeTemp()
        return debyeTemp*debyeTemp / temperature
        
    def DebyeTemp(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 506 onwards
        #return in kelvin
        return {
            'Aluminium' : 390, #24-ST
            'Iron' : 420,
            'Brass' : 320,
            'Copper' : 320,
            'Lead' : 88,
            'Tungsten' : 350,
        }[self.material]
    
    def Conductivity(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 476 onwards
        #return conductivity at room temperature and pressure in g/cc
        return {
            'Brass' : 15.7,
            'Chromium' : 27.2
        }[self.material]
    
    def Density(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 506 onwards
        #return density at room temperature and pressure in g/cc
        return {
            'Aluminium' : 2.71, #24-ST
            'Iron' : 7.8,
            'Brass' : 8.5,
            'Copper' : 8.93,
            'Lead' : 11.3,
            'Tungsten' : 19.3,
        }[self.material]