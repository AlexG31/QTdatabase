#encoding:utf-8
import os
import sys
import pickle
import json
import pdb
import glob
import marshal
import matplotlib.pyplot as plt

# project homepath
curfilepath =  os.path.realpath(__file__)
curfolderpath = os.path.dirname(curfilepath)
projhomepath = os.path.dirname(curfilepath)
projhomepath = os.path.dirname(projhomepath)
# configure file
with open(os.path.join(projhomepath,'ECGconf.json'),'r') as fin:
    conf = json.load(fin)
sys.path.append(projhomepath)

#import QTdata.loadQTdata.QTloader as QTloader
from QTdata.loadQTdata import QTloader 
from RFclassifier.ECGRF import ECGrf as ECGRF
from RFclassifier.evaluation import ECGstatistics as ECGstats
from ECGPloter.ResultPloter import ECGResultPloter

class RecSelector():
    def __init__(self):
        self.qt= QTloader()
    def inspect_recs(self):
        reclist = self.qt.getQTrecnamelist()
        set_testing= set(conf['selQTall0_test_set'])
        set_training = set(reclist) - set_testing
        
        out_reclist = set_training

        # records selected
        selected_record_list = []
        for ind,recname in enumerate(out_reclist):
            # inspect
            print '{} records left.'.format(len(out_reclist) - ind - 1)
            # plot
            QTsig = self.qt.load(recname)
            rawsig = QTsig['sig']
            # expert labels
            testresult = self.qt.getexpertlabeltuple(recname)
            poslist,labellist = zip(*testresult)
            poslist = list(poslist)
            poslist.sort()
            dispRange = (poslist[0],poslist[-1])
            resplt = ECGResultPloter(rawsig,testresult)
            resplt.plot(plotTitle = 'QT record {}'.format(recname),dispRange = dispRange)
            #self.qt.plotrec(recname)
            usethis = raw_input('Use this record as training record?(y/n):')
            if usethis == 'y':
                selected_record_list.append(recname)
            # debug
            #if ind > 2:
                #pass
        with open(os.path.join(os.path.dirname(curfilepath),'selected_training_records.json'),'w') as fout:
            json.dump(selected_record_list,fout)

    def pick_invalid_record(self):
        reclist = self.qt.getQTrecnamelist()
        invalidrecordlist = []
        for ind,recname in enumerate(reclist):
            # inspect
            print 'Inspecting record ''{}'''.format(recname)
            sig = self.qt.load(recname)
            if abs(sig['sig'][0]) == float('inf'):
                invalidrecordlist.append(recname)
        return invalidrecordlist

    def save_recs_to_img(self):
        reclist = self.qt.getQTrecnamelist()
        sel1213 = conf['sel1213']
        sel1213set = set(sel1213)
        
        out_reclist = set(reclist) - sel1213set

        for ind,recname in enumerate(reclist):
            # inspect
            print '{} records left.'.format(len(out_reclist) - ind - 1)
            #self.qt.plotrec(recname)
            self.qt.PlotAndSaveRec(recname)
            # debug
            if ind > 9:
                pass
                #print 'debug break'
                #break

    def inspect_recname(self,tarrecname):
        self.qt.plotrec(tarrecname)
    def inspect_selrec(self):
        QTreclist = self.qt.getQTrecnamelist()
        with open(os.path.join(curfolderpath,'selected_training_records.json'),'r') as fin:
            sel0115 = json.load(fin)
        #sel0115 = conf['selQTall0']
        #test_reclist = set(QTreclist) - set(sel0115)
        for ind,recname in enumerate(sel0115):
            print '{} records left.'.format(len(sel0115) - ind - 1)
            self.inspect_recname(recname)
            
    def RFtest(self,testrecname):
        ecgrf = ECGRF()
        sel1213 = conf['sel1213']
        ecgrf.training(sel1213)
        Results = ecgrf.testing([testrecname,])
        # Evaluate result
        filtered_Res = ECGRF.resfilter(Results)
        stats = ECGstats(filtered_Res[0:1])
        Err,FN = stats.eval(debug = False)

        # write to log file
        EvalLogfilename = os.path.join(projhomepath,'res.log')
        stats.dispstat0(\
                pFN = FN,\
                pErr = Err)
        # plot prediction result
        stats.plotevalresofrec(Results[0][0],Results)
                #LogFileName = EvalLogfilename,\
                #LogText = 'Statistics of Results in [{}]'.\
                    #format(RFfolder)\
                #)
        #ECGstats.stat_record_analysis(pErr = Err,pFN = FN,LogFileName = EvalLogfilename)
        



def pickout_invalid_files():
    recsel = RecSelector()
    invalideList = recsel.pick_invalid_record()
    print invalideList
    # find those signals only contains 'inf'
    with open('invalid_records.json','w') as fout:
        json.dump(invalideList,fout)

if __name__ == "__main__":
    #pickout_invalid_files()
    #sys.exit()

    recsel = RecSelector()
    #recsel.inspect_recname('sel46')
    #recsel.save_recs_to_img()
    #recsel.inspect_recs()
    recsel.inspect_selrec()

    print '-'*30


