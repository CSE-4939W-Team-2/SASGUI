import numpy as np
from sklearn.model_selection import StratifiedKFold
import argparse
import pandas as pd
import os
import sys
import json
sys.path.append('..')
sys.path.append('../krr')
sys.path.append('../hierarchical')
sys.path.append('./krr')
sys.path.append('./hierarchical')
sys.path.append('./full_model')
import loaders
from hierarchical import hierarchical as hier
from full_model import full_send as fm
from sklearn.svm import SVC
from sklearn.metrics import classification_report as CR
from sklearn.metrics import accuracy_score as AS
from sklearn.kernel_ridge import KernelRidge as KRR
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_percentage_error as MAPE
from sklearn.model_selection import train_test_split

def init():
#Initialize Variables
    datadir = 'hierarchical_SAS_analysis-main 2/data'
    dataset = 'lowar16'
    targets = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere']
    reg_file = 'hierarchical_SAS_analysis-main 2/full_model/regression-hyperparameters'
    struct_strings = ['svc_10._100._rbf_1.', 'svc_100._100._rbf_1.', 'svc_10._100._rbf_1.', 'svc_100._10._rbf_1.', 'svc_100._100._rbf_1.']
    q = loaders.load_q(datadir)
    train_params = {}
    test_params = {}
    train_spec = loaders.load_all_spec(targets, q, datadir, dataset)
    gamma_norm = train_spec[targets[0]].shape[0]
    regressors = fm.construct_regressor(reg_file, gamma_norm)
    train_params = fm.load_all_params(regressors, datadir, dataset)
    regressors = fm.train_all_regression(train_spec, train_params, regressors)
    decision1 = {0:0,1:0,2:1,3:0,4:0,5:1}
    decision2 = {0:0,1:0,3:1,4:1}
    decision3 = {0:0,1:1}
    decision4 = {3:0,4:1}
    decision5 = {2:0,5:1}
    decisions = [decision1, decision2, decision3, decision4, decision5]
    hierarchical_map = [{0:1,1:4},{0:2,1:3},{0:'0',1:'1'},{0:'3',1:'4'},{0:'2',1:'5'}]
    spec, labels, _ = loaders.unravel_dict(train_spec, targets)
    spec = loaders.scale_highq(spec, 0.001)
    classifiers = hier.create_classifiers(struct_strings, gamma_norm)
    hierarchical = hier.create_hierarchical(classifiers, decisions, spec, labels)
    return (classifiers, hierarchical_map, regressors)
    #return {'classifier' : classifiers, 'hier' : hierarchical_map, 'regress' : regressors}
    #return {'ml' : True}



def predict_morphology(tspec, classifiers, hierarchical_map):
    targets = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere']
    preds, mapped_labs, mapped_inds = hier.eval_hierarchical(classifiers, hierarchical_map, tspec.reshape(1,-1), np.array(['0']))
    morph = targets[int(preds[0])]
    return(morph)


def predict_dimensions(tspec, regressors, morphology):
    regs = {}
    for p in regressors[morphology].keys():
        regs[p] = regressors[morphology][p].predict(tspec)
    return(regs)

