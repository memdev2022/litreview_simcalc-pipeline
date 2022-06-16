# This script transform similarity matrix into a long format.Each row informs a pairwise similarity between two entries.
# It also informs which task type each of the two entries belong to.
# Then, it produces a box of the matrix to reveal within-group and between-group similarities

{
  library(dplyr)
  library(tidyverse)
  library(readxl)
  library(ggplot2)
}

{
  directory = dirname(getSourceEditorContext()$path) %>% str_extract(pattern = '[^simcalc-pipeline]+') %>% file.path("simcalc-pipeline")
  data_path = file.path(directory,'data_files')
  script_path = file.path(directory,'scripts') 
  funcon_path = file.path(directory,'supplementary_files')
  result_path = file.path(directory,'visualization')
  setwd(directory)
}


# Cosmetics
{source(file.path(funcon_path, "PN_GetPalette.R"))}


# STEP 1: extract Entry_ID ----

# Task type was stored in the original QC dataframe as well as its preprocessed dataframe (dfQC)
# let's retrieve this QC sheet, find those PC entries

# Get the original QC
dfQC <- read_xlsx(file.path(data_path,'Lit_Review_Preprocessed.xlsx'))

# get Entry_IDs of interest (could be arranged/filtered/manipulated)
dfQC.filtered <- dfQC %>% arrange(Task_type) # user can adapt here
dfQC.filtered.Entry_ID = dfQC.filtered$Entry_ID


# STEP 2: get position of the arranged entries in the similarity matrix and rearrange matrix ----
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


# STEP 3: get a similarity matrix rearranged ----
# reorder
matSim.filtered = (matSim %>% select(-Entry_ID))[rowOrder,colOrder] %>% as.matrix()
matSim.filtered.Entry_ID = matSim.filtered %>% rownames()

# STEP 4: make dfs ----
# https://www.datanovia.com/en/lessons/heatmap-in-r-static-and-interactive-visualization/#r-packagesfunctions-for-drawing-heatmaps
nEntry = nrow(matSim.filtered)
ingroup <- list(Tt1 = which(dfQC.filtered$Task_type == 1),
                Tt2 = which(dfQC.filtered$Task_type == 2),
                Tt3 = which(dfQC.filtered$Task_type == 3),
                Tt4 = which(dfQC.filtered$Task_type == 4),
                Tt5 = which(dfQC.filtered$Task_type == 5))

outgroup <- list(Tt1 = setdiff(c(1:nEntry), ingroup$Tt1),
                 Tt2 = setdiff(c(1:nEntry), ingroup$Tt2),
                 Tt3 = setdiff(c(1:nEntry), ingroup$Tt3),
                 Tt4 = setdiff(c(1:nEntry), ingroup$Tt4),
                 Tt5 = setdiff(c(1:nEntry), ingroup$Tt5))

# Individual pair
dfContrast = data.frame()
for (i in 1:nrow(matSim.filtered)) {
  
  # i = currently processed row
  # For each entry, get ingroup = which task type group it belongs to
  if (i %in% ingroup$Tt1) {current_ingroup1 = '1'}
  if (i %in% ingroup$Tt2) {current_ingroup1 = '2'}
  if (i %in% ingroup$Tt3) {current_ingroup1 = '3'}
  if (i %in% ingroup$Tt4) {current_ingroup1 = '4'}
  if (i %in% ingroup$Tt5) {current_ingroup1 = '5'}
 
  # j = currently processed column, and we only process the upper half of the matrix >> until row j=i 
  for (j in 1:i) {
    
    if (j < i ) {
      
      print(j)
      
      if (j %in% ingroup$Tt1) {current_ingroup2 = '1'}
      if (j %in% ingroup$Tt2) {current_ingroup2 = '2'}
      if (j %in% ingroup$Tt3) {current_ingroup2 = '3'}
      if (j %in% ingroup$Tt4) {current_ingroup2 = '4'}
      if (j %in% ingroup$Tt5) {current_ingroup2 = '5'}
      
      
      current_Contrast = sprintf('%svs%s', current_ingroup1, current_ingroup2)
      current_Similarity = matSim.filtered[i,j]
      current_dfContrast = data.frame(Contrast = current_Contrast, Similarity = current_Similarity, start = current_ingroup1, end = current_ingroup2)
      
      dfContrast = rbind(dfContrast, current_dfContrast)
      
    }
    
    
  }
  
  
}






# STEP 5: boxplot ----

pdf(file.path(result_path,sprintf("Boxplot_individualdata_%s.pdf",matSimVersion)))
p=ggplot(dfContrast)+
  geom_jitter(aes(x=0, y=Similarity, color=start), alpha = .1, show.legend = F)+
  geom_boxplot(aes(x=0, y=Similarity), color = 'black')+
  scale_color_manual(values = TaskTypelevelPalette)+
  ylim(0,1)+
  facet_grid(start~end)+ coord_fixed(ratio = 1)+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())
print(p)
dev.off()

  


# Step 6: descriptives ----
library(rstatix)
summary_dfContrast <- dfContrast %>%
  group_by(Contrast) %>%
  get_summary_stats(Similarity)
writexl::write_xlsx(dfContrast, file.path(data_path, sprintf("IntertaskSimilarity_%s.xlsx", matSimVersion)))
