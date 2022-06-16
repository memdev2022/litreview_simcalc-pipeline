library(rstudioapi)
library(dplyr)
library(tidyverse)
library(tidyr)

library(readxl)
library(writexl)
library(reshape2) 
library(stringr) 
library(fastDummies)

# Plotting
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager") # BiocManager is requisite for ComplexHeatMap
install.packages('ComplexHeatmap')
library(ComplexHeatmap)
library(ggplot2)
library(RColorBrewer)
library(circlize)
