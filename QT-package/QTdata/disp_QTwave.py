#!/usr/local/bin/python
#encoding:utf-8

import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import json
import pdb
# project homepath
curfilepath =  os.path.realpath(__file__)
projhomepath = os.path.dirname(curfilepath)
projhomepath = os.path.dirname(projhomepath)
# configure file
with open(os.path.join(projhomepath,'ECGconf.json'),'r') as fin:
    conf = json.load(fin)
sys.path.append(projhomepath)
import codecs

import glob
import re
import pickle
import marshal


import WTdenoise.wtdenoise as wtdenoise
import QTdata.loadQTdata as QTdb

def show_drawing(folderpath = os.path.dirname(curfilepath)+'/QTdata_repo/'):
    with open(folderpath+'sel103.txt','r') as fin:
        sig = pickle.load(fin)
        # plot sig
        plt.figure(1)
        plt.subplot(211)
        mark_ind = [sig['time'][x] for x in sig['marks']['T']]
        mark_amp= [sig['sig'][x] for x in sig['marks']['T']]

        plt.plot(sig['time'],sig['sig'],'k',\
                mark_ind,mark_amp,'ro')
        plt.title('ECG signal')
        plt.xlim(mark_ind[0],mark_ind[-1])
        # denoised sig
        #plt.figure(2)
        plt.subplot(212)
        denoised_sig = wtdenoise.denoise(sig['sig'])
        mark_ind = sig['marks']['T'];
        mark_amp= [denoised_sig[x] for x in sig['marks']['T']]
        

        plt.plot(denoised_sig,'b',mark_ind,mark_amp,'ro');
        #plt.plot(sig['time'],denoised_sig,'k',\
        #        mark_ind,mark_amp,'ro')
        plt.title('WTdenoised ECG signal')
        plt.xlim(mark_ind[0],mark_ind[-1])
        plt.show()
        
        
        
def find_first_grt_than(val,array):
    ## array must be sorted
    L,R = 0,len(array)-1
    while L<=R:
       mid = int(L+(R-L)/2)
       if array[mid] == val:
           return mid
       elif array[mid] > val:
           R = mid - 1
       else:
           L = mid + 1
    if L < len(array):
        return L
    else:
        return None

def proc_time2ind(mark,time):
    time.sort()
    # find first in time val >= mark[i]
    ret = []
    for val in mark:
        ind = find_first_grt_than(val,time)
        if ind:
            ret.append(ind)
    ret.sort()
    return ret

def convert_all_mark_to_index(folderpath = './QTdata_py/'):
    #qtfiles = os.listdir(os.curdir+os.sep+'QTdata_py'+os.sep)
    files = glob.glob(os.curdir+os.sep+'QTdata_py'+os.sep+'*.txt')

    # get *.txt
    files = map(lambda x:os.path.split(x)[1],files)
    qtfiles = files

    cnt = 0
    for filename in qtfiles:
        print 'filename:',filename
        print 'fullpath:',folderpath+filename

        filepath = folderpath + filename
        filesize = os.stat(filepath).st_size
        print 'file size:',os.stat(filepath).st_size
        if filesize <= 0:
            print 'empty file!'
            continue

        with open(folderpath+filename,'rb') as fin:
            sig = pickle.load(fin)
            print 'loaded:',filename
            sig['marks']['T'] = proc_time2ind(\
                    sig['marks']['T'],sig['time'])
            sig['marks']['P'] = proc_time2ind(\
                    sig['marks']['P'],sig['time'])
            sig['marks']['R'] = proc_time2ind(\
                    sig['marks']['R'],sig['time'])
            sig['marks']['lp'] = proc_time2ind(\
                    sig['marks']['lp'],sig['time'])
            sig['marks']['rp'] = proc_time2ind(\
                    sig['marks']['rp'],sig['time'])
            # save to new file:
            with open('./QTdata_repo/'+filename,'wb') as fout:
                marshal.dump(sig,fout)
                print 'cnt = ',cnt
                cnt += 1

            print 'saved as ','./QTdata_repo/'+filename
    print '--convertion complete--'

def disp_recID(recID = 1):
    if isinstance(recID,int) == False:
        raise Exception('recID input must be integer!')
    QTloader = QTdb.QTloader()
    reclist = QTloader.getQTrecnamelist()
    sig = QTloader.load(reclist[recID])

    plt.figure(1)
    #plt.subplot(211)
    #mark_ind = [sig['time'][x] for x in sig['marks']['T']]
    #mark_amp= [sig['sig'][x] for x in sig['marks']['T']]

    plt.plot(sig['sig'],'k')
    #plt.plot(sig['time'],sig['sig'],'k',mark_ind,mark_amp,'ro')
    plt.title('ECG signal')
    #plt.xlim(mark_ind[0],mark_ind[-1])
    plt.show()
def disp_rec(recname = 'sel103'):
    QTloader = QTdb.QTloader()
    sig = QTloader.load(recname)
    pdb.set_trace()

    plt.figure(1)
    #plt.subplot(211)
    #mark_ind = [sig['time'][x] for x in sig['marks']['T']]
    #mark_amp= [sig['sig'][x] for x in sig['marks']['T']]

    plt.plot(sig['sig'],'g')
    plt.plot(sig['sig2'],'r')
    #plt.plot(sig['time'],sig['sig'],'g')
    #plt.plot(sig['time'],sig['sig2'],'r')
    plt.title('QT rec: '+recname)
    #plt.xlim(mark_ind[0],mark_ind[-1])
    plt.show()


if __name__ == '__main__':
    #show_drawing()
    #convert_all_mark_to_index()
    disp_rec(recname = 'sel103')
    #disp_recID()
