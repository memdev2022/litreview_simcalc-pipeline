"""
UNCONSTRAINED
Script for getting complete similarity matrix and for getting individual dimensions
"""

#loading packages
import numpy as np
import pandas as pd
import scipy
import os
import sys
from scipy.spatial import distance
import math
from math import nan
from datetime import datetime

#load binarized data file
#specify path for data files (workaround via git command to make sure that directories are correct)
if os.getcwd().endswith('simcalc-pipeline'):
    wd = os.getcwd()
else:
    import subprocess
    try:
        homedir_repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        os.chdir(homedir_repo[0:-1])
    except:
        print('\nWARNING: Directory not a git repository!\n')
    if os.getcwd().endswith('simcalc-pipeline'):
        wd = os.getcwd()
    else:
        error_str = '"'+os.getcwd()+'" is not home directory of repository. \nPlease make sure to be in root directory of the git repository ("/simcalc-pipeline").'
        raise NameError(error_str)

#or define wd directly here if path to data does is not defined correctly automatically:
#wd = "D:/" this was only placeholder, but can be specified if needed to point to simcalc-pipeline direcetory (ending with '*simcalc-pipeline')

#deining filepath:
filepath = os.path.join(wd, 'data_files', '')

#reading data
try:
    data_lit_bin = pd.read_excel(filepath + 'Lit_Review_binarized.xlsx')
except FileNotFoundError:
    raise ValueError("Path to binarized file not correct. Please check again and assign manually if necessary.")
#check file
data_lit_bin

# Defining data and measure (jaccard is the default we use when the dimension is just binary)
data = data_lit_bin
measure = 'jaccard'
dimensions = ["Age", "Design", "Eye tracking", "Imaging structure", "Imaging function",
              "Task type", "To be remembered", "Encoding", "Retrieval", "Similarity Manipulation Encoding",
              "Similarity Manipulation Retrieval", "Cue manipulation", "Stimuli","Modality",
              "Repetition of encoding trials", "Delay"]
n_dimensions = int(len(dimensions))

# Subset all respective dimensions
Age       = data.loc[:, [a for a in data.columns if a.startswith("Age")]]
Design    = data.loc[:, [a for a in data.columns if a.startswith("Design")]]
ETrack    = data.loc[:, [a for a in data.columns if a.startswith("Eye tracking")]]
ImgStr    = data.loc[:, [a for a in data.columns if a.startswith("Imaging structure")]]
ImgFun    = data.loc[:, [a for a in data.columns if a.startswith("Imaging function")]]
TaskType  = data.loc[:, [a for a in data.columns if a.startswith("Task type")]]
TBRI      = data.loc[:, [a for a in data.columns if a.startswith("To be remembered")]]
Encoding  = data.loc[:, [a for a in data.columns if a.startswith("Encoding")]]
Retrieval = data.loc[:, [a for a in data.columns if a.startswith("Retrieval")]]
SimEnc    = data.loc[:, [a for a in data.columns if a.startswith("Similarity Manipulation Encoding")]]
SimRet    = data.loc[:, [a for a in data.columns if a.startswith("Similarity Manipulation Retrieval")]]
CueM      = data.loc[:, [a for a in data.columns if a.startswith("Cue")]]
Stim      = data.loc[:, [a for a in data.columns if a.startswith("Stimuli")]]
Mod       = data.loc[:, [a for a in data.columns if a.startswith("Mod")]]
RepEnc    = data.loc[:, [a for a in data.columns if a.startswith("Repetition of encoding trials")]]
Delay     = data.loc[:, [a for a in data.columns if a.startswith("Delay")]]
#as list
subsets = [Age, Design, ETrack, ImgStr, ImgFun, TaskType, TBRI, Encoding, Retrieval,
           SimEnc, SimRet, CueM, Stim, Mod, RepEnc, Delay]

# Now we can check where there is missing information (no entry in respective dimension) --> asked using: is there an index for a row that contains only zeroes in that dimension?
# We print this so that we know which dimensions will occasionally be left out in our calculation
print('Checking for no entries or missing information:\n')
for d in range(0, len(dimensions)):
    print('%s: {}'.format((np.where((np.sum(subsets[d], axis=1)) == 0)[0]).any())%dimensions[d])

###############################################################################
# HERE WE START WITH THE CALCULATIONS
###############################################################################

# Looping over every every pairwise comparison that looks at the individual dimensions and calculates the distance according to the constraints
age_dists = [] #empty list to add distances to for converting into squareform in the end (0)
design_dists = [] #empty list to add distances to for converting into squareform in the end (1)
eyetrack_dists = [] #empty list to add distances to for converting into squareform in the end (2)
imstruc_dists = [] #empty list to add distances to for converting into squareform in the end (3)
imfunc_dists = [] #empty list to add distances to for converting into squareform in the end (4)
tasktype_dists = [] #empty list to add distances to for converting into squareform in the end (5)
tbri_dists = [] #empty list to add distances to for converting into squareform in the end (6)
enc_dists = [] #empty list to add distances to for converting into squareform in the end (7)
ret_dists = [] #empty list to add distances to for converting into squareform in the end (8)
simenc_dists = [] #empty list to add distances to for converting into squareform in the end (9)
simret_dists = [] #empty list to add distances to for converting into squareform in the end (10)
cuemanip_dists = [] #empty list to add distances to for converting into squareform in the end (11)
stim_dists = [] #empty list to add distances to for converting into squareform in the end (12)
mod_dists = [] #empty list to add distances to for converting into squareform in the end (13)
repenctrial_dists = [] #empty list to add distances to for converting into squareform in the end (14)
delay_dists = [] #empty list to add distances to for converting into squareform in the end (15)
dists = []
c = 1 #comparison starting from row 1, add 1 at the end of each ref loop !

