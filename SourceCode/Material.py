class Material:
    def __init__(self, material="iron"):
        
        material = material.lower()
        #common corrections
        if material=='steel':
            material = 'AISI 304'
        if material=='stainless steel':
            material = 'AISI 304'
        
        self.material = material
        
        #self.resTempAlpha
        
    def Conductivity(self, temperature=0):
        #temp in kelvin
        #linear approximation from "Magnetic Fields" Heinz E. Knoepfel page 473 onwards
        #if above debyeTemp
        debyeTemp = self.DebyeTemp()
        return debyeTemp*debyeTemp / temperature
        
    def DebyeTemp(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 506 onwards
        #return in kelvin
        
        dic = {
            'aluminium' : 390, #24-ST
            'iron' : 420,
            'brass' : 320,
            'copper' : 320,
            'lead' : 88,
            'tungsten' : 350,
        }
        
        return dic.setdefault(self.material, 420)
    
    def Conductivity(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 476 onwards
        #return conductivity at room temperature and pressure in g/cc
        dic = {
            'brass' : 15.7e6,
            'chromium' : 27.2e6,
            'iron' : 11.3e6,
            'aluminium' : 39.2e6,
            'tungsten' : 5.5e6,
            'aisi 304' : 1.38e6, #stainless steel
        }
        return dic.setdefault(self.material, 10e6)
    
    def Density(self):
        #"Magnetic Fields" Heinz E. Knoepfel page 506 onwards
        #return density at room temperature and pressure in g/cc
        dic = {
            'aluminium' : 2.71, #24-ST
            'iron' : 7.8e3,
            'brass' : 8.5e3,
            'copper' : 8.93e3,
            'lead' : 11.3e3,
            'tungsten' : 19.3e3,
            'aisi 304' : 8.03e3, #stainless steel
        }
        return dic.setdefault(self.material, 7.8)