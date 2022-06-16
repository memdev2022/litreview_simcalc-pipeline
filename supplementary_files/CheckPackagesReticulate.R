#check the available packages:
library(reticulate)
py_run_string('print("Checking necessary python packages available for reticulate: \\n")')

#numpy
a = ''
if (py_module_available('numpy')){
  message('numpy available')
} else{
  while (a !='y' & a != 'n') {
    a = readline('numpy not available. Do you want to install numpy?(y/n)')
  }
  if(a == 'y'){
    py_install('numpy')
    } else{
      message('numpy not installed, please check on your own before continuing!')
    } 
}

#pandas
a = ''
if (py_module_available('pandas')){
  message('pandas available')
} else{
  while (a !='y' & a != 'n') {
    a = readline('pandas not available. Do you want to install pandas?(y/n)')
  }
  if(a == 'y'){
    py_install('pandas')
  } else{
    message('pandas not installed, please check on your own before continuing!')
  } 
}

#scipy
a = ''
if (py_module_available('scipy')){
  message('scipy available')
} else{
  while (a !='y' & a != 'n') {
    a = readline('scipy not available. Do you want to install scipy?(y/n)')
  }
  if(a == 'y'){
    py_install('scipy')
  } else{
    message('scipy not installed, please check on your own before continuing!')
  } 
}

#openpyxl
a = ''
if (py_module_available('openpyxl')){
  message('openpyxl available')
} else{
  while (a !='y' & a != 'n') {
    a = readline('openpyxl not available. Do you want to install openpyxl?(y/n)')
  }
  if(a == 'y'){
    py_install('openpyxl')
  } else{
    message('openpyxl not installed, please check on your own before continuing!')
  } 
}

rm(a)