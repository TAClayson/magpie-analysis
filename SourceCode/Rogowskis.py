from SourceCode.Bdots import *

class Rogowskis:
    def __init__(self, shot, returnPosts, threshold=0.25, attenuators =[10*10.4, -10.48*10.79] ):
        self.shot=shot
        self.returnPosts = returnPosts
        self.attenuators = attenuators
        #rogowski 1 and 2
        self.bd1=ScopeChannel(shot, '2', 'c1')
        self.bd2=ScopeChannel(shot, '2', 'c2')
        self.truncate(threshold)
        self.integrate()
        #output data
        print("Current start: "+str( self.time[0] )+" ns")
        print("Peak current: "+str(self.Imax)+" MA")
    def truncate(self, threshold=0.25, window=1000, cal=[3e9,3e9]):
        #find the start of the current pulse with a  high threshold
        sig1=self.bd1.data
        start=np.nonzero(abs(sig1)>threshold)[0][0]
        #back off a bit so we can see the zero signal
        self.start=start-50
        #zero the data
        z1=np.mean(self.bd1.data[0:200]) 
        z2=np.mean(self.bd2.data[0:200])
        #truncate arrays
        self.time=self.bd1.time[self.start:self.start+window]
        self.bd1_tr=(self.bd1.data[self.start:self.start+window]-z1)
        self.bd2_tr=(self.bd2.data[self.start:self.start+window]-z2)
        #multiply by scale factors to get dI/dt
        self.dIdt1 = self.bd1_tr*cal[0]*self.attenuators[0]
        self.dIdt2 = self.bd2_tr*cal[1]*self.attenuators[1]
    def integrate(self, min_signal=5e4):
        #perform integration on both signals
        self.I1=scipy.integrate.cumtrapz(self.dIdt1,self.time)/1e9
        self.I2=scipy.integrate.cumtrapz(self.dIdt2,self.time)/1e9
        #check currents are positive:
        i1=self.I1
        if np.abs(self.I1.max())<np.abs(self.I1.min()):
            self.I1=-self.I1
        if np.abs(self.I2.max())<np.abs(self.I2.min()):
            self.I2=-self.I2
        #check that there's a signal
        if self.I2.max()<min_signal:
            self.I_Tot=self.I1*self.returnPosts
            print(self.shot+": using Rog 1 only")
        if self.I1.max()<min_signal:
            self.I_Tot=self.I2*self.returnPosts
            print(self.shot+": using Rog 2 only")
        if self.I1.max()>5e4 and self.I2.max()>5e4:
            self.I_Tot=(self.I1+self.I2)*self.returnPosts/2.0
            print(self.shot+": using both Rogs")
            
        self.time_I=self.time[:-1]
        #self.t0=self.time_I[np.where(self.I_Tot>2e3)[0][0]]
        #self.time_0ed=self.time_I-self.t0
        self.Imax=self.I_Tot.max()/1e6
    def plot(self, data, ax=None, scale=1, bdname=None):
        if ax is None:
            fig, ax=plt.subplots()
        if data is "raw":
            t=self.bd1.time
            d1=self.bd1.data
            d2=self.bd2.data
            l1='R1 raw'
            l2='R2 raw'
        if data is "tr":
            t=self.time
            d1=self.bd1_tr
            d2=self.bd2_tr
            l1='R1 truncated'
            l2='R2 truncated'
        if data is "dIdt":
            t=self.time
            d1=self.dIdt1
            d2=self.dIdt2
            l1='R1 dI/dt'
            l2='R2 dI/dt'
        if data is "I":
            t=self.time_I
            d1=self.I1
            d2=self.I2
            l1='I1'
            l2='I2'
        if data is "total":
            t=self.time_I
            d1=self.I_Tot
            d2=None
            l1=self.shot+' Current'
        if data is "I_Tot0":
            t=self.time_0ed
            d1=self.I_Tot
            d2=None
            l1=self.shot+' Current'
        ax.plot(t, scale*d1, label=l1, lw=4)
        if d2 is not None:
            ax.plot(t, scale*d2, label=l2, lw=4)
        ax.legend()