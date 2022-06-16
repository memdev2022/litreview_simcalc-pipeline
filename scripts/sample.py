#sample script for getting correct working directory

import os
import sys
import time


print('current wd:\n',os.getcwd(), '\n')
sys.stdout.flush()

#we can revert to this if we need to at some point
if os.getcwd().endswith('simcalc-pipeline'):
    wd = os.getcwd()
else:
    import subprocess
    try:
        homedir_repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        os.chdir(homedir_repo[0:-1])
    except:
        print('\nWARNING: Directory not a git repository!\n')
    if os.getcwd().endswith('simcalc-pipeline'):
        wd = os.getcwd()
    else:
        error_str = '"'+os.getcwd()+'" is not home directory of repository. \nPlease make sure to be in root directory of the git repository ("/simcalc-pipeline").'
        raise NameError(error_str)

# elif len(sys.path[0]) == 0:
#     scriptdir = os.path.join(os.getcwd(), '')
#     os.chdir(os.path.join(scriptdir, '..'))
#     wd = os.getcwd()
# else:
#     scriptdir = os.path.join(sys.path[0], '')
#     os.chdir(os.path.join(scriptdir, '..'))
#     wd = os.getcwd()

#assigning filepath
filepath = os.path.join(wd, 'data_files', '')

print('filepath is: \n', filepath, '\n\n')
print('current wd is: \n', wd, '\n\n')
sys.stdout.flush()

time.sleep(0.5)
a = input("Procede?(y/n)")

print("input: ",a)


import subprocess
#subprocess.check_output(["git", "status"])
homedir_repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
#import colorama
#print(f'{colorama.Fore.GREEN}\nhomedir of repo is ', homedir_repo[1:-1], f'{colorama.Style.RESET_ALL}')
print('\nhomedir of repo is ', homedir_repo[1:-1])

os.chdir(homedir_repo[0:-1])
print(os.getcwd())

import os
os.chdir('scripts/')
os.getcwd()
import DimsOfInterest
DimsOfInterest.make_matrix(dims = ['age', 'tbri'])
