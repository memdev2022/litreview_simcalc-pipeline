"""
CONSTRAINED
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

#or define wd directly here if path to data is not defined correctly automatically:
#wd = "D:/" this was only placeholder, but can be specified if needed to point to simcalc-pipeline direcetory (ending with 'simcalc-pipeline'!!)

#deining filepath:
filepath = os.path.join(wd, 'data_files', '')

#reading data
try:
    data_lit_bin = pd.read_excel(filepath + 'Lit_Review_binarized.xlsx')
except FileNotFoundError:
    raise ValueError("path to binarized file not correct. please check again and assign manually if necessary")
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
print('\n--\nChecking for no entries or missing information:\n')
for d in range(0, len(dimensions)):
    print('%s: {}'.format((np.where((np.sum(subsets[d], axis=1)) == 0)[0]).any())%dimensions[d])
# Now we check where there are more than 1 entries in dimension
print('\n--\nChecking for more than one entry in dimension:\n')
for d in range(0, len(dimensions)):
    print('%s: {}'.format((np.where((np.sum(subsets[d], axis=1)) > 1)[0]).any())%dimensions[d])
print('\n--\nChecking for more than two entries in dimension:\n')
for d in range(0, len(dimensions)):
    print('%s: {}'.format((np.where((np.sum(subsets[d], axis=1)) > 2)[0]).any())%dimensions[d])
#printing to console:
sys.stdout.flush()
###############################################################################
# HERE WE START WITH THE CALCULATIONS
###############################################################################

# Looping over every every pairwise comparison that looks at the individual dimensions and calculates the distance according to the constraints
age_dists = [] #empty list to add distances to for converting into squareform in the end
design_dists = [] #empty list to add distances to for converting into squareform in the end
eyetrack_dists = [] #empty list to add distances to for converting into squareform in the end
imstruc_dists = [] #empty list to add distances to for converting into squareform in the end
imfunc_dists = [] #empty list to add distances to for converting into squareform in the end
tasktype_dists = [] #empty list to add distances to for converting into squareform in the end
tbri_dists = [] #empty list to add distances to for converting into squareform in the end
enc_dists = [] #empty list to add distances to for converting into squareform in the end
ret_dists = [] #empty list to add distances to for converting into squareform in the end
simenc_dists = [] #empty list to add distances to for converting into squareform in the end
simret_dists = [] #empty list to add distances to for converting into squareform in the end
cuemanip_dists = [] #empty list to add distances to for converting into squareform in the end
stim_dists = [] #empty list to add distances to for converting into squareform in the end
mod_dists = [] #empty list to add distances to for converting into squareform in the end
repenctrial_dists = [] #empty list to add distances to for converting into squareform in the end
delay_dists = [] #empty list to add distances to for converting into squareform in the end
dists = []

c = 1 #comparison starting from row 1, add 1 at the end of each ref loop !
age_steps = 1/17 #defining age_steps to calculate the distance between age groups equally across 18 possibilities
delay_steps = 1/12 #defining delay_steps to calculate the distance between age groups equally across 13 possibilities
sim_manip_dismatrix = distance.squareform([1,1,1,1,1,0.5,0.25,0.5,0.5,0.25,0.5,0.5,0.5,0.5,0.5]) #making matrix to access which distance is for which combination for sim manipulation
cue_manip_dismatrix = distance.squareform([1,1,1,1,1,0.5,0.5,0.25,0.5,0.5,0.5,0.5,0.5,0.25,0.5]) #making matrix to access which distance is for which combination for cue manipulation
mod_dismatrix = distance.squareform([1,1,0.5,0.5,1,1]+[1,0.5,1,0.5,1]+[1,0.5,0.5,1]+[0.5,0.5,1]+[0.5,1]+[1]) #making matrix to access which distance is for which combination for modality

# THIS IS THE IMPORTANT LOOP
print('\n\n -- STARTING CALCULATION -- \n\n')
sys.stdout.flush()
#%%time
for ref in range(0,len(data)):

    #define the reference
    first = data.iloc[[ref]]

    for pair in range(c,len(data)):
        #define the paired entry for distance
        second = data.iloc[[pair]]
        ind_dists = [] #we will append this list with the individual distance scores of every dimension used for the calculation

        for d in range(0,len(dimensions)):

            ref_dim  = first.loc[:,[a for a in first.columns if a.startswith(dimensions[d])]]
            pair_dim = second.loc[:,[a for a in second.columns if a.startswith(dimensions[d])]]


            #we will first define a statement that checks whether d is a dimension that is calculated according to jaccard's method
            #that is: design, eye tracking, task type, tbri, retrieval mode, stimuli, repetition of encoding trials
            if d == 1 or d == 2 or d == 5 or d == 6 or d == 8 or d == 12 or d == 14:

                #in eye tracking, stimuli & repition of encoding trials: leave out dimension if both have no information in the respective dimensions
                #we need to access the np.array with the correct index of ref or pair once the sum is calculated
                if (np.sum(ref_dim, axis=1) == 0)[ref] and (np.sum(pair_dim, axis=1) == 0)[pair]:

                    eyetrack_dists.append(nan) if d == 2 else stim_dists.append(nan) if d == 12 \
                    else repenctrial_dists.append(nan) if d == 14 else print("\nwarning: {} and {} have no entries for {}\n".format(ref, pair, dimensions[d]))
                    ind_dists.append(nan)

                else:
                    j_d = distance.jaccard(ref_dim, pair_dim)
                    design_dists.append(j_d) if d == 1 else eyetrack_dists.append(j_d) if d == 2 else tasktype_dists.append(j_d) if d == 5 else tbri_dists.append(j_d) if d == 6 \
                    else ret_dists.append(j_d) if d == 8 else stim_dists.append(j_d) if d == 12 else repenctrial_dists.append(j_d) if d == 14 \
                    else print("\nwrong assignment of {} for {} and {}\n".format(dimensions[d], ref, pair))
                    ind_dists.append(j_d)
                    #ind_dists.append(distance.jaccard(ref_dim, pair_dim))

            elif d == 0: #AGE

                # initial setup of lists and sets for Age calculation
                set_a = set(np.where(ref_dim == 1)[1] + 1) # set of which age groups were tested in ref(first)
                list_set_a = list(set_a) # as list
                set_b = set(np.where(pair_dim == 1)[1] + 1) # set of which age groups were tested in pair(second)
                list_set_b = list(set_b) # as list
                diff_a = set_a - set_b # which were tested in ref but not in pair
                list_diff_a = list(diff_a) # as list
                diff_b = set_b - set_a # which were tested in pair but not in ref
                list_diff_b = list(diff_b) # as list
                overlap = set_a & set_b # overlapping age groups tested
                dist_overlap = [0] *len(overlap) #count all overlaps as distance of 0 (i.e. similarity of 1), if none, then empty list!

                # now get the distances from all age groups that are only in ref
                already_used = [] # we store age groups that are already compared if they only occur in pair (this is to avoid double dipping)
                dists_a = [] # empty list to append the individual distances to
                comp_age = []
                if len(list_diff_a) != 0: # checking if there is an age group in ref that is not in pair
                    for e in list_diff_a: # for every age group
                        diff_array = abs(np.array(e) - np.array(list_set_b)) # difference to all age groups in pair
                        min_diff = min(diff_array) # get the smallest difference = smallest distance between age groups tested
                        dis_score = age_steps*min_diff # multiply the age_steps by the respective distance (=smallest difference)
                        #print('for {}: '.format(e),dis_score)
                        dists_a.append(dis_score) # append the distance score to the list of distances for ref
                        comp_age = list_set_b[np.where(diff_array == min_diff)[0][0]] # get the closest age group that was used for comparison
                        # there is the possibility that two age groups are closest to the one in ref:
                        # in these cases, we take the first one appearing in list_set_b and the other will still need comparison in second step for pair below
                        if comp_age in diff_b: # check whether this age group is only in pair
                            already_used.append(comp_age) # if yes, then we append it to our already_used list

                # now we remove all already used age groups from diff_b that would otherwise result in computing the same distance twice
                if len(already_used) != 0:
                    to_remove = np.unique(already_used) # we check the unique entries (could also be the same multiple times) in already used to get which age groups to remove in list_diff_b
                    for rem in to_remove:
                        list_diff_b.remove(rem)

                # now get the distances from the remaining age groups that are only in pair
                # same procedure as above with age groups only in ref (without last step of removing -> no need now)
                dists_b = []
                if len(list_diff_b) != 0:
                    for e in list_diff_b:
                        diff_array = abs(np.array(e) - np.array(list_set_a))
                        min_diff = min(diff_array)
                        dis_score = age_steps*min_diff
                        #print('for {}: '.format(e),dis_score)
                        dists_b.append(dis_score)

                # now we bring together all distances in one list and compute the average
                total_dists = dist_overlap + dists_a + dists_b
                age_dist = np.mean(total_dists)

                # now append the distance score to the ind_dists list for gathering the distances of every dimension
                age_dists.append(age_dist)
                ind_dists.append(age_dist)

            elif d == 3 or d == 4: # Imaging structural | Imaging functional

                if (np.sum(ref_dim, axis=1) == 0)[ref] and (np.sum(pair_dim, axis=1) == 0)[pair]:
                    imstruc_dists.append(nan) if d == 3 else imfunc_dists.append(nan) # leave out imaging dimension if both studies did not use any imaging struc/func
                    ind_dists.append(nan)

                elif (np.sum(ref_dim, axis=1) == 0)[ref] or (np.sum(pair_dim, axis=1) == 0)[pair]:
                    imstruc_dists.append(1) if d == 3 else imfunc_dists.append(1) # append a distance of 1 for that imaging dimension if only one has it and the other does not
                    ind_dists.append(1)

                else: # two more conditions: both imaging, but different technique -> 0.5 ; both imaging and the same technique -> 0

                    if list(ref_dim.iloc[0]) == list(pair_dim.iloc[0]): #if the arrays are the same after being checked that both contain at least one entry
                        imstruc_dists.append(0) if d == 3 else imfunc_dists.append(0)
                        ind_dists.append(0)

                    else:
                        imstruc_dists.append(0.5) if d == 3 else imfunc_dists.append(0.5)
                        ind_dists.append(0.5)


            elif d == 7: # Encoding Instructions

                if (np.where(ref_dim.iloc[0] == 1)[0][0]+1) == 4 and (np.where(pair_dim.iloc[0] == 1)[0][0]+1) == 4:
                    enc_dists.append(nan) #leave out if both are unspecified
                    ind_dists.append(nan)

                elif (np.where(ref_dim.iloc[0] == 1)[0][0]+1) == 4 or (np.where(pair_dim.iloc[0] == 1)[0][0]+1) == 4:
                    enc_dists.append(1) # append a distance of 1 for if one of the two encoding instructions are unspecified but the other is specified
                    ind_dists.append(1)

                elif list(ref_dim.iloc[0]) == list(pair_dim.iloc[0]): #if the arrays are the same (after checking for double entry in 4)
                    enc_dists.append(0) #distance of 0 (similarity of 1)
                    ind_dists.append(0)

                elif (np.where(ref_dim.iloc[0] == 1)[0][0]+1) == 3 or (np.where(pair_dim.iloc[0] == 1)[0][0]+1) == 3: #if one of the entries is a three, check the other

                    set_union = set(np.where(ref_dim.iloc[0] == 1)[0]+1) | set(np.where(pair_dim.iloc[0] == 1)[0]+1)
                    if 2 in set_union or 1 in set_union and 3 in set_union: #check for 2 or 1 in union and double checking the 3
                        enc_dists.append(0.5) #if one is 3 and the other 1 or 2, then we assign a distance of 0.5 for encoding instructions
                        ind_dists.append(0.5)
                    else:
                        enc_dists.append(1) #if one is 3 and the other is 5, then distance of 1
                        ind_dists.append(1)

                else: #for all other cases (comparison between 5,1,2), assign a distance of 1
                    enc_dists.append(1)
                    ind_dists.append(1)


            elif d == 9 or d == 10 or d == 11: # Similarity Manipulation at Encoding & Retrieval , Cue Manipulation

                # similar set up as for Age calculation with defining sets
                set_a = set(np.where(ref_dim == 1)[1] + 1) # set of which type(s) was used in ref(first)
                list_set_a = list(set_a) # as list
                set_b = set(np.where(pair_dim == 1)[1] + 1) # set of which type(s) was used in pair(second)
                list_set_b = list(set_b) # as list
                diff_a = set_a - set_b # which were tested in ref but not in pair
                list_diff_a = list(diff_a) # as list
                diff_b = set_b - set_a # which were tested in pair but not in ref
                list_diff_b = list(diff_b) # as list
                overlap = set_a & set_b # overlapping
                dist_overlap = [0] *len(overlap) #count all overlaps as distance of 0 (i.e. similarity of 1), if none, then empty list!
                dist_ab = []

                if len(set_a) == 1 and len(set_b) == 1: # first check whether both have only one entry (simple comparison)

                    set_union = set_a | set_b # define the union

                    if len(set_union) == 1: #if the union is a single number, then they overlap in their entry of that dimension -> distance of 0
                        simenc_dists.append(0) if d == 9 else simret_dists.append(0) if d == 10 else cuemanip_dists.append(0)
                        ind_dists.append(0)

                    elif d == 9 or d == 10: #if they don't and it is one of the sim manipulation dimensions

                        c_d = sim_manip_dismatrix[list(set_union)[0]-1,list(set_union)[1]-1] # index the matrix with values for respective combination in similarity manipulation
                        simenc_dists.append(c_d) if d == 9 else simret_dists.append(c_d)
                        ind_dists.append(c_d)

                    elif d == 11: #if it is cue manipulation dimension

                        cuemanip_dists.append(cue_manip_dismatrix[list(set_union)[0]-1,list(set_union)[1]-1]) # index the matrix with values for respective combination in cue manipulation
                        ind_dists.append(cue_manip_dismatrix[list(set_union)[0]-1,list(set_union)[1]-1])

                elif (len(set_a) == 1 and len(set_b) == 2) or (len(set_a) == 2 and len(set_b) == 1): # one set has one entry, the other has 2

                    if len(dist_overlap) != 0: #if one is overlapping, the other is automatically compared to empty entry(!) -> distance of 1
                        dist_ab = [1]

                    else:
                        # write code here for comparing both entries to the one entry
                        if len(list_set_a) > len(list_set_b): #if set_a has more entries (this checking can be taken out and replaced by a nested loop similar to that in modality)

                            if d == 9 or d == 10:
                                for e in list_set_a:
                                    dist_ab.append(sim_manip_dismatrix[e-1,list_set_b[0]-1])
                            else:
                                for e in list_set_a:
                                    dist_ab.append(cue_manip_dismatrix[e-1,list_set_b[0]-1])

                        elif len(list_set_b) > len(list_set_a): #if set_b has more entries

                            if d == 9 or d == 10:
                                for e in list_set_b:
                                    dist_ab.append(sim_manip_dismatrix[e-1,list_set_a[0]-1])
                            else:
                                for e in list_set_b:
                                    dist_ab.append(cue_manip_dismatrix[e-1,list_set_a[0]-1])

                    # now we calculate the mean of all distances
                    mean_dist = np.mean(dist_overlap + dist_ab)
                    simenc_dists.append(mean_dist) if d == 9 else simret_dists.append(mean_dist) if d == 10 else cuemanip_dists.append(mean_dist)
                    ind_dists.append(mean_dist)

                else: #only option left is that both have two entries (max of 2 entries)

                    if len(dist_overlap) == 2: #if overlap has two elements, then entries are the same and distance of 0 is appended
                        simenc_dists.append(0) if d == 9 else simret_dists.append(0) if d == 10 else cuemanip_dists.append(0)
                        ind_dists.append(0)

                    elif len(dist_overlap) == 1: #if overlap has one element, then compare the remaining entry of each

                        if d == 9 or d == 10:
                            dist_ab = sim_manip_dismatrix[list_diff_a[0]-1, list_diff_b[0]-1] #the different entries are used to acceess the distance matrix

                        else:
                            dist_ab = cue_manip_dismatrix[list_diff_a[0]-1, list_diff_b[0]-1] #the different entries are used to acceess the distance matrix

                        #now append the mean distance
                        mean_dist = np.mean(dist_overlap + dist_ab)
                        simenc_dists.append(mean_dist) if d == 9 else simret_dists.append(mean_dist) if d == 10 else cuemanip_dists.append(mean_dist)
                        ind_dists.append(mean_dist)

                    else: #no overlapping elements means we compare every entry to every other one (2x2)

                        if d == 9 or d == 10:
                            for a in list_set_a:
                                for b in list_set_b:
                                    dist_ab.append(sim_manip_dismatrix[a-1, b-1])

                        else:
                            for a in list_set_a:
                                for b in list_set_b:
                                    dist_ab.append(cue_manip_dismatrix[a-1, b-1])

                        simenc_dists.append(np.mean(dist_ab)) if d == 9 else simret_dists.append(np.mean(dist_ab)) if d == 10 else cuemanip_dists.append(np.mean(dist_ab))
                        ind_dists.append(np.mean(dist_ab))


            elif d == 13: #Modality

                if (np.sum(ref_dim, axis=1) == 0)[ref] and (np.sum(pair_dim, axis=1) == 0)[pair]:
                    mod_dists.append(nan) #if both do not have an entry, leave out for calculation
                    ind_dists.append(nan)

                elif (np.sum(ref_dim, axis=1) == 0)[ref] or (np.sum(pair_dim, axis=1) == 0)[pair]:
                    mod_dists.append(1) #if one has an entry but the other does not -> distance of 1
                    ind_dists.append(1)

                elif (np.sum(ref_dim, axis=1) == 1)[ref] and (np.sum(pair_dim, axis=1) == 1)[pair]:
                    #if both have a single entry then find the respective distance in mod_dismatrix (can also be 0 if both are the same)
                    mod_dists.append(mod_dismatrix[int(np.where(pair_dim == 1)[1]),int(np.where(ref_dim == 1)[1])])
                    ind_dists.append(mod_dismatrix[int(np.where(pair_dim == 1)[1]),int(np.where(ref_dim == 1)[1])])

                else:

                    # similar set up as for Age calculation with defining sets
                    set_a = set(np.where(ref_dim == 1)[1] + 1) # set of which type(s) was used in ref(first)
                    list_set_a = list(set_a) # as list
                    set_b = set(np.where(pair_dim == 1)[1] + 1) # set of which type(s) was used in pair(second)
                    list_set_b = list(set_b) # as list
                    diff_a = set_a - set_b # which were tested in ref but not in pair
                    list_diff_a = list(diff_a) # as list
                    diff_b = set_b - set_a # which were tested in pair but not in ref
                    list_diff_b = list(diff_b) # as list
                    overlap = set_a & set_b # overlapping
                    dist_overlap = [0] *len(overlap) #count all overlaps as distance of 0 (i.e. similarity of 1), if none, then empty list!
                    dist_ab = []

                    if len(set_a) != len(set_b):
                        #if the sets are not the same length
                        if len(diff_a) == 0 or len(diff_b) == 0:
                            #if one or the other difference is empty, then we want to add as many distances of 1 to the calculation as the length of the difference array
                            dist_ab = [1]*len(diff_a) + [1]*len(diff_b)

                        else:
                            #if there is at least one element in both differences, get all possible comparisons between the differences
                            for a in list_diff_a:
                                for b in list_diff_b:
                                    dist_ab.append(mod_dismatrix[a-1, b-1])

                    else:
                        #if the sets do have the same length
                        if len(list_diff_a) != 0 and len(list_diff_b) != 0:
                            #the difference arrays are not zero -> compare all entries in the difference arrays to each other
                            for a in list_diff_a:
                                for b in list_diff_b:
                                    dist_ab.append(mod_dismatrix[a-1, b-1])

                        #if one has zero elements, the other must have zero as well and all are overlapping elements -> move on to calculating mean distance

                    #append the mean distance
                    mean_dist = np.mean(dist_overlap + dist_ab)
                    mod_dists.append(mean_dist)
                    ind_dists.append(mean_dist)

            elif d == 15: #Delay

                if (np.sum(ref_dim, axis=1) == 0)[ref] and (np.sum(pair_dim, axis=1) == 0)[pair]:
                    delay_dists.append(nan) #if both do not have an entry, leave out for calculation
                    ind_dists.append(nan)

                elif (np.sum(ref_dim, axis=1) == 0)[ref] or (np.sum(pair_dim, axis=1) == 0)[pair]:
                    delay_dists.append(1) #if one has an entry but the other does not -> distance of 1
                    ind_dists.append(1)

                elif (np.sum(ref_dim, axis=1) == 1)[ref] and (np.sum(pair_dim, axis=1) == 1)[pair]:
                    #if both have a single entry then find the respective distance in between the two bins (can also be 0 if both are the same)
                    single_del_dist = abs(int(np.where(pair_dim == 1)[1]) - int(np.where(ref_dim == 1)[1])) #get the absolute difference between the two delay bins
                    delay_dists.append(delay_steps*single_del_dist) #append the delay_steps x the absolute difference as distance for delay
                    ind_dists.append(delay_steps*single_del_dist)

                else: #now if at least one has 2 and the other is not zero, the rest of the possible cases have to be checked

                    # similar set up as for Age calculation with defining sets
                    set_a = set(np.where(ref_dim == 1)[1] + 1) # set of which type(s) was used in ref(first)
                    list_set_a = list(set_a) # as list
                    set_b = set(np.where(pair_dim == 1)[1] + 1) # set of which type(s) was used in pair(second)
                    list_set_b = list(set_b) # as list
                    diff_a = set_a - set_b # which were tested in ref but not in pair
                    list_diff_a = list(diff_a) # as list
                    diff_b = set_b - set_a # which were tested in pair but not in ref
                    list_diff_b = list(diff_b) # as list
                    overlap = set_a & set_b # overlapping
                    dist_overlap = [0] *len(overlap) #count all overlaps as distance of 0 (i.e. similarity of 1), if none, then empty list!
                    dist_ab = []

                    # now get the distances from all delay bins that are only in ref
                    already_used = [] # we store entries that are already compared if they only occur in pair (this is to avoid double dipping)
                    dists_a = [] # empty list to append the individual distances to
                    comp_delay = []
                    if len(list_diff_a) != 0: # checking if there is a delay bin in ref that is not in pair
                        for e in list_diff_a: # for every delay bin
                            diff_array = abs(np.array(e) - np.array(list_set_b)) # difference to all delay bins in pair
                            min_diff = min(diff_array) # get the smallest difference = smallest distance between delay bins
                            dis_score = delay_steps*min_diff # multiply the delay_steps by the respective distance (=smallest difference)

                            dists_a.append(dis_score) # append the distance score to the list of distances for ref
                            comp_delay = list_set_b[np.where(diff_array == min_diff)[0][0]]; # get the closest delay bin that was used for comparison
                            # there is the possibility that two bins are closest to the one in ref:
                            # in these cases, we take the first one appearing in list_set_b and the other will still need comparison in second step for pair below
                            if comp_delay in diff_b: # check whether this delay bin is only in pair
                                already_used.append(comp_delay) # if yes, then we append it to our already_used list

                    # now we remove all already used delay bins from diff_b that would otherwise result in computing the same distance twice
                    if len(already_used) != 0:
                        to_remove = np.unique(already_used) # we check the unique entries (could also be the same multiple times) in already used to get which delay bins to remove in list_diff_b
                        for rem in to_remove:
                            list_diff_b.remove(rem)

                    # now get the distances from the remaining delay bins that are only in pair
                    # same procedure as above with delay bins only in ref (without last step of removing -> no need now)
                    dists_b = []
                    if len(list_diff_b) != 0:
                        for e in list_diff_b:
                            diff_array = abs(np.array(e) - np.array(list_set_a))
                            min_diff = min(diff_array)
                            dis_score = age_steps*min_diff
                            #print('for {}: '.format(e),dis_score)
                            dists_b.append(dis_score)

                    # now we bring together all distances in one list and compute the average
                    total_dists = dist_overlap + dists_a + dists_b
                    delay_dist = np.mean(total_dists)

                    # now append the distance score to the ind_dists list for gathering the distances of every dimension
                    delay_dists.append(delay_dist)
                    ind_dists.append(delay_dist)


        # now we measure the mean distance across all dimensions
        w_dist = np.nanmean(ind_dists)
        dists.append(w_dist)


    c +=1 # add 1 to c as to keep the starting index of the comparison correct
    print('row nr. {}: done'.format(ref+1)) # print finished row for keeping track of position
    sys.stdout.flush()

# make pd.DataFrame of all dimenstions
dist_constrained = pd.DataFrame(distance.squareform(dists))
sim_constrained = 1 - dist_constrained

#adding Entry_ID
dist_constrained.insert(0, 'Entry_ID', data_lit_bin['Entry_ID'])
sim_constrained.insert(0, 'Entry_ID', data_lit_bin['Entry_ID'])

#save total as csv files
dist_constrained.to_csv(filepath + '02b_Constrained/distance_constrained.csv', index = False)
sim_constrained.to_csv(filepath + '02b_Constrained/similarity_constrained.csv', index = False)

#save individual vectors as csv files
#saving individual dimension values as column vectors in csv format
age_pd = pd.DataFrame(age_dists)
age_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/age_vec.csv', index = False)
design_pd = pd.DataFrame(design_dists)
design_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/design_vec.csv', index = False)
eyetrack_pd = pd.DataFrame(eyetrack_dists)
eyetrack_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/eyetrack_vec.csv', index = False)
imstruc_pd = pd.DataFrame(imstruc_dists)
imstruc_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/imstruc_vec.csv', index = False)
imfunc_pd = pd.DataFrame(imfunc_dists)
imfunc_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/imfunc_vec.csv', index = False)
tasktype_pd = pd.DataFrame(tasktype_dists)
tasktype_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/tasktype_vec.csv', index = False)
tbri_pd = pd.DataFrame(tbri_dists)
tbri_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/tbri_vec.csv', index = False)
enc_pd = pd.DataFrame(enc_dists)
enc_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/enc_vec.csv', index = False)
ret_pd = pd.DataFrame(ret_dists)
ret_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/ret_vec.csv', index = False)
simenc_pd = pd.DataFrame(simenc_dists)
simenc_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/simenc_vec.csv', index = False)
simret_pd = pd.DataFrame(simret_dists)
simret_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/simret_vec.csv', index = False)
cuemanip_pd = pd.DataFrame(cuemanip_dists)
cuemanip_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/cuemanip_vec.csv', index = False)
stim_pd = pd.DataFrame(stim_dists)
stim_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/stim_vec.csv', index = False)
mod_pd = pd.DataFrame(mod_dists)
mod_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/mod_vec.csv', index = False)
repenctrial_pd = pd.DataFrame(repenctrial_dists)
repenctrial_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/repenctrial_vec.csv', index = False)
delay_pd = pd.DataFrame(delay_dists)
delay_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/delay_vec.csv', index = False)
dists_pd = pd.DataFrame(dists)
dists_pd.to_csv(filepath + '02b_Constrained/SingleDimensions/constrained_totaldist_vec.csv', index = False)
entry_IDs = data_lit_bin[['Entry_ID']]
entry_IDs.to_csv(filepath + '02b_Constrained/SingleDimensions/EntryID.csv', index = False)

#Print finish message:
print('\n\n Finished! Files saved under\n', filepath + '02b_Constrained/', '\n and\n', filepath + '02b_Constrained/SingleDimensions/')
