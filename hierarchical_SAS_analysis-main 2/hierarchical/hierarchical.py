import numpy as np
from sklearn.model_selection import StratifiedKFold
import argparse
import pandas as pd
import os
import sys
sys.path.append('..')
sys.path.append('../krr')
import loaders
#import sas_krr_reg as spreg
from sklearn.svm import SVC
from sklearn.metrics import classification_report as CR
from sklearn.metrics import accuracy_score as AS
from matplotlib import pyplot as plt

def relabel(labels, decision):
   new_inds = np.empty(0)
   new_labels = np.empty(0)
   for i in decision.keys():
      temp_matches = np.equal(labels, i)
      temp_labels = decision[i]*np.ones(np.sum(temp_matches))
      temp_inds = np.where(temp_matches)[0]
      new_inds = np.concatenate((new_inds, temp_inds))
      new_labels = np.concatenate((new_labels, temp_labels))
   return(new_inds.astype(int), new_labels)

def create_classifiers(struct_strings, gamma_norm):
   classifiers = []
   for ss in struct_strings:
      ss = ss.strip()
      toks = ss.split('_')
      if toks[0].lower() == 'svc':
         if toks[3].lower()== 'poly':
            classifier = SVC(C = float(toks[1]), gamma = float(toks[2])/gamma_norm, kernel = 'poly', degree = int(toks[4]), coef0=float(toks[5]))
         else:
            classifier = SVC(C = float(toks[1]), gamma = float(toks[2])/gamma_norm, kernel = toks[3], coef0 = float(toks[4]))
      #elif toks[0].lower() == 'knr':
         #classifier = 
      classifiers += [classifier]
   return(classifiers)

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('--targets', default = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere'], nargs = '+')
   parser.add_argument('--datadir', default = '../../data')
   parser.add_argument('--dataset', default = 'newlar2')
   parser.add_argument('--test_dataset', default=None)
   parser.add_argument('--projection', type=bool, default=False)
   parser.add_argument('--logfile', default='hierarchical_log.csv')
   parser.add_argument('--struct_strings', default=['svc_10_10 ','svc_10_10 ','svc_10_10 ','svc_10_10 ', 'svc_10_10'], nargs='+')
   parser.add_argument('--shuffle', type=bool, default = False)
   parser.add_argument('--n_splits', default=10)
   parser.add_argument('--experimental', type=bool, default = False)
   return(parser.parse_args())
   
def create_hierarchical(classifiers, decisions, train_spec, train_labels):
   for i in range(len(classifiers)):
      temp_inds, temp_labels = relabel(train_labels, decisions[i])
      classifiers[i].fit(train_spec[temp_inds], temp_labels)
   return()

def eval_hierarchical(classifiers, hierarchical_map, spec, labels):
   print('LABELS')
   print(labels)
   inds = np.arange(spec.shape[0])
   queue = [0]
   spec_queue = [spec]
   key_queue = [labels]
   inds_queue = [inds]
   out_preds = np.empty(0)
   out_key = np.empty(0)
   out_inds = np.empty(0)
   while(len(queue)>0):
      print(queue)
      node = queue[0]
      temp_spec = spec_queue[0]
      temp_key = key_queue[0]
      temp_inds = inds_queue[0]
      temp_preds = classifiers[node].predict(spec_queue[0])
      for bin_val in [0,1]:
         match_inds = np.where(np.equal(temp_preds, bin_val))[0]
         if type(hierarchical_map[node][bin_val]) == int:
            if match_inds.shape[0] > 0:
               queue += [hierarchical_map[node][bin_val]]
               spec_queue += [temp_spec[match_inds]]
               key_queue += [temp_key[match_inds]]
               inds_queue += [temp_inds[match_inds]]
         else:
            out_preds = np.concatenate((out_preds, int(hierarchical_map[node][bin_val])*np.ones(match_inds.shape[0])))
            out_key = np.concatenate((out_key, temp_key[match_inds]))
            out_inds = np.concatenate((out_inds, temp_inds[match_inds]))
      queue = queue[1:]
      spec_queue = spec_queue[1:]
      key_queue = key_queue[1:]
      inds_queue = inds_queue[1:]
   return(out_preds, out_key, out_inds)
            
def main():
   args = parse_args()
   decision1 = {0:0,1:0,2:1,3:0,4:0,5:1}
   decision2 = {0:0,1:0,3:1,4:1}
   decision3 = {0:0,1:1}
   decision4 = {3:0,4:1}
   decision5 = {2:0,5:1}
   decisions = [decision1, decision2, decision3, decision4, decision5]
   hierarchical_map = [{0:1,1:4},{0:2,1:3},{0:'0',1:'1'},{0:'3',1:'4'},{0:'2',1:'5'}]
   q = loaders.load_q(args.datadir)
   targets = args.targets
   spec_dict = loaders.load_all_spec(targets, q, args.datadir, args.dataset)
   spec, labels = loaders.concatenate_spec(spec_dict)
   maxval = np.max(spec[:,0])
   #spec = loaders.scale(spec, maxval)
   incoherence = 0.001
#   spec = loaders.scale_highq(spec, incoherence)
   if args.shuffle:
      shinds = np.arange(spec.shape[0])
      np.random.shuffle(shinds)
      spec = spec[shinds]
      labels = labels[shinds]
   classifiers = create_classifiers(args.struct_strings, 200)
   if args.test_dataset is not None:
      test_spec_dict = loaders.load_all_spec(targets, q, args.datadir, args.test_dataset, prefix='test')
      test_spec, test_labels = loaders.concatenate_spec(test_spec_dict)
   #   test_spec = loaders.scale(test_spec, maxval)
#      test_spec = loaders.scale_highq(test_spec, incoherence)
      hierarchical = create_hierarchical(classifiers, decisions, spec, labels)
      preds, mapped_labs, mapped_inds = eval_hierarchical(classifiers, hierarchical_map, test_spec, test_labels)
      cr = CR(mapped_labs, preds)
      incorrect_inds = np.where(np.equal(mapped_labs, preds))
      incorrect_labs = mapped_labs[incorrect_inds].astype(int)
      incorrect_key = mapped_inds[incorrect_inds].astype(int)
      incorrect_preds = preds[incorrect_inds].astype(int)
      acc = AS(mapped_labs, preds)
      outfile = open(args.logfile, 'a')
      outfile.write('TEST %s TRAIN %s %s %f\n'%(args.test_dataset, args.dataset, ' '.join(args.struct_strings), acc))
      outfile.close()
      for i in np.unique(incorrect_labs):
         where_incorrect = np.where(np.equal(incorrect_labs, i))[0].astype(int)
         np.random.shuffle(where_incorrect)
         plt.xscale('log')
         plt.yscale('log')
         for j in range(min(5, len(where_incorrect))):
            plt.plot(q.astype(float), spec[incorrect_key[where_incorrect[j]]])#, label = '%f predicted as %s'%(incorrect_key[where_incorrect[j]], args.targets[incorrect_preds[where_incorrect[j]]]))
         plt.legend()
         plt.title('%s Incorrectly Predicted Spectra'%(args.targets[i]))
         plt.xlabel('Q')
         plt.ylabel('Intensity')
         plt.savefig('%s_missed.png'%(args.targets[i]))
         plt.clf()
   elif args.experimental:
      colors = np.array(['red', 'green', 'blue', 'black_fbio', 'cs-sphere-3'])
      color_map = {'blue':'blue', 'red':'red', 'green':'green', 'black_fbio':'purple', 'cs-sphere-3':'magenta'}
      exp_spec = np.zeros((len(colors), spec.shape[1]))
      for i in range(colors.shape[0]):
          infile = np.loadtxt('%s/exp/%s_fitted.csv'%(args.datadir, colors[i]))
          exp_spec[i,:] = infile[:,1]
      #    if colors[i] in ['cs-sphere-3']:
      #        exp_spec[i,:] = exp_spec[i,:]+1.
      #exp_spec = loaders.scale(exp_spec, maxval)
      exp_spec = np.log10(exp_spec)
      exp_spec = loaders.scale_highq(exp_spec, incoherence)
      hierarchical = create_hierarchical(classifiers, decisions, spec, labels)
      preds, mapped_cols, _ = eval_hierarchical(classifiers, hierarchical_map, exp_spec, colors)
      outfile = open('Experimental_predictions.csv', 'w')
      for i in range(mapped_cols.shape[0]):
          outfile.write('%s %s\n'%(mapped_cols[i], preds[i]))
      outfile.close()
      plt.xscale('log')
      plt.yscale('log')
      pinds = np.arange(spec.shape[0])
      np.random.shuffle(pinds)
      for pi in pinds[:10]:
         plt.plot(q.astype(float),10**spec[pi,:], color='black', alpha=.5)
      for i in range(colors.shape[0]):
         #plt.plot(q.astype(float), 10**exp_spec[i,:], label=colors[i])
         plt.plot(q.astype(float), 10**exp_spec[i,:], color=color_map[colors[i]])
      plt.plot(q.astype(float),10**spec[np.random.randint(0, high=6000),:], color='black')
      plt.xlabel('Q')
      plt.ylabel('Intensity')
      plt.savefig('experimental_show.png')
      plt.legend()
      plt.clf()

   else:
      KF = StratifiedKFold(n_splits = args.n_splits)
      per_fold = np.zeros(args.n_splits)
      fold_ind = 0
      for train_inds, val_inds in KF.split(spec, labels):
         train_spec = spec[train_inds]
         train_labels = labels[train_inds]
         val_spec = spec[val_inds]
         val_labels = labels[val_inds]
         hierarchical = create_hierarchical(classifiers, decisions, train_spec, train_labels)
         preds, mapped_key, mapped_indices = eval_hierarchical(classifiers, hierarchical_map, val_spec, val_labels)
         per_fold[fold_ind] = AS(mapped_key, preds)
         fold_ind += 1
      print('%f +- %f'%(np.mean(per_fold), np.std(per_fold)))
      outfile = open(args.logfile, 'a')
      outfile.write('KFOLD %s %s %f\n'%(args.dataset, ' '.join(args.struct_strings), np.mean(per_fold)))
      

if __name__ == '__main__':
   main()
