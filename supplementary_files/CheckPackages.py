"""
Checking if all necessary packages are available (still in progress, since R is not able to send the keyboard input to python)
"""
print("\nChecking if necessary python packages are available.\n")
a=''
try:
    import pip
    print('pip already installed, proceeding to checking installed packages...\n\n')
except:
    while a != 'y' and a != 'n':
        a = input("Pip not yet installed, Do you want to try to install pip? (y/n)")
    #a = input("Do you want to try to install pip? (y/n)")
    if a == 'y':
        import os
        ex_code = os.system("python -m ensurepip --default-pip")
        if ex_code == 0:
            print('pip successfally installed, proceeding to checking installed packages...\n\n')
        else:
            print("pip was not able to be installed. \nPlease get pip on your own or use preferred packge installer to get the necessary packages if not yet installed (numpy, pandas, scipy)\nand run this script again!")
    else:
        print("pip was not installed. \nPlease get pip on your own or use preferred packge installer to get the necessary packages if not yet installed (numpy, pandas, scipy)\nand run this script again!")

#numpy
a=''
try:
    import numpy
    print('numpy available')
except ImportError:
    while a != 'y' and a != 'n':
        a = input("Do you want to try to install numpy via pip? (y/n)")
    if a == 'y':
        try:
            pip.main(['install', '--user', 'numpy'])
            import numpy
            print('numpy downloaded and ready!')
        except:
            print('numpy not able to be installed via pip. Please do on your own before running calculation!')
    else:
        print("numpy not installed. Please do on your own before running calculation!")
except:
    print("Please download numpy before running calculation!")

#pandas
a=''
try:
    import pandas
    print('pandas available')
except ImportError:
    while a != 'y' and a != 'n':
        a = input("Do you want to try to install pandas via pip? (y/n)")
    if a == 'y':
        try:
            pip.main(['install', '--user', 'pandas'])
            import pandas
            print('pandas downloaded and ready!')
        except:
            print('pandas not able to be installed via pip. Please do on your own before running calculation!')
    else:
        print("pandas not installed. Please do on your own before running calculation!")
except:
    print("Please download pandas before running calculation!")

#scipy
a=''
try:
    import scipy
    print('scipy available')
except ImportError:
    while a != 'y' and a != 'n':
        a = input("Do you want to try to install scipy via pip? (y/n)")
    if a == 'y':
        try:
            pip.main(['install', '--user', 'scipy'])
            import scipy
            print('scipy downloaded and ready!')
        except:
            print('scipy not able to be installed via pip. Please do on your own before running calculation!')
    else:
        print("scipy not installed. Please do on your own before running calculation!")
except:
    print("Please download scipy before running calculation!")

#openpyxl
a=''
try:
    import openpyxl
    print('openpyxl available')
except ImportError:
    while a != 'y' and a != 'n':
        a = input("Do you want to try to install openpyxl via pip? (y/n)")
    if a == 'y':
        try:
            pip.main(['install', '--user', 'openpyxl'])
            import openpyxl
            print('openpyxl downloaded and ready!')
        except:
            print('openpyxl not able to be installed via pip. Please do on your own before running calculation!')
    else:
        print("openpyxl not installed. Please do on your own before running calculation!")
except:
    print("Please download openpyxl before running calculation!")
