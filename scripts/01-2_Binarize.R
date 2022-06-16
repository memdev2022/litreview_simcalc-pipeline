# Load packages
{
  library(dplyr)
  library(tidyverse)
  library(readxl)
  library(fastDummies)
  library(reshape2)
  library(stringr)
  library(writexl)
  library(rstudioapi)
}

{
  directory = dirname(getSourceEditorContext()$path) %>% str_extract(pattern = '[^simcalc-pipeline]+') %>% file.path("simcalc-pipeline")
  data_path = file.path(directory,'data_files')
  script_path = file.path(directory,'scripts') 
  funcon_path = file.path(directory,'supplementary_files')
  result_path = file.path(directory,'visualization')
  setwd(directory)
}

# Read data set
reviewtable <- read_xlsx(file.path(data_path,'Lit_Review_Preprocessed.xlsx'))
identifier_var <- c("Entry_ID", "Authors","Title", "Year")


#....................................................................................................
# Variable                              | Data type                                | Transform to    
# ...................................................................................................
# Entry_ID                              | character                                |.                
# Age                                   | numerical, binary                        |binary           
# Design                                | numerical, non-binary categorical        |binary           
# Eye tracking                          | numerical, binary                        |binary           
# Imaging_structural/functional         | numerical, non-binary categorical        |binary           
# Task_type                             | numerical, non-binary categorical        |binary           
# To-be-remembered-info                 | numerical, non-binary categorical        |binary           
# Encoding_instruction                  | numerical, non-binary categorical        |binary           
# Repetition_of_encoding                | numerical, non-binary categorical        |binary           
# Retrieval_mode                        | numerical, non-binary categorical        |binary           
# Similiarity_Manipulation_Encoding     | numerical, non-binary categorical        |binary           
# Similiarity_Manipulation_Retrieval    | numerical, non-binary categorical        |binary           
# Cue manipulation                      | numerical, non-binary categorical        |binary           
# Stimuli                               | numerical, non-binary categorical        |binary           
# Modality                              | numerical, non-binary categorical        |binary           
# Repetition                            | numerical, non-binary categorical        |binary           
# Delay                                 | numerical, not binned                    |binary           
#....................................................................................................




# Binarize data set with a customized functions ----
{source(file.path(funcon_path, "PN_BinarizeDataset.R"))}
df_main <- PN_BinarizeDataset(reviewtable,identifier_var)

# Polish variable , e.g., from Stimuli__1 to Stimuli_1
non_indentifier <- df_main %>%
  select(-identifier_var)%>%
  names() %>%
  str_replace_all(pattern = "__", replacement = "_") %>%
  str_replace_all(pattern = "_", replacement = " ")
names(df_main) <- c(identifier_var, non_indentifier)

# Re-order columns
df_main <- df_main %>%
  select(all_of(identifier_var),
         starts_with('Age'),
         starts_with('Design'),
         starts_with('Eye tracking'),
         starts_with('Imaging structure'),
         starts_with('Imaging function'),
         starts_with('Task type'),
         starts_with('To be remembered information'),
         starts_with('Encoding instruction'),
         starts_with('Retrieval mode'),
         starts_with('Similarity Manipulation Encoding'),
         starts_with('Similarity Manipulation Retrieval'),
         starts_with('Cue manipulation'),
         starts_with('Stimuli'),
         starts_with('Modality'),
         starts_with('Repetition of encoding trials'),
         starts_with('Delay'))


writexl::write_xlsx(df_main, file.path(data_path, "Lit_Review_binarized.xlsx"))
