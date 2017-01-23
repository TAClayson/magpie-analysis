#Code built for disecting shot names and finding the files and folders on Linna
#assumes standard format: sMMDD_YY

import os

class Shot:
    def __init__(self, shotName=""):
        self.shotName=shotName
        #get the date
        self.month = int(shotName[1:3])
        self.day = int(shotName[3:5])
        self.year = int(shotName[6:8])
        if self.year>90: #handling Y2K
            self.yearLong = 1900+self.year
        else:
            self.yearLong = 2000+self.year

        self.path = "//LINNA/Users/Magpie/Documents/MAGPIE data/" + str(self.yearLong)

        #there are several options for the month folders
        monthsLong = ['January','February','March','April','May','June','July','August', 'September','October','November','December']
        monthsShort = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug', 'Sep','Oct','Nov','Dec']
        self.TryFolder(self.path, monthsLong[self.month-1])
        self.TryFolder(self.path, monthsLong[self.month-1]+"_"+str(self.yearLong))
        self.TryFolder(self.path, monthsLong[self.month-1]+"_"+str(self.year))
        self.TryFolder(self.path, monthsLong[self.month-1]+" "+str(self.yearLong))
        self.TryFolder(self.path, monthsShort[self.month-1])
        self.TryFolder(self.path, monthsShort[self.month-1]+"_"+str(self.yearLong))
        self.TryFolder(self.path, monthsShort[self.month-1-1]+"_"+str(self.year))
        self.TryFolder(self.path, monthsShort[self.month-1]+" "+str(self.yearLong))
        
        #find the actual shot folder
        for subfolder in os.listdir(self.path):
            if subfolder[0:8]==self.shotName:
                self.folder = subfolder
                print("Folder found: "+self.path+"/"+self.folder)

    def TryFolder(self, rootfolder="", subfolder=""):
        if os.path.isdir(rootfolder+"/"+subfolder):
            self.path = rootfolder+"/"+subfolder
        if os.path.isdir(rootfolder+"/"+subfolder.lower()):
            self.path = rootfolder+"/"+subfolder.lower()