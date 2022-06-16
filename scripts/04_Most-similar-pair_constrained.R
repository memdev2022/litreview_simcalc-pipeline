# This script extract pairwise similarity of selected entries.


# I will use pattern-completion entries as example:
# Filter entries which investigated Pattern Completion (PC)
# Similarity scores are retrieved from the constrained version


if (interactive() ){
{
  library(dplyr) 
  library(tidyverse) 
  library(readxl) 
  library(reshape2) 
  library(stringr) 
  library(writexl)
  
}

# {
#   directory = dirname(getSourceEditorContext()$path) %>% str_extract(pattern = '[^simcalc-pipeline]+') %>% file.path("simcalc-pipeline")
#   data_path = file.path(directory,'data_files/')
#   script_path = file.path(directory,'scripts/') 
#   funcon_path = file.path(directory,'supplementary_files/')
#   result_path = file.path(directory,'visualization/')
# }



# We want to get pairwise similarity of PC entries only
# To do this, we have to get the right Entry_IDs and then find
# their position in the matrix


# STEP 1: extract Entry_ID ----

# Pattern completion was stored in the preprocessed QC data frame (dfQC)
# let's retrieve this QC sheet, find those PC entries
dfQC <- read_xlsx(file.path(data_path,'Lit_Review_Preprocessed.xlsx')) # choose: Lit_Review_QC.xlsx

# get Entry_IDs of interest
dfQC.filtered <- dfQC# %>% filter(PS == 1)
dfQC.filtered.Entry_ID = dfQC.filtered$Entry_ID

# STEP 2: get position of the PC-entries in the similarity matrix ----

# Choose which version of matrix file to use
allDataFiles = list.files(data_path, recursive = T)
matSimVersion = readline("Choose a version of similarity matrix (1=constrained; 2=unconstrained) >>> ") %>%
  str_replace_all(c("1" = "constrained", "2" = "unconstrained"))
matSimFile = allDataFiles[allDataFiles %>% str_detect(sprintf('similarity_%s.csv', matSimVersion))]

# Retrieve the similarity matrix [matSim]
matSim <- read.csv(file.path(data_path,matSimFile), encoding = 'UTF-8')
rownames(matSim) = matSim$Entry_ID
names(matSim) = c('Entry_ID', matSim$Entry_ID)

# match the goal positions with the current matrix positions
rowOrder = match(dfQC.filtered.Entry_ID, rownames(matSim %>% select(-Entry_ID))) 
colOrder = match(dfQC.filtered.Entry_ID, names(matSim %>% select(-Entry_ID)))



# STEP 3: get a similarity matrix with only PC-entries ----
# reorder
matSim.filtered = (matSim %>% select(-Entry_ID))[rowOrder,colOrder] %>% as.matrix()
matSim.filtered.Entry_ID = matSim.filtered %>% rownames()


# delete the lower half of the matrix
matSim.filtered[lower.tri(matSim.filtered)] <- NA

# Prepare for data manipulation
# transform matrix to data frame: its columns and rows are identified by Entry_ID
dfSim.filtered <- matSim.filtered %>% 
  as.data.frame() %>%
  mutate(Entry1 = matSim.filtered.Entry_ID) # first column = Entry_ID
names(dfSim.filtered) = c(matSim.filtered.Entry_ID, "Entry1") # other columns = Entry_ID

# Melt the dfSim to get a long format
dfSim.filtered <- melt(dfSim.filtered,
                      id.vars = "Entry1",
                      variable.name = "Entry2",
                      value.name = "Similarity")

# We only allow the following similarity scores:
# >>>> similarity score between an entry with another entry other than itself
# >>>> similarity score that is not NA (because we deleted the lower half of the matrix)
dfSim.filtered <- dfSim.filtered %>% 
  filter(Entry1 != Entry2,
         !(is.na(Similarity)))

# Add title of entries
dfSim.filtered <- left_join(dfSim.filtered, dfQC.filtered %>% select(Entry_ID, Title), by = c("Entry1"="Entry_ID"))
names(dfSim.filtered)[names(dfSim.filtered) == "Title"] <- "Title1"
dfSim.filtered <- left_join(dfSim.filtered, dfQC.filtered %>% select(Entry_ID, Title), by = c("Entry2"="Entry_ID"))
names(dfSim.filtered)[names(dfSim.filtered) == "Title"] <- "Title2"


# Last,
# We rank order of highest to lowest pairwise similarity
dfSim.ranked <- dfSim.filtered %>%
  arrange(desc(Similarity))



# SAVE DATA FILE ----
# This will be saved in [...//simcalc-pipeline/data_files/TopSimPair_PC_....xlsx]
writexl::write_xlsx(dfSim.ranked, file.path(data_path, sprintf("TopSimPair_PC_%s.xlsx", matSimVersion)))

}
