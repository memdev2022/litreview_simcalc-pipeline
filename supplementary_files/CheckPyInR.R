#Check if Python works:
CheckPy = function(){
  tryCatch(
    expr = {
      py_run_file(file.path(funcon_path, 'checkPyVer.py'))
    },
    error = function(e){
      warning('Python not working via reticulate or wrong version (must be at least 3.). Uncomment line below and run to troubleshoot!')
      #print(e)
    }
  )
}
  