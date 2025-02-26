#revision with highQ scaling and constant plateau addition 1-13-22
import numpy as np
import pandas as pd

def load_spec(fn, q):
   indf = pd.DataFrame(pd.read_csv("example_curve.csv"))
   print(indf)
   spec = np.log10(np.array(indf.loc[:,q])+1.)
   return(spec)

def load_params(fn, colnames):
   outparams = {}
   indf = pd.DataFrame(pd.read_csv(fn))
   for cn in colnames:
      if cn in indf.columns:
         outparams[cn] = np.array(indf.loc[:,cn])
      else:
         outparams[cn] = np.zeros(len(indf))
   return(outparams)

def scale(spec, maxval):
   for i in range(spec.shape[0]):
      spec[i,:] = spec[i,:]-spec[i,0]+maxval
   return(spec)

def scale_highq(spec, incoherence):
   for i in range(spec.shape[0]):
      spec[i] = spec[i] -np.mean(spec[i,-20:])+0.001
   return(spec)

def shuffle(spec, params):
   targets = spec.keys()
   for t in targets:
      ss = spec[t]
      inds = np.arange(ss.shape[0])
      np.random.shuffle(inds)
      for p in params[t].keys():
         params[t][p] = params[t][p][inds]
      spec[t] = spec[t][inds]
   return(spec, params)

def load_q(datadir, qfile = 'q_200.txt'):
   q = np.loadtxt('%s/%s'%(datadir, qfile), dtype=str, delimiter=',')
   return(q)

def load_all_spec(targets, q, datadir, dataset, prefix='train'):
   all_spec = {}
   maxval = 0
   for t in targets:
      fn = '%s/%s/%s_%s_%s.csv'%(datadir, dataset, prefix, t, dataset)
      spec = load_spec(fn, q)
      if np.max(spec[:,0]) > maxval:
         maxval = np.max(spec[:,0])
      all_spec[t] = spec
#   for t in targets:
#      all_spec[t] = scale(all_spec[t], maxval)
   return(all_spec)

def unravel_dict(spec_dict, targets = None):
    if targets is None:
        targets = spec_dict.keys()
    out_spec = spec_dict[targets[0]]
    out_labels = np.zeros(out_spec.shape[0])
    out_map = np.arange(out_spec.shape[0])
    for i in range(1,len(targets)):
        t = targets[i]
        out_spec = np.concatenate((out_spec, spec_dict[t]))
        out_labels = np.concatenate((out_labels, i*np.ones(spec_dict[t].shape[0])))
        out_map = np.concatenate((out_map, np.arange(spec_dict[t].shape[0])))
    return(out_spec, out_labels, out_map)

def concatenate_spec(spec):
   key = 0
   spec_list = []
   label_list = []
   for t in spec.keys():
      spec_list += [spec[t]]
      label_list += [key*np.ones(spec[t].shape[0])]
      key += 1
   allspec = np.concatenate(spec_list)
   labels = np.concatenate(label_list)      
   return(allspec, labels)


def load_all_params(targets, param_list, datadir, dataset, prefix = 'train'):
   all_params = {}
   for t in targets:
      fn = '%s/%s/%s_%s_%s.csv'%(datadir, dataset, prefix, t, dataset)
      params = load_params(fn, param_list)
      all_params[t] = params
   return(all_params)
