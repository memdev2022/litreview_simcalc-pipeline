rm(list=ls())

#check for rstudioapi first, since we need this for getting the root directory of the repository:
{ a = ''
if('rstudioapi' %in% installed.packages()){
  library(rstudioapi)
  rm(a)
} else {
    print('rstudioapi required for finding root directory of repository on local system, but not istalled.')
    while (a != 'y' & a!= 'n') {
      a = readline('do you want to directly istall rstudioapi?(y/n)')
    }
    if(a == 'y'){
      install.packages('rstudioapi')
      rm(a)
    } else{
      warning('rstudioapi not downloaded. Please do this on your own and run from the top again. 
Or manually assign the root directory of the repo on your local system to the "directory" variable below')
      } 
    rm(a)
}
}

# Set up working directories and paths
# in RStudio: Session >> Set Working Directory >> To Source File Location
{
  directory = dirname(rstudioapi::getSourceEditorContext()$path)
  data_path = file.path(directory,'data_files/')
  script_path = file.path(directory,'scripts/') 
  funcon_path = file.path(directory,'supplementary_files/')
  result_path = file.path(directory,'visualization/')
  
  #setwd to directory
  setwd(directory)
  
}

#check for all other R packages to be installed and load everything relevent:
source(file.path(funcon_path, 'CheckRPackages.R'))

# Step 1. Preprocess and binarize the complete data frame----
source(local = FALSE,echo = TRUE,print.eval = TRUE,verbose = FALSE,
       file= file.path(script_path,"01-1_Preprocessing.R"))

source(local = FALSE,echo = TRUE,print.eval = TRUE,verbose = FALSE,
       file= file.path(script_path,"01-2_Binarize.R"))


# Step 2. Compute similarity matrix ----

# Always run this to get python started in R !!
library(reticulate)
#checking for correct python version + if python works
source(file.path(funcon_path, 'CheckPyInR.R')); CheckPy()
#if you get an error, uncomment below for troubleshoot script to find python location on computer and use it to attatch to reticulate
#rstudioapi::restartSession("source(file.path(funcon_path, 'ts_py.R'))")


#checking if all python packages are available for reticulate
source(file.path(funcon_path, 'CheckPackagesReticulate.R')) 
#if something does not work running the line above or somehow you get an error later in the script running the python scripts,
#try running this line:
#py_run_file(file.path(funcon_path, 'CheckPackages.py'))


# Choose a py script to compute similarity matrix in constrained/unconstrained version (preferably, you run both after each other)
matrixScript = readline("Decide the version of the similarity matrix (1=constrained; 2=unconstrained) >>> ") %>% as.character() %>%
  str_replace_all(c(`2` = "02a_UnconstrainedSimilarity.py", `1` = "02b_ConstrainedSimilarity.py"))


#create path to script
py.path = file.path(script_path, matrixScript)
#run calculation: this can take up to a few hours, depending on which version you calculate and on your computer's processing speed
py_run_file(py.path)

# Additional Step: Dimsensions of Interest (!!!only run after running the above Step2 calculations!!!) ----

#we want to load the module into R via reticulate
DimsOfInterest = import_from_path(module = 'DimsOfInterest', path = script_path)
#if additional info on makematrix function is wanted, run the help below:
py_help(DimsOfInterest$make_matrix)
#Information on make_matrix():

# This is a function to create a distance or similarity matrix from the individual dimensions used to obtain the total similarity/distance scores.
# It takes the arguments
# - version ('constrained' (default) or 'unconstrained') specifying which calculation model to use,
# - type ('similarity' (default), 'distance' or 'both') specifying if the matrix should be similarity (1 on the diagonal) or distance (0 on the diagonal) or both (NOTE: similarity matrix = 1 - distance matrix),
# - dims, which is a character vector/list comprising of the following dimensions: 
# age, design, eyetrack, imstruc, imfunc, tasktype, tbri, enc, ret, simenc, simret, cuemanip, stim, mod, repenctrial, delay

#specify your function arguments:
source(file.path(funcon_path, 'specify_doi_args.R')); arguments = specify_doi_args()

try_func = try(DimsOfInterest$make_matrix(version = arguments$v, type = arguments$t, dims = arguments$d))
#If importing the module above somehow does not work directly, try using the R function that calls python via reticulate below:
if(class(try_func) == 'try-error'){
  source(file.path(funcon_path, 'DimsOfInterest_FunctionR.R'))
  try(make_matrix(version = arguments$v, type = arguments$t, dims = arguments$d))
}




# Step 3. Plot heatmap for the total matrix ----
# Run the script below. You will be asked to define which version of heatmap to produce (1=constrained, 2=unconstrained)
source(local = FALSE,echo = TRUE,print.eval = TRUE,verbose = FALSE,
       file= file.path(script_path,"03_Heatmap_constrained.R"))


# Step 4. Get dataframe for the top most similar pairs ----
# This script turns the similarity matrix to a dataframe, then it rearranges the dataframe from the most to the least similar pairs of entries.
# You will be asked to define a version of this ranked data frame (1=constrained, 2=unconstrained)

source(local = FALSE,echo = TRUE,print.eval = TRUE,verbose = FALSE,
       file= file.path(script_path,"04_Most-similar-pair_constrained.R"))


# Step 5. Visualiza pairwise similarity by task type ----
# Run the script below to draw boxplots comparing within-task and between-task similarity
source(local = FALSE,echo = TRUE,print.eval = TRUE,verbose = FALSE,
       file= file.path(script_path,"05_Boxplot_TaskSimilarity.R"))

