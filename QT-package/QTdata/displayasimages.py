#encoding:utf-8
import os
import sys
import pickle
import json
import glob
import marshal
import matplotlib.pyplot as plt
import pdb

class VectorImage:
    def __init__(self):
        pass
    def save2image(self,sigvec,savefolder,dispWinLen,dispWinGap,winnum = 1):
        plt.figure(num = 1,figsize = (20,10))
        Labels = self.getexpertlabeltuple(recname)

        lpos = [x[0] for x in Labels]
        Amps = [sig['sig'][x] for x in lpos]
        plt.plot(sig['sig'])
        plt.plot(lpos,Amps,'ro')
        # text box
        #bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="cyan", ec="b", lw=2)
        #t = ax.text(0, 0, "Direction", ha="center", va="center", rotation=45,size=15,bbox=bbox_props)
        xylist = zip(lpos,Amps)
        for ind,xy_val in enumerate(xylist):
            plt.annotate(s= Labels[ind][1],xy = xy_val)
        # xlim
        x_left = lpos[0]-100
        #x_right = lpos[-1]+100
        x_right = x_left + xWinLen
        plt.xlim(x_left,x_right)

        plt.title(recname)
        plt.savefig(os.path.join(savefolderpath,recname+'.png'))
        #plt.show()
        plt.clf()
        
