#!/usr/bin/env python3
"""
Module for making similarity/distance matrix with any dimensions of interest
"""

#pacakges:
#from supplementary_files.ImportDOI import *
import numpy as np
import pandas as pd
import scipy
from scipy.spatial import distance
import math
from math import nan
import os
import sys
from datetime import datetime


def make_matrix(version = 'constrained', type = 'similarity', dims = []):
    """

This is a function to create a distance or similarity matrix from the individual dimensions used to obtain the total similarity/distance scores.
It takes the arguments
- version ('constrained' (default) or 'unconstrained') specifying which calculation model to use,
- type ('similarity' (default), 'distance' or 'both') specifying if the matrix should be similarity (1 on the diagonal) or distance (0 on the diagonal) or both (NOTE: similarity matrix = 1 - distance matrix),
- dims, which is a character vector/list comprising of the following dimensions:\n\t age, design, eyetrack, imstruc, imfunc, tasktype, tbri, enc, ret, simenc, simret, cuemanip, stim, mod, repenctrial, delay

    """

    if len(dims) == 0: #checking if entries at all for dims
        nodims = "No dimensions supplied, please input dimensions of interest to the 'dims' argument of the function!\n\
(valid dimensions: age, design, eyetrack, imstruc, imfunc, tasktype, tbri, enc, ret, simenc, simret, cuemanip, stim, mod, repenctrial, delay)"
        raise ValueError(nodims)

    #is version correctly defined
    if version == 'unconstrained':
        subdir = '02a_Unconstrained'
        vers_mat = 'unconstr_'
    elif version == 'constrained':
        subdir = '02b_Constrained'
        vers_mat = 'constr_'
    else:
        raise ValueError("version argument must be either 'unconstrained' or 'constrained' (default), please edit input argument!")

    #define filepath
    currentwd = os.getcwd()
    if currentwd.endswith('simcalc-pipeline'):
        filepath = os.path.join(os.getcwd(), 'data_files', subdir, 'SingleDimensions', '')
        destpath = os.path.join(os.getcwd(), 'data_files', '03_DimsOfInterest', '')
    else:
        import subprocess
        try:
            homedir_repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
            os.chdir(homedir_repo[0:-1])
        except:
            print('\nWARNING: Directory not a git repository!\n')
            sys.stdout.flush()
        currentwd = os.getcwd()
        if currentwd.endswith('simcalc-pipeline'):
            filepath = os.path.join(os.getcwd(), 'data_files', subdir, 'SingleDimensions', '')
            destpath = os.path.join(os.getcwd(), 'data_files', '03_DimsOfInterest', '')
        else:
            error_str = '"'+os.getcwd()+'" is not home directory of repository. \nPlease make sure to be in root directory of the git repository ("/simcalc-pipeline").'
            raise NameError(error_str)

    #is type correctly defined?
    if type != 'similarity' and type != 'distance' and type != 'both':
        raise ValueError("type argument must be either 'both', 'distance' or 'similarity' (default), please edit input argument!")

    #now getting all single dim files
    if len(np.unique(dims)) != len(dims):
        raise ValueError('Duplicates detected. Please check that if a dimension is included, it only appears once in the input list/vector.')
    dim_names = os.listdir(filepath) #get the names of all files in the respective SingleDimensions subdirectory
    selected_dims = []
    for dim in dims:
        sel_dim = [a for a in dim_names if dim in a]
        if dim == "enc": #if enc than enc not simenc
            selected_dims.append('enc_vec.csv')
        elif dim == "ret": #if ret than ret not simret
            selected_dims.append('ret_vec.csv')
        elif len(sel_dim) != 1: #and dim != 'enc' and dim != 'ret':
            error_str = 'dimension not found or not specific enough for input "' + dim + '". Please check if the dimension is correctly named according to this scheme: \n\
age, design, eyetrack, imstruc, imfunc, tasktype, tbri, enc, ret, simenc, simret, cuemanip, stim, mod, repenctrial, delay'
            #fix problem with enc and ret to make more specific (problems with simenc and simret that they contain the same part in the name)
            raise ValueError(error_str) #if one of the dims is not correctly assigned, raise Error
        else:
            selected_dims.append(sel_dim[0]) #otherwise make list with the names of files wanted

    print_type = type
    if print_type == "both":
        print_type = "both similarity and distance"
    print_dims = ', '.join(dims)

    print('making {} matrix from {} model for dimensions {}.'.format(print_type, version, print_dims))
    sys.stdout.flush()

    ind_doi = [0] * len(selected_dims)
    for d in range(0,len(ind_doi)):
        path2file = filepath + selected_dims[d]
        ind_doi[d] = np.transpose(np.array(pd.read_csv(path2file)))[0] #loading files

    mean_doi = np.nanmean(ind_doi, axis=0)

    #getting ID
    ID = pd.read_csv(filepath + 'EntryID.csv')
    #making matrix:
    dist_mat = pd.DataFrame(distance.squareform(mean_doi))
    sim_mat  = 1 - dist_mat
    #add the # ID
    dist_mat.insert(0, 'EntryID', ID['Entry_ID'])
    sim_mat.insert(0, 'EntryID', ID['Entry_ID'])
    #filename ending:
    filename_sim  = os.path.join(destpath, 'sim_' + vers_mat + datetime.now().strftime("%y-%m-%d") + '__' + '_'.join(dims) + '.csv')
    filename_dist = os.path.join(destpath, 'dist_' + vers_mat + datetime.now().strftime("%y-%m-%d") + '__' + '_'.join(dims) + '.csv')

    if type == 'both':
        #saving
        dist_mat.to_csv(filename_dist, index=False)
        sim_mat.to_csv(filename_sim, index=False)
        print("Matrices created and saved in {}".format(destpath))
    elif type == 'similarity':
        sim_mat.to_csv(filename_sim, index=False)
    elif type == 'distance':
        dist_mat.to_csv(filename_dist, index=False)

    #print finish message for single type output:
    if type != 'both':
        print("Matrix created and saved in {}".format(destpath))
