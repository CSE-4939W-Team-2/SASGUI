import argparse
import numpy as np
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold as KFold
import sys
sys.path.append('..')
import loaders

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('--targets', default=['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere'], nargs = '+')
   parser.add_argument('--classifier', default='knn')
   parser.add_argument('--datadir', default='../../data/')
   parser.add_argument('--dataset', default='newlar2')
   parser.add_argument('--test_dataset', default=None, help = 'The dataset to use for test in evaluation setting. If not None 5-fold validation will be used.')
   parser.add_argument('--alpha', default=1, help = 'The alpha parameer for KRC ignored for KNN and SVC', type=float)
   parser.add_argument('--kernel', default='polynomial')
   parser.add_argument('--degree', default=5, type=int)
   parser.add_argument('--c', default=1, help = 'The C parameter for SVC', type=float)
   parser.add_argument('--gamma', default=1, help='ignored fo KNN',type = float)
   parser.add_argument('--weight', default='uniform', help='The weight parameter for knn')
   parser.add_argument('--n_neighbors', default=1, help='The number of neighbors for KNN, ignored otherwise', type=int)
   parser.add_argument('--logfile', default = 'baseline_log.csv')
   parser.add_argument('--shuffle',type=bool, default=False)
   parser.add_argument('--print_folds', default=None, type=str)
   parser.add_argument('--learning_curve', default=False, type=bool)
   parser.add_argument('--experimental', type=bool, default=False)
   parser.add_argument('--coeff0', default = 1, type = float)
   return(parser.parse_args())

def main():
   args = parse_args()
   q = loaders.load_q(args.datadir)
   spec_dict = loaders.load_all_spec(args.targets, q, args.datadir, args.dataset)
   print(spec_dict)
   spec, labels = loaders.concatenate_spec(spec_dict)
   maxval = np.max(spec[:,0])
#   spec = loaders.scale(spec, maxval)
   if args.shuffle:
      inds = np.arange(spec.shape[0])
      np.random.shuffle(inds)
      spec = spec[inds]
      labels = labels[inds]
   if args.classifier == 'svc':
      predictor = SVC(C = args.c, gamma = args.gamma/spec.shape[0], degree = args.degree, kernel = args.kernel, coef0 = args.coeff0)
      outkey = 'SVC %f NA %f %f %d %s NA NA '%(args.c, args.gamma, args.coeff0, args.degree, args.kernel)
   elif args.classifier == 'knn':
      predictor = KNeighborsClassifier(n_neighbors = args.n_neighbors)
      outkey = 'KNN NA NA NA NA NA NA %d %s '%(args.n_neighbors, args.weight)
   else:
      predictor = RidgeClassifier(alpha = args.alpha)
      #predictor = RidgeClassifier(alpha = args.alpha, gamma = args.gamma/spec.shape[0], kernel = args.kernel, degree = args.degree)
      outkey = 'KRC NA %f NA NA NA NA NA NA'%(args.alpha)
   if args.test_dataset is not None:
      test_spec_dict = loaders.load_all_spec(args.targets, q, args.datadir, args.test_dataset, prefix='test')
      test_spec, test_labels = loaders.concatenate_spec(test_spec_dict)
      #test_spec = loaders.scale(test_spec, maxval)
      if not args.learning_curve:
         test_inds = np.arange(test_spec.shape[0])
   #      test_spec = test_spec[inds]
   #      test_labels = test_labels[inds]
         predictor.fit(spec, labels)
         preds = predictor.predict(test_spec)
         logfile = open(args.logfile, 'a')
         logfile.write('TEST %s%f\n'%(outkey, accuracy_score(test_labels, preds)))
      else:
         n_folds = 10
         kf = KFold(n_splits=n_folds)
         fold_ind = 0
         accs = np.zeros(n_folds)
         test_folds = np.zeros(n_folds)
         for train_inds, val_inds in kf.split(spec, labels):
            X_train = spec[train_inds]
            X_val = spec[val_inds]
            y_train = labels[train_inds]
            y_val = labels[val_inds]
            predictor.fit(X_train, y_train)
            preds = predictor.predict(X_val)
            accs[fold_ind] = accuracy_score(y_val, preds)
            test_preds = predictor.predict(test_spec)
            test_folds[fold_ind] = accuracy_score(test_labels, test_preds)
            fold_ind += 1
      if args.print_folds is not None:
         np.savetxt(args.print_folds, accs)
         np.savetxt('test_%s'%(args.print_folds), test_folds)
      
   elif args.experimental:
      colors = ['red', 'green', 'blue']
      test_spec = np.zeros((len(colors), spec.shape[1]))
      for i in range(len(colors)):
          col = colors[i]
          infile = np.loadtxt('%s/exp/%s_fitted.csv'%(args.datadir, col))
          test_spec[i,:] = infile[:,1]
      test_spec = np.log10(test_spec)
      #test_spec = loaders.scale(test_spec, maxval)
      predictor.fit(spec, labels)
      predictions = predictor.predict(test_spec)
      outfile = open('Experimental_predictions.csv','a')
      outfile.write('%s\n'%(args.dataset))
      for i in range(len(colors)):
          outfile.write('%s %s\n'%(colors[i], args.targets[predictions[i].astype(int)]))
   else:
      n_folds = 10
      kf = KFold(n_splits=n_folds)
      fold_ind = 0
      accs = np.zeros(n_folds)
      for train_inds, val_inds in kf.split(spec, labels):
         X_train = spec[train_inds]
         X_val = spec[val_inds]
         y_train = labels[train_inds]
         y_val = labels[val_inds]
         predictor.fit(X_train, y_train)
         preds = predictor.predict(X_val)
         accs[fold_ind] = accuracy_score(y_val, preds)
         fold_ind += 1
         print(accs)
      if args.print_folds is not None:
         np.savetxt(args.print_folds, accs)
      logfile = open(args.logfile, 'a')
      logfile.write('%s%f %f\n'%(outkey, np.mean(accs), np.std(accs)))
    

if __name__ == '__main__':
   main()
      
   

