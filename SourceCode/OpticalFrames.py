#class for managing optical framing camera and images
#assumes the images are located in a subfolder with a background and shot subfolder

#__init__(self, shotName, start, IF)
    #sets up the camera, searches for the images and loads them all
    #shotName as a string
    #start = start time in ns
    #IF = inter-frame time in ns
#plot(self, toPlot="shots" array=None, frame=1, clim=None, ax=None)
    #plots a single image
    #toPlot = string specifying what to plot
        #"shot" = shot images
        #"background" = background images
        #"raw" = raw shot images
    #array = manually pass the array of images
    #frame = frame to plot, 1 to 12
#plot_sequence(self, toPlot="shot", array=None, frames=list(range(1,13)), clim=None, figsize=None)
    #plots a sequence of images
    #toPlot = string specifying what to plot
        #"shot" = shot images
        #"background" = background images
        #"raw" = raw shot images
    #array = manually pass the array of images
    #frames = frames to plot, 1 to 12
    

import numpy as np
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import csv
import images2gif as ig
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import rotate
import matplotlib.gridspec as gridspec

from SourceCode.ShotNames import *

class OpticalFrames:
    def __init__(self, shotName, start, IF):
        self.shot = Shot(shotName)
        self.shotName = shotName
        
        #find the fast frame /12 frame folder
        self.folder = ""
        self.path = self.shot.path+"/"+self.shot.folder
        for subfolder in os.listdir(self.path):
            if subfolder[-10:]=="fast frame":
                self.folder = subfolder
            elif subfolder[-10:]=="fast-frame":
                self.folder = subfolder
            elif subfolder[-8:]=="12 frame":
                self.folder = subfolder
            elif subfolder[-8:]=="12-frame":
                self.folder = subfolder
            elif subfolder==self.shotName:
                self.folder = subfolder
        
        if self.folder=="": #do we have a folder?
            print("No optical framing folder found")
            return
        else:
            print("Optical frame folder found: "+self.folder)
        
        self.start=start
        self.IF=IF
        self.frame_times=np.arange(start, start+12*IF, IF)
        self.load_images()
        self.normalise()
        
        
        
    def load_images(self):
        backgrounds=[]
        shots=[]
        rootPath = self.path+"/"+self.folder
        
        #see if the files are located in the root folder
        for i in range(1,13):
            if i<10:
                st="0"+str(i)
            else:
                st=str(i)
            bk_fn=rootPath+"/"+self.shotName+" Background_0"+st+".tif"
            if os.path.isfile(bk_fn):
                bk_im=plt.imread(bk_fn) #read background image
                #bk_im=np.asarray(np.sum(bk_im,2), dtype=float)
                backgrounds.append(bk_im)#np.asarray(np.sum(bk_im,2), dtype=float)) #convert to grrayscale
            sh_fn=rootPath+"/"+self.shotName+" Shot_0"+st+".tif" 
            if os.path.isfile(sh_fn):
                sh_im=plt.imread(sh_fn)
                shots.append(sh_im)
        
        #find the shot folder
        shotPath = ""
        if os.path.isdir(rootPath+"/shot"):
            shotPath = rootPath+"/shot"
        #load shot images
        if shotPath!="":
            print("Searching: "+shotPath)
            for i in range(1,13):
                if i<10:
                    st="_00"+str(i)
                else:
                    st="_0"+str(i)
                sh_fn=shotPath+"/"+self.shotName+st+".tif"
                if os.path.isfile(sh_fn):
                    sh_im=plt.imread(sh_fn)
                    shots.append(sh_im)
                else:
                    print("File missing: "+sh_fn)

        #find the background folder
        backPath = ""
        if os.path.isdir(rootPath+"/back"):
            backPath = rootPath+"/back"
        elif os.path.isdir(rootPath+"/background"):
            backPath = rootPath+"/background"
        elif os.path.isdir(rootPath+"/ref"):
            backPath = rootPath+"/ref"
        #load background images
        if shotPath!="":
            print("Searching: "+shotPath)
            for i in range(1,13):
                if i<10:
                    st="_00"+str(i)
                else:
                    st="_0"+str(i)
                sh_fn=shotPath+"/"+self.shotName+st+".tif"
                if os.path.isfile(sh_fn):
                    sh_im=plt.imread(sh_fn)
                    backgrounds.append(sh_im)
                else:
                    print("File missing: "+sh_fn)
           
        self.shots = shots
        self.backgrounds = backgrounds
        
        
        
    def normalise(self):
        norms=[b_im.sum() for b_im in self.backgrounds] #sums over the background image to get a normal scale
        n_max=max(norms)
        nn=[n/n_max for n in norms]
        self.normalised=[s_im/n for s_im, n in zip(self.shots, nn)]
        
        
        
    def logarithm(self, lv_min=-4, lv_max=0.2):
        self.s_l=[np.log(s_im) for s_im in self.s_n]
        self.s_nl=[(np.clip(s_im, a_min=lv_min, a_max=lv_max)-lv_min)/(lv_max-lv_min) for s_im in self.s_l]
        
        
        
    def rotate(self, angle_deg=0):
        self.s_r=[rotate(s_im, angle_deg)for s_im in self.s_nl]
        
        
        
    def crop(self, origin, xcrop=400, ycrop=400):
        x0=origin[1]
        y0=origin[0]
        self.origin=[ycrop,xcrop]
        self.s_c=[s_im[y0-ycrop:y0+ycrop,x0-xcrop:x0+xcrop] for s_im in self.s_r]        
        
        
        
    def plot(self, toPlot="shot", array=None, frame=1, clim=None, ax=None):
        if array is None:
            if toPlot is "shot":
                array = self.normalised
            elif toPlot is "background":
                array = self.backgrounds
            elif toPlot is "raw":
                array = self.shots
            
        fin=frame-1
        if ax is None:
            fig, ax=plt.subplots(figsize=(12,8))
        ax.imshow(array[fin], cmap='afmhot', clim=clim)
        ax.axis('off')
        ax.set_title('t='+str(self.frame_times[fin])+' ns', fontsize=22)
        
        
        
    def plot_norm(self, frame=1, clim=None, ax=None):
        self.plot(self.s_n, frame=frame, clim=clim, ax=ax)
        
        
        
    def plot_log(self, frame=1, clim=None, ax=None):
        self.plot(self.s_nl, frame=frame, clim=clim, ax=ax)
        
        
        
    def plot_rot(self, frame=1, clim=None, ax=None):
        self.plot(self.s_r, frame=frame, clim=clim, ax=ax)
        
        
        
    def plot_crop(self, frame=1, clim=None, ax=None):
        self.plot(self.s_c, frame=frame, clim=clim, ax=ax)
        
        
        
    def plot_sequence(self, toPlot="shot", array=None, frames=list(range(1,13)), clim=None, figsize=None):
        xframes=round(len(frames)/3)
        if array is None:
            if toPlot is "raw":
                array = self.shots
            elif toPlot is "background":
                array = self.backgrounds
            elif toPlot is "shot":
                array = self.normalised
                
        if figsize is None:
            figsize=(xframes*4,16)
        fig, ax=plt.subplots(3,xframes, figsize=figsize)
        ax=ax.flatten()
        for fin, f in enumerate(frames):
            fn=f-1 #shift to 0 indexed arrays
            a=ax[fin]
            a.imshow(array[fn], cmap='afmhot', clim=clim)
            a.axis('off')
            a.set_title('t='+str(self.frame_times[fn])+' ns', fontsize=22)
        fig.suptitle("Optical framing images from "+self.shot.shotName, fontsize=32)
        fig.tight_layout(w_pad=0, h_pad=0)
        self.fig=fig
        
        
        
    def save_sequence(self, filename=None):
        if filename is None:
            filename=self.shot+" frame sequence"
        self.fig.savefig(filename+".png")
        
        
        
    def create_lineout(self, axis=0, frame=1,centre=None,average_over_px=20, mm_range=10, scale=29.1, ax=None):
        px_range=mm_range*scale
        fn=frame-1 #shift to 0 indexed arrays
        if axis is 1:
            d=np.transpose(self.s_c[fn])
            y0=self.origin[1] if centre is None else centre
            x0=self.origin[0]
        if axis is 0:
            d=self.s_c[fn]
            y0=self.origin[0] if centre is None else centre
            x0=self.origin[1]
        section=d[y0-average_over_px:y0+average_over_px, x0-px_range:x0+px_range]
        self.lo=np.mean(section, axis=0)
        self.mm=np.linspace(-px_range, px_range, self.lo.size)/scale
        if ax is None:
            fig, ax=plt.subplots(figsize=(12,8))
        ax.plot(self.mm, self.lo, label='t='+str(self.frame_times[fn])+' ns', lw=4)
        
        
        
    def make_movie(self, clim=[0,1]):
        w=6
        h=w/self.s_c[0].shape[1]*self.s_c[0].shape[0]
        fig, ax=plt.subplots(figsize=(w,h))
        hot_im=[]
        for im in self.s_c:
            ax.imshow(im, cmap='afmhot', clim=clim)
            plt.axis('off')
            fig.tight_layout()
            fig.canvas.draw()
            w,h=fig.canvas.get_width_height()
            buf=np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
            buf.shape=(h,w,3)
            hot_im.append(buf)
        shfn=self.shot+" Shot"
        ig.writeGif(shfn+'.gif',hot_im, duration=0.2)