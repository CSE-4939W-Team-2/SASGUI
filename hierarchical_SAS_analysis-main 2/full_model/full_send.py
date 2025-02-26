import numpy as np
from sklearn.model_selection import StratifiedKFold
import argparse
import pandas as pd
import os
import sys
sys.path.append('..')
sys.path.append('../krr')
sys.path.append('../hierarchical')
import loaders
#import sas_krr_reg as spreg
import hierarchical as hier
from sklearn.svm import SVC
from sklearn.metrics import classification_report as CR
from sklearn.metrics import accuracy_score as AS
from matplotlib import pyplot as plt
from sklearn.kernel_ridge import KernelRidge as KRR
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('--targets', default = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere'], nargs = '+')
   parser.add_argument('--datadir', default = '../data')
   parser.add_argument('--dataset', default = 'newlar2')
   parser.add_argument('--test_dataset', default=None)
   parser.add_argument('--projection', type=bool, default=False)
   parser.add_argument('--logfile', default='hierarchical_log.csv')
   parser.add_argument('--struct_strings', default=['svc_10_10 ','svc_10_10 ','svc_10_10 ','svc_10_10 ', 'svc_10_10'], nargs='+')
   parser.add_argument('--shuffle', type=bool, default = False)
   parser.add_argument('--n_splits', default=10)
   parser.add_argument('--experimental', type=bool, default = False)
   parser.add_argument('--reg_file', type = str, default='regression_hypers.py')
   return(parser.parse_args())


def parse_pfile(pfile):
   data_conversions = {'alpha':float,'gamma':float,'kernel':str,'degree':int,'coeff0':float}
   pdict = {}
   infile = open(pfile, 'r')
   for line in infile.readlines():
       tokens = line.split()
       ps = {}
       for i in range(len(tokens)):
           #print(tokens[i])
           t = tokens[i]
           if t.replace('-','').strip() == 'target':
               targ = tokens[i+1].strip()
           elif t.replace('-','').strip() == 'param':
               p = tokens[i+1].strip()
           elif t[:2] == '--':
               pname = tokens[i].replace('-','').strip()
               pf = data_conversions[pname]
               ps[pname] = pf(tokens[i+1])
       if targ not in pdict.keys():
           pdict[targ] = {}
       pdict[targ][p]=ps
       #print('T')
       #print(t)
       #print(p)
       #print(pdict[targ][p])
   return(pdict)

           
def construct_regressor(pfile, gamma_norm):
    rdict = {}
    pdict = parse_pfile(pfile)
    for t in pdict.keys():
        if t not in rdict.keys():
            rdict[t] = {}
        for p in pdict[t].keys():
            if pdict[t][p]['kernel'] == 'polynomial':
                regressor = KRR(alpha = pdict[t][p]['alpha'], gamma = pdict[t][p]['gamma']/gamma_norm, degree = pdict[t][p]['degree'], kernel = pdict[t][p]['kernel'], coef0 = pdict[t][p]['coeff0'])
            else:
                regressor = KRR(alpha = pdict[t][p]['alpha'], gamma = pdict[t][p]['gamma']/gamma_norm, kernel = pdict[t][p]['kernel'].lower(), coef0 = pdict[t][p]['coeff0'])
            rdict[t][p] = regressor
    return(rdict)

def load_all_params(pdict, datadir, dataset):
    train_params = {}
    test_params = {}
    #print(pdict)
    for t in pdict.keys():
        train_params[t] = {}
        for p in pdict[t].keys():
          train_params[t][p] = loaders.load_params('%s/%s/train_%s_%s.csv'%(datadir, dataset, t, dataset), [p])[p]
    return(train_params)

def train_all_regression(train_spec, train_params, regressors):
    for t in train_params.keys():
        for p in train_params[t].keys():
            #print('%s %s'%(t, p))
            #print(train_params[t][p])
            regressors[t][p] = regressors[t][p].fit(train_spec[t], train_params[t][p])
    return(regressors)

def main():
    args = parse_args()
    
    q = loaders.load_q(args.datadir)
    train_params = {}
    test_params = {}
    train_spec = loaders.load_all_spec(args.targets, q, args.datadir, args.dataset)
    test_spec = loaders.load_all_spec(args.targets, q, args.datadir, args.test_dataset, prefix = 'test')
    #train_spec = loaders.scale_highq(train_spec, 0.001)
    gamma_norm = train_spec[args.targets[0]].shape[0]
    regressors = construct_regressor(args.reg_file, gamma_norm)
    print('REGRESSORS')
    print(regressors)
    train_params = load_all_params(regressors, args.datadir, args.dataset)
    test_params = load_all_params(regressors, args.datadir, args.test_dataset)
    regressors = train_all_regression(train_spec, train_params, regressors)


    decision1 = {0:0,1:0,2:1,3:0,4:0,5:1}
    decision2 = {0:0,1:0,3:1,4:1}
    decision3 = {0:0,1:1}
    decision4 = {3:0,4:1}
    decision5 = {2:0,5:1}
    decisions = [decision1, decision2, decision3, decision4, decision5]
    hierarchical_map = [{0:1,1:4},{0:2,1:3},{0:'0',1:'1'},{0:'3',1:'4'},{0:'2',1:'5'}]
    spec, labels, _ = loaders.unravel_dict(train_spec, args.targets)
    tspec, tlabels, tmap = loaders.unravel_dict(test_spec, args.targets)
    tspec = loaders.scale_highq(tspec, 0.001)
    spec = loaders.scale_highq(spec, 0.001)
    classifiers = hier.create_classifiers(args.struct_strings, gamma_norm)
    hierarchical = hier.create_hierarchical(classifiers, decisions, spec, labels)
    preds, mapped_labs, mapped_inds = hier.eval_hierarchical(classifiers, hierarchical_map, tspec, tlabels)
    mapped_inds = mapped_inds.astype(int)
    preds = preds.astype(int)
    for i in range(len(args.targets)):
        t = args.targets[i]
        examples = np.equal(mapped_labs, i)
        predicted = np.equal(preds, i)
        correct_inds = np.where(np.logical_and(examples, predicted))[0]
        incorrect_inds = np.where(np.logical_and(examples, np.logical_not(predicted)))[0]
        correct_file = open('correct_%s.csv'%(args.targets[i]), 'w')
        correct_regs = {}
        original_correct = tmap[mapped_inds[correct_inds]]
        correct_spec = test_spec[args.targets[i]][original_correct]
        for p in regressors[t].keys():
            correct_regs[p] = regressors[t][p].predict(correct_spec)
        for oci in range(len(original_correct)):
            oc = original_correct[oci]
            correct_file.write('%d TRUE %s REGRESSED %s\n'%(oc, ' '.join(['%s:%f'%(p, test_params[t][p][oc]) for p in test_params[t].keys()]), ' '.join(['%s:%f'%(p, correct_regs[p][oci]) for p in correct_regs.keys()])))
        correct_file.close()
        incorrect_file = open('incorrect_%s'%(t), 'w')
        original_incorrect = tmap[mapped_inds[incorrect_inds]]
        incorrect_spec = test_spec[args.targets[i]][original_incorrect]
        for ici in range(incorrect_inds.shape[0]):
            regression = {}
            ptarg = args.targets[preds[incorrect_inds[ici]]]
            for p in regressors[ptarg].keys():
                regression[p] = regressors[ptarg][p].predict(np.reshape(incorrect_spec[ici], (1,-1)))
            incorrect_file.write('%d TRUE %s REGRESSED %s %s\n'%(original_incorrect[ici], ' '.join(['%s:%f'%(p, test_params[t][p][original_incorrect[ici]]) for p in test_params[t].keys()]), ptarg, ' '.join(['%s:%f'%(p, regression[p]) for p in regression.keys()])))
    if args.experimental:
        espec = np.log10(np.loadtxt('%s/experimental_spectra.csv'%(args.datadir))+.001)
        espec = loaders.scale_highq(espec, 0.001)
        preds, mapped_labs, mapped_inds = hier.eval_hierarchical(classifiers, hierarchical_map, espec, np.zeros(espec.shape[0]))
        #print(preds)
        #print(mapped_labs)
        #print(mapped_inds)
        sinds = np.argsort(mapped_inds).astype(int)
        plt.xscale('log')
        plt.yscale('log')
        for i in range(len(sinds)):
            ptarg = args.targets[int(preds[sinds[i]])]
            regressor = regressors[ptarg]
            outstring = '%s '%(ptarg)
            for p in regressor.keys():
                tpred = regressor[p].predict(espec[i].reshape(1,-1))
                #print('%s %f\n'%(p, tpred))
                outstring += ' %s: %f'%(p, tpred)
            print(outstring)
            plt.plot(q.astype(float), 10**espec[i], label=i)
        plt.legend()
        plt.title('Experimental Spectra')
        plt.xlabel('q')
        plt.ylabel('I')
        plt.savefig('exp_full.png')


if __name__ == '__main__':
    main()
