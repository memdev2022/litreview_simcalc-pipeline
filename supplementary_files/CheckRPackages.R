#CHECK for all necessary R packages

message("Checking if all R packages required are installed on system..\n")

#istalled packages
ins_pac = installed.packages()
#required packages
pckgs = c('rstudioapi', 'tidyverse', 'dplyr', 'tidyr', 'ggplot2', 'readxl', 'writexl', 'reshape2',
          'reticulate', 'stringr', 'fastDummies', 'BiocManager', 'ComplexHeatmap', 'RColorBrewer', 
          'rstatix', 'circlize')

#checking all required
for (p in 1:length(pckgs)){
  a=''
  if (pckgs[p] %in% rownames(ins_pac)){
    library(pckgs[p], character.only = T)
    message(paste0(pckgs[p],  ' available & loaded!'))
  } else{
    while(a != 'y' & a != 'n'){
      a = readline(paste0(pckgs[p],  ' not installed, but required! Do you want to install it?(y/n)'))
    }
    if(a == 'y'){
      install.packages(pckgs[p])
      library(pckgs[p], character.only = T)
      message(paste0(pckgs[p],  ' installed & loaded!'))
    } else{
      warning(paste0('"', pckgs[p], '" required for running script. Please make sure to install before continuiung!'))
    }
  }
}
#removing variables not needed anymore
rm(ins_pac, a, pckgs, p)