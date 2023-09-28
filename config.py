#---------------------------------------------------------------|
#                   Therap Controller v0.2                      |
#                                                               |
#       Company: BridgesMN                                      |
#                                                               |
#       Development Lead - TsengCyen Yang                       |
#---------------------------------------------------------------|

#-----------------------------------------------------------|
#                       Config                              |
#-----------------------------------------------------------|
#   Used to hide away other initialization code and other   |
#   commonly used Functions.                                |
#-----------------------------------------------------------|

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW

import requests #API Manipulator https://www.nylas.com/blog/use-python-requests-module-rest-apis/
import os,time,psutil,re,ctypes.wintypes,pickle

from tkinter import *
from tkinter import messagebox

from PIL import Image,ImageTk

#General
appVersion = 'v1.0'

#Set user install location
CSIDL_PERSONAL = 5
SHGFP_TYPE_CURRENT = 0
installDoc = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, installDoc)
defaultLocation = installDoc.value + "\\TherapController\\"

#Set user configuration file
global configFile,therap_vars,cProviderCode
configFile = "config.pkl"

def startProgram(win,demoMode):
    global therap_vars,cProviderCode

    #Set Company (Provided by Therap)
    if not demoMode:
        cProviderCode = 'BRIDGES-MN'
    elif demoMode:
        cProviderCode = 'DEMOIL-IL'

    #GUI Initialization
    win.title('BridgesMN - Therap')
    win.iconbitmap('App-Icon.ico')
    
    #Verify install path exists, otherwise create it
    if os.path.isdir(defaultLocation):
        dummy = 'x' #Do nothing
    else:
        os.makedirs(defaultLocation, exist_ok=True)
    
    #Check for pre-existing config settings written to a file
    if os.path.isfile(defaultLocation + configFile):
        with open(defaultLocation + configFile, 'rb') as conf:
            therap_vars = pickle.load(conf)

            if therap_vars['windowPos'] == '640x400+<bound method Misc.winfo_x of <tkinter.Tk object .>>+<bound method Misc.winfo_y of <tkinter.Tk object .>>':
                win.geometry('{}x{}+{}+{}'.format(640,400,int(win.winfo_screenwidth()/2-320),int(win.winfo_screenheight()/2-200)))
            else:
                win.geometry(therap_vars['windowPos'])
                
    #Create a new config file with default values
    else:
        #Initialize Save Data
        therap_vars = {
            'windowPos':'{}x{}+{}+{}'.format(640,400,int(win.winfo_screenwidth()/2-320),int(win.winfo_screenheight()/2-200))
            }

        #Set default window
        win.geometry('{}x{}+{}+{}'.format(640,400,int(win.winfo_screenwidth()/2-320),int(win.winfo_screenheight()/2-200)))

def getCProviderCode():
    return cProviderCode
