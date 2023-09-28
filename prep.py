from cx_Freeze import setup, Executable
import sys,os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Python\\Python310\\"))
os.environ['TCL_LIB'] = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl8.6')
os.environ['TK_LIB'] = os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk8.6')
base = None

if sys.platform == 'win32':
    base = "Win32GUI"
    
executables = [Executable("TherapController.py", base=base, icon="App-Icon.ico")]
  
setup(name = "Therap Scheduler" ,
      options = {"build_exe": {"packages":["tkinter","selenium","psutil","os","time","requests","re",
                                           "webdriver_manager.chrome","subprocess","pickle","PIL"],
            "include_files":["App-Icon.ico","logo.png",
            os.path.join(PYTHON_INSTALL_DIR,'DLLs','tcl86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR,'DLLs','tk86t.dll')]}},
      version = "1.0" ,
      description = "This application will be used to control the functions of the Therap Web Service" ,
      executables = executables)
