#Troubleshooting if reticulate does not find correct python version
message('Trying to solve by restarting and initializing other python version if available!\n\n')
if(.Platform$OS.type == 'windows'){
  py_vw = py_versions_windows()
  max_py = max(as.numeric(py_vw$version))
  path_2py = py_vw$executable_path[py_vw$version == max_py & py_vw$version >= 3]
  rm(py_vw, max_py)
  if(length(path_2py) == 1){
    use_python(path_2py)
  } else if (length(path_2py) > 1){
    use_python(path_2py[1]) #using top search result
  } else {
    stop('No adequate python version found on system! Please download python from https://www.python.org/ or using the reticulate package before continuing!')
  }
} else {
  path_2py = try(system('which python3', intern = T), silent = TRUE)
  if(class(path_2py) == "try-error"){
    path_2py = try(system('which python', intern = T), silent = TRUE)
    if(class(path_2py) == "try-error"){
      stop('python not found on system. Please download python from https://www.python.org/ or using the reticulate package before continuing!')
    }
  }
  use_python(path_2py)
}
py_run_file(file.path(funcon_path, 'checkPyVer.py'))