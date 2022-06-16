# This script arranges entries by task type (inferred from original dataset)
# Then, it produces a heatmap of the matrix, but entries are arranged by task type
if (interactive() ){

{
  library(dplyr)
  library(rstudioapi)
  library(tidyverse)
  library(readxl)
  library(RColorBrewer)
  library(circlize)
  if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
  # install.packages('ComplexHeatmap')
  library(ComplexHeatmap)
}

# {
#   directory = dirname(getSourceEditorContext()$path) %>% str_extract(pattern = '[^simcalc-pipeline]+') %>% file.path("simcalc-pipeline")
#   data_path = file.path(directory,'data_files')
#   script_path = file.path(directory,'scripts') 
#   funcon_path = file.path(directory,'supplementary_files')
#   result_path = file.path(directory,'visualization')
#   setwd(directory)
# }



# Cosmetics
{source(file.path(funcon_path, "PN_GetPalette.R"))}


# STEP 1: extract rearranged Entry_ID ----

# Task type was stored in the original QC dataframe as well as its preprocessed dataframe (dfQC)
# let's retrieve this QC sheet, find those PC entries



# Get the original QC
dfQC <- read_xlsx(file.path(data_path,'Lit_Review_Preprocessed.xlsx'))
  
 
# get Entry_IDs of interest (could be arranged/filtered/manipulated)
dfQC.filtered <- dfQC %>% arrange(Task_type) # user can adapt here
dfQC.filtered.Entry_ID = dfQC.filtered$Entry_ID


# STEP 2: get position of the arranged entries in the similarity matrix and rearrange matrix----


# Choose which matrix file to make heatmap
allDataFiles = list.files(data_path, recursive = T)
matSimVersion = readline("Which version of similarity matrix to make heatmap (1=constrained; 2=unconstrained) >>> ") %>%
  str_replace_all(c("1" = "constrained", "2" = "unconstrained"))
matSimFile = allDataFiles[allDataFiles %>% str_detect(sprintf('similarity_%s.csv', matSimVersion))]

# Retrieve the similarity matrix [matSim]
matSim <- read.csv(file.path(data_path,matSimFile), encoding = 'UTF-8')
rownames(matSim) = matSim$Entry_ID
names(matSim) = c('Entry_ID', matSim$Entry_ID)

# match the goal positions with the current matrix positions
rowOrder = match(dfQC.filtered.Entry_ID, rownames(matSim %>% select(-Entry_ID))) 
colOrder = match(dfQC.filtered.Entry_ID, names(matSim %>% select(-Entry_ID)))
rowOrder==colOrder


# STEP 3: get a similarity matrix ordered by Task type ----
# reorder
matSim.filtered = (matSim %>% select(-Entry_ID))[rowOrder,colOrder] %>% as.matrix()
matSim.filtered.Entry_ID = matSim.filtered %>% rownames()

# # optional: delete the lower half of the matrix
# matSim.filtered[lower.tri(matSim.filtered)] <- NA



# STEP 4: plot matrix ----
# https://www.datanovia.com/en/lessons/heatmap-in-r-static-and-interactive-visualization/#r-packagesfunctions-for-drawing-heatmaps

Entry_ID <- matSim.filtered.Entry_ID
Task_type <- dfQC.filtered$Task_type
nTask_type <- unique(Task_type) %>% length()

# add annotation for task type
ha_top <- HeatmapAnnotation(Task_type = Task_type, 
                            annotation_label = "Task type",
                            col = list(Task_type = c("1" = TaskTypelevelPalette[1],
                                                     "2" = TaskTypelevelPalette[2],
                                                     "3" = TaskTypelevelPalette[3],
                                                     "4" = TaskTypelevelPalette[4],
                                                     "5" = TaskTypelevelPalette[5])))
ha_left <- rowAnnotation(Task_type = Task_type,
                         col = list(Task_type = c("1" = TaskTypelevelPalette[1],
                                                  "2" = TaskTypelevelPalette[2],
                                                  "3" = TaskTypelevelPalette[3],
                                                  "4" = TaskTypelevelPalette[4],
                                                  "5" = TaskTypelevelPalette[5])),
                         show_annotation_name = c(bar = FALSE),
                         show_legend = c("bar" = FALSE))
  
# make plot
{
  pdf(file.path(result_path,sprintf("Heatmap_similarity_%s.pdf",matSimVersion)))
  p = Heatmap(matSim.filtered, name = "Similarity",
              col = colorRamp2(seq(0,1,.2), rev(heatmatrixPalette)),
              heatmap_legend_param = list(at = seq(0,1,.2)),
              cluster_columns = F, cluster_rows = F,
              show_row_names = FALSE, show_column_names = FALSE,
              top_annotation = ha_top,
              left_annotation = ha_left,
              width = unit(5, "in"), height = unit(5,"in"))
  print(p)
  dev.off()
}

}