# THIS IS THE IMPORTANT LOOP
print('\n\n -- STARTING UNCONSTRAINED CALCULATION -- \n\n')
sys.stdout.flush()

for ref in range(0,len(data)):

    #define the reference
    first = data.iloc[[ref]]

    for pair in range(c,len(data)):
        #define the paired entry for distance
        second = data.iloc[[pair]]
        ind_dists = []

        for d in range(0,len(dimensions)):

            a_dim = first.loc[:,[a for a in first.columns if a.startswith(dimensions[d])]]
            b_dim = second.loc[:,[a for a in second.columns if a.startswith(dimensions[d])]]

            if (np.sum(a_dim, axis = 1) == 0)[ref] and (np.sum(b_dim, axis = 1) == 0)[pair]:

                eyetrack_dists.append(nan) if d == 2 else imstruc_dists.append(nan) if d == 3 else imfunc_dists.append(nan) if d == 4 else stim_dists.append(nan) if d == 12 \
                else mod_dists.append(nan) if d == 13 else repenctrial_dists.append(nan) if d == 14 else delay_dists.append(nan) if d == 15 \
                else print("\nwarning: {} and {} have no entries for {}\n".format(ref, pair, dimensions[d]))
                ind_dists.append(nan)
                #continue #we don't need continue anymore since we are passing something inside the if clause

            else:

                j_d = distance.jaccard(a_dim, b_dim)

                age_dists.append(j_d) if d == 0 else design_dists.append(j_d) if d == 1 else eyetrack_dists.append(j_d) if d == 2 else imstruc_dists.append(j_d) if d == 3 \
                else imfunc_dists.append(j_d) if d == 4 else tasktype_dists.append(j_d) if d == 5 else tbri_dists.append(j_d) if d == 6 else enc_dists.append(j_d) if d == 7 \
                else ret_dists.append(j_d) if d == 8 else simenc_dists.append(j_d) if d == 9 else simret_dists.append(j_d) if d == 10 else cuemanip_dists.append(j_d) if d == 11 \
                else stim_dists.append(j_d) if d == 12 else mod_dists.append(j_d) if d == 13 else repenctrial_dists.append(j_d) if d == 14 else delay_dists.append(j_d) if d == 15 \
                else print("\nwarning: no distance calculated for {} and {} in {}\n".format(ref, pair, dimensions[d]))

                ind_dists.append(j_d)

        #w_dist = np.array(ind_dists).sum()/len(ind_dists) #this was older version without nan values
        w_dist = np.nanmean(ind_dists) #new version with nan values
        dists.append(w_dist)

    c +=1
    print('row nr. {}: done'.format(ref+1))
    sys.stdout.flush()


# make pd.DataFrame of all dimenstions
dist_unconstrained = pd.DataFrame(distance.squareform(dists))
sim_unconstrained = 1 - dist_unconstrained

#adding Entry_ID
dist_unconstrained.insert(0, 'Entry_ID', data_lit_bin['Entry_ID'])
sim_unconstrained.insert(0, 'Entry_ID', data_lit_bin['Entry_ID'])

#save total as csv files
dist_unconstrained.to_csv(filepath + '02a_Unconstrained/distance_unconstrained.csv', index = False)
sim_unconstrained.to_csv(filepath + '02a_Unconstrained/similarity_unconstrained.csv', index = False)

#save individual vectors as csv files
#saving individual dimension values as column vectors in csv format
age_pd = pd.DataFrame(age_dists)
age_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/age_vec.csv', index = False)
design_pd = pd.DataFrame(design_dists)
design_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/design_vec.csv', index = False)
eyetrack_pd = pd.DataFrame(eyetrack_dists)
eyetrack_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/eyetrack_vec.csv', index = False)
imstruc_pd = pd.DataFrame(imstruc_dists)
imstruc_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/imstruc_vec.csv', index = False)
imfunc_pd = pd.DataFrame(imfunc_dists)
imfunc_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/imfunc_vec.csv', index = False)
tasktype_pd = pd.DataFrame(tasktype_dists)
tasktype_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/tasktype_vec.csv', index = False)
tbri_pd = pd.DataFrame(tbri_dists)
tbri_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/tbri_vec.csv', index = False)
enc_pd = pd.DataFrame(enc_dists)
enc_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/enc_vec.csv', index = False)
ret_pd = pd.DataFrame(ret_dists)
ret_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/ret_vec.csv', index = False)
simenc_pd = pd.DataFrame(simenc_dists)
simenc_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/simenc_vec.csv', index = False)
simret_pd = pd.DataFrame(simret_dists)
simret_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/simret_vec.csv', index = False)
cuemanip_pd = pd.DataFrame(cuemanip_dists)
cuemanip_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/cuemanip_vec.csv', index = False)
stim_pd = pd.DataFrame(stim_dists)
stim_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/stim_vec.csv', index = False)
mod_pd = pd.DataFrame(mod_dists)
mod_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/mod_vec.csv', index = False)
repenctrial_pd = pd.DataFrame(repenctrial_dists)
repenctrial_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/repenctrial_vec.csv', index = False)
delay_pd = pd.DataFrame(delay_dists)
delay_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/delay_vec.csv', index = False)
dists_pd = pd.DataFrame(dists)
dists_pd.to_csv(filepath + '02a_Unconstrained/SingleDimensions/unconstrained_totaldist_vec.csv', index = False)
entry_IDs = data_lit_bin[['Entry_ID']]
entry_IDs.to_csv(filepath + '02a_Unconstrained/SingleDimensions/EntryID.csv', index = False)

#Print finish message:
print('\n\n Finished! Files saved under\n', filepath + '02a_Unconstrained/', '\n and\n', filepath + '02a_Unconstrained/SingleDimensions/')
