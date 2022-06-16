## SPECIFYING FUNCTION ARGUMENTS:
specify_doi_args = function(){
#version
cat('Which version to use? (1=constrained, 2=unconstrained)')
v = readline('input here -->')
if (v == 1){
  v = 'constrained'
} else if (v == 2){
  v = 'unconstrained'
} else {
  message('No valid version chosen, reverting to default ("constrained")')
  v = 'constrained'
}

#type
cat('Which type to output? (1=similarity, 2=distance, 3=both)')
t = readline('input here -->')
if (t == 1){
  t = 'similarity'
} else if (t == 2){
  t = 'distance'
} else if (t == 3) {
  t = 'both'
} else {
  message('No valid type chosen, reverting to default ("similarity")')
  t = 'similarity'
}

#dimensions
numdim=''
while (str_length(numdim) == 0) {
  
  cat('\n___________________\nWhich dimensions do you want to include in your calculation? \n(seperate with comma like this: 1,2,3)\n
age = 1\ndesign = 2\neye tracking = 3\nstructural imaging = 4\nfunctional imaging = 5\ntask type = 6\nto be rememberd information = 7\nencoding instructions = 8\nretrieval mode = 9\nsimilarity manipulation encoding = 10\nsimilarity manipulation retrieval = 11\ncue manipulation = 12\nstimuli = 13\nmodality = 14\nrepetition of encoding trials = 15\ndelay = 16')
  numdim = readline('input here -->')
  if(str_length(numdim) == 0) {
    message('No valid dimensions supplied, please input again')
  } 
}
#redefine numdim and define vector of dims for input
dimvec= c('age', 'design', 'eyetrack', 'imstruc', 'imfunc', 'tasktype', 'tbri', 'enc', 'ret', 'simenc', 'simret', 'cuemanip', 'stim', 'mod', 'repenctrial', 'delay')
numdim = as.numeric(str_split(numdim, ',')[[1]])
if (length(numdim) != length(unique(numdim))){
  warning('some numbers inputed twice. If this was a mistake, please run the specification of arguments function again.')
}
d=character()
for (ndim in unique(numdim)){
  if (ndim > 0 & ndim < 17){
    d = c(d, dimvec[ndim])
  } else {
    warning(paste0('"',ndim,'" is not linked to any dimension and cannot be used to specify a dimension of interest. If this was a mistake, please run the specification of arguments function again.'))
  }
}
arguments = list('v' = v, 't' = t, 'd' = d)
return(arguments)
}