def main(shape):
   bg_constant = 0.001
   targets = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere']
   classifiers, hierarchical_map, regressors = init()
   test_spectra = np.log10(np.loadtxt('hierarchical_SAS_analysis-main 2/data/experimental_spectra.csv')+bg_constant).reshape(1,-1)
   est_spectra = np.loadtxt('hierarchical_SAS_analysis-main 2/data/experimental_spectra.csv')+bg_constant
   print(est_spectra)
   li = np.array(est_spectra).tolist()
   print(li)
   test_spectra = loaders.scale_highq(test_spectra, bg_constant)
   predicted_morphology = predict_morphology(test_spectra, classifiers, hierarchical_map)
   #pass in diff predicted
   predicted_dimension = predict_dimensions(test_spectra, regressors, shape)
   morph = 'Predicted Morphology: %s'%(predicted_morphology)
   print(predicted_morphology)
   print(predicted_dimension)
   print('SASHIER1 %s'%(shape))
   if shape == "cs_sphere":
       return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), 'radius' : '%s'%(predicted_dimension.get('radius')[0]) , "q2" : li, 'pd' : '%s'%(predicted_dimension.get('polydispersity')[0]), 'thickness' : '%s'%(predicted_dimension.get('shell')[0])}
   if shape == "cs_cylinder":
       return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), 'radius' : '%s'%(predicted_dimension.get('radius')[0]) , "q2" : li, 'pd' : '%s'%(predicted_dimension.get('polydispersity')[0]), 'thickness' : '%s'%(predicted_dimension.get('shell')[0])}
   if shape == "cylinder":
       return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), 'length' : '%s'%(predicted_dimension.get('length')[0]) , "q2" : li,'radius' : '%s'%(predicted_dimension.get('radius')[0]), 'pd' : '%s'%(predicted_dimension.get('polydispersity')[0])}
   if shape == "sphere":
       return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), "q2" : li,'radius' : '%s'%(predicted_dimension.get('radius')[0]), 'pd' : '%s'%(predicted_dimension.get('polydispersity')[0])}
   if shape == "disk":
    return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), 'length' : '%s'%(predicted_dimension.get('length')[0]) , "q2" : li,'radius' : '%s'%(predicted_dimension.get('radius')[0])}
   if shape == "cs_disk":
       return {'morph' : 'Predicted Morphology: %s'%(predicted_morphology), 'radius' : '%s'%(predicted_dimension.get('radius')[0]) , "q2" : li, 'pd' : '%s'%(predicted_dimension.get('polydispersity')[0]), 'thickness' : '%s'%(predicted_dimension.get('shell')[0])}
print("Running startup.py...")
def main2(filepath):
   bg_constant = 0.001
   targets = ['cylinder', 'disk', 'sphere', 'cs_cylinder', 'cs_disk', 'cs_sphere']
#   classifiers, hierarchical_map, regressors = init()
   test_spectra = np.log10(np.loadtxt(filepath)+bg_constant).reshape(1,-1)
   est_spectra = np.loadtxt(filepath)+bg_constant
   print(est_spectra)
   li = np.array(est_spectra).tolist()
   print(li)
   test_spectra = loaders.scale_highq(test_spectra, bg_constant)
   predicted_morphology = predict_morphology(test_spectra, classifiers, hierarchical_map)
   #pass in diff predicted
   predicted_dimension = predict_dimensions(test_spectra, regressors, predicted_morphology)
   morph = 'Predicted Morphology: %s'%(predicted_morphology)
   print(predicted_morphology)
   print(predicted_dimension)
   if predicted_morphology == "cs_sphere":
       return {'morph' : '/coreShellSphere', 'coreShellSphereRadius' : '%s'%(predicted_dimension.get('radius')[0]) , 
               'coreShellSpherePolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0]), 
               'coreShellSphereThickness' : '%s'%(predicted_dimension.get('shell')[0])}
   if predicted_morphology == "cs_cylinder":
       return {'morph' : '/coreShellCylinder', 'coreShellCylinderRadius' : '%s'%(predicted_dimension.get('radius')[0]) , 
               'coreShellCylinderPolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0]), 
               'coreShellCylinderThickness' : '%s'%(predicted_dimension.get('shell')[0]),
               'coreShellCylinderLength' : '%s'%(predicted_dimension.get('length')[0])}
   if predicted_morphology == "cylinder":
       return {'morph' : '/cylinder', 'cylinderLength' : '%s'%(predicted_dimension.get('length')[0]) , 
               'cylinderRadius' : '%s'%(predicted_dimension.get('radius')[0]), 
               'cylinderPolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0])}
   if predicted_morphology == "sphere":
       return {'morph' : '/sphere', 'sphereRadius' : '%s'%(predicted_dimension.get('radius')[0]), 
               'spherePolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0])}
   if predicted_morphology == "disk":
       return {'morph' : '/disk', 'diskLength' : '%s'%(predicted_dimension.get('length')[0]),
               'diskRadius' : '%s'%(predicted_dimension.get('radius')[0]), 
               'diskPolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0])}
   if predicted_morphology == "cs_disk":
       return {'morph' : '/coreShellDisk', 'coreShellDiskRadius' : '%s'%(predicted_dimension.get('radius')[0]),
                'coreShellDiskPolydispersity' : '%s'%(predicted_dimension.get('polydispersity')[0]),
                'coreShellDiskThickness' : '%s'%(predicted_dimension.get('shell')[0]),
                'coreShellDiskLength' : '%s'%(predicted_dimension.get('length')[0])}


classifiers, hierarchical_map, regressors = init()
if __name__ == '__main__':
   main()
