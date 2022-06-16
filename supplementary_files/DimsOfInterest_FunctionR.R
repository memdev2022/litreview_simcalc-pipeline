#locating file location and reticulate package
script_location = dirname(sys.frame(1)$ofile)
setwd(file.path(script_location, '..'))
rm(script_location)
library(reticulate)

make_matrix <- function(version = 'constrained', type = 'similarity', dims = character()) {
  #We have as default values the constrained model and a similarity matrix

  if (!endsWith(getwd(), 'simcalc-pipeline')){
    stop('WorkingDirectory not correct. Please run source() on the "DimsOfInterest_FunctionR.R" file inside the "supplementary_files" directory again or switch manually to the root directory of the repository (simcalc-pipeline) before running function again!')
  }

  if (version != 'constrained' && version != 'unconstrained'){
    stop("version argument must be either 'unconstrained' or 'constrained' (default), please edit input argument!")
  }

  if (type != 'similarity' && type != 'distance' && type != 'both'){
    stop("type argument must be either both, 'distance' or 'similarity' (default), please edit input argument!")
  }

  if (length(dims) != 0){
    dims_4py = c('[')
    for(d in 1:length(dims)){
      if (d != length(dims)){
        dims_4py = paste0(dims_4py, "'", dims[d], "',")
      } else{
        dims_4py = paste0(dims_4py, "'", dims[d], "']")
      }
    }
  }else{
    stop("No dimensions supplied, please input dimensions of interest as character vector to the 'dims' argument!")
  }

  pystring = paste0("from scripts import DimsOfInterest; DimsOfInterest.make_matrix('",version,"','",type,"', dims = ",dims_4py,")")
  #this can be added at the beginning of the arguments if we have some global commands to run with required modules:
  #from supplementary_files.ImportDOI import *; 
  
  #sending function arguments to python function
  py_run_string(pystring)

}
