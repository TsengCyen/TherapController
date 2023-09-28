from config import *

#---------------------------------------------------------------|
#                   Therap Controller v1.0                      |
#---------------------------------------------------------------|
#       Company: BridgesMN                                      |
#---------------------------------------------------------------|
#       Development Lead - TsengCyen Yang                       |
#---------------------------------------------------------------|
#-----------------------------------------------------------|
#                   Table of Contents                       |
#-----------------------------------------------------------|
#   Can be used to CTRL+F to your desired location          |
#-----------------------------------------------------------|
#   Start Functions                                         |
#   Main Menu                                               |
#   Therap - Scheduler                                      |
#   Therap - Admin                                          |
#   Login Related                                           |
#   Alerts                                                  |
#   Set Global Variables                                    |
#   Closing Statements                                      |
#-----------------------------------------------------------|
#-----------------------------------------------------------|
#             Useful Variables from Config                  |
#-----------------------------------------------------------|
#   defaultLocation         - Install default location      |
#   companyLogo             - Image of Company Logo         |
#-----------------------------------------------------------|

#-----------------------------------------------------------|
#           Dummy Clients   (cProviderCode = 'DEMOIL-IL')   |
#-----------------------------------------------------------|
#       Matthew Jones                                       |
#       Mary Active                                         |
#                                                           |
#       Program - Demo Residential Program                  |
#       Service - Personal Support Services                 |
#-----------------------------------------------------------|
#In Demo Mode, login is overridden with the demo account automatically
#regardless of any input to the username and password fields
global demoMode
demoMode = True

#-----------------------------------------------------------|
#                                                           |
#       Start Functions                                     |
#                                                           |
#-----------------------------------------------------------|

#Global Variables
global windowSmall,loggedIn,checkInput,BGColor,cLogoColor,textColor,placeHText,errorText,noServiceColor,postLogin
global billable,verified,checkClient,checkClientP,checkClientS,checkClient
global doCheckOut,scoreOne,scoreTwo,scoreThree
global checkISPOneC,checkISPTwoC,checkISPThreeC,checkISPC,checkOutC,ispNotes

#Initialize Global Variables
windowSmall = 1
loggedIn = 0
checkInput = 0
BGColor = '#95c6ff'
cLogoColor = 'white'
topMenuColor = '#95c6ff'
textColor = 'black'
infoTextColor = '#94360b'
placeHText = 'grey'
errorText = 'red'
noServiceColor = 'darkgrey'
postLogin = 0
billable = 1
verified = 0
checkClient = 0
checkClientP = 0
checkClientS = 0
checkClientC = 0
doCheckOut = 0
scoreOne = 3
scoreTwo = 3
scoreThree = 3
checkISPOneC = 0
checkISPTwoC = 0
checkISPThreeC = 0
checkISPC = 0
checkOutC = 0
ispNotes = ['What type of tasks did you assist with during their work day?\n',
            'Description of the goal worked on, or what staff did to support the person\n',
            'Description of the incident and report. If no incident occured, indicate so in this box\n',
            'Other comments regarding the work day\n',
            'Any other comments - i.e. Reason for location discrepancy\n',
            '\n']
checkInPH = ['Client Name (Ex: Jane Doe)',
             'Client Region (Ex: Ramsey)',
             'Client Activity (Ex: Employment Services)',
             'Notes regarding anything check-in related (Ex: Discrepancy with location)\n']

#Closeout existing chromedriver sessions before opening new one
for process in (process for process in psutil.process_iter() if process.name()=="chromedriver.exe"):
    process.kill()

#Query and prepare TherapAPI
#- NO API TOKEN YET -

#Chrome Driver no CMD output + Chrome stays open when waiting for an action
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_service.creationflags = CREATE_NO_WINDOW
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
#chrome_options.add_argument("--headless") #Add Comment for Debugging
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=chrome_service,options=chrome_options)

#Create actions variable to allow inputting keys as is without direct element selection
#Example Code to place in-line below
actions = ActionChains(driver)

#Create Primary GUI
global win
win = Tk()
startProgram(win,demoMode)

#Window Position
global windowX,windowY
windowX = int(win.winfo_screenwidth()/2-320)
windowY = int(win.winfo_screenheight()/2-200)

#Make window not resizable and set background color
win.resizable(False,False)
win.configure(background=BGColor)

#---------------------------|
#   Photo Initializations   |
#---------------------------|
baseheight = 50
img = Image.open('logo.png')
hpercent = (baseheight / float(img.size[1]))
wsize = int((float(img.size[0]) * float(hpercent)))
img = img.resize((wsize, baseheight), Image.ANTIALIAS)
img.save('resized_logo.png')
cImage = PhotoImage(file='resized_logo.png')

#-----------------------------------------------------------|
#                                                           |
#       Main Menu                                           |
#                                                           |
#-----------------------------------------------------------|

#Primary GUI where the user decides what they want to do
def guiMain(userFill,passFill):
    global loggedIn,checkInput,userLabel,postLogin,windowX,windowY
    setVerifyF() #Reset Verification
    updateCursor(0) #Reset Cursor

    #Remeber window position
    windowX = win.winfo_x()
    windowY = win.winfo_y()
    
    #Clear and re-build GUI
    for child in win.winfo_children():
            child.destroy()

    #Check for Window Resizing
    if windowSmall == 0:
        win.geometry('{}x{}+{}+{}'.format(640,400,windowX,windowY))

    if loggedIn == 0:
        win.geometry('{}x{}+{}+{}'.format(320,400,int(win.winfo_screenwidth()/2-160),int(win.winfo_screenheight()/2-200)))
        
        #Image of Company Logo
        companyLogo = Label(win,image=cImage,bg=cLogoColor,width='320')
        companyLogo.place(x=0,y=0)
        
        #Login Elements
        userBox = Entry(win)
        passBox = Entry(win)
        userBox.place(x=95,y=280)
        passBox.place(x=95,y=310)

        if userFill == '' or passFill == '':
            userBox.configure(fg=placeHText)
            passBox.configure(fg=placeHText)
            userBox.insert(0,'Username')
            passBox.insert(0,'Password')
        else:
            passBox.configure(show="*")

        userBox.bind('<FocusIn>',lambda x:on_focus_in(userBox,False))
        userBox.bind('<FocusOut>',lambda x:on_focus_out(userBox,'Username',False))
        passBox.bind('<FocusIn>',lambda x:on_focus_in(passBox,True))
        passBox.bind('<FocusOut>',lambda x:on_focus_out(passBox,'Password',True))
        userBox.bind('<Return>',lambda x:checkLogin(userBox.get(),passBox.get()))
        passBox.bind('<Return>',lambda x:checkLogin(userBox.get(),passBox.get()))

        #Buttons user will see while NOT logged in
        bLogin = Button(win, text='Sign-In',
                    command=lambda: checkLogin(userBox.get(),passBox.get()),
                    width=20, bg=cLogoColor, fg=textColor)
        bLogin.place(x=85,y=350)
        bLogin.bind('<Enter>',lambda x:updateCursor(0))
        bLogin.bind('<Leave>',lambda x:updateCursor(1))

        #Allow the press of "Enter" to also proceed with logging in
        #passBox.bind('<Return>',lambda: checkLogin(userBox.get(),passBox.get()))

        versionLabel = Label(win,text=appVersion,font='times 8',bg=BGColor)
        versionLabel.place(x=1,y=383)
        
    if checkInput == 1:
        #Missing Input Warning and re-fill in existing information
        #Warning Pop-Up
        errorLabel = Label(win, text='Bad Input - Please Try Again', font='times 10 bold', fg=errorText, bg=BGColor)
        errorLabel.place(x=75,y=245)

        #Re-fill existing information
        userBox.insert(END,userFill)
        passBox.insert(END,passFill)

    #-----------------------|
    #   Main Menu Content   |
    #-----------------------|
        
    if loggedIn == 1:
        #Make sure we are on the homepage
        driver.get('https://secure.therapservices.net/ma/newfpage/worklist')
        
        #Application Label
        companyLogo = Label(win,image=cImage,bg=cLogoColor,width='640',height='50')
        companyLogo.place(x=0,y=0)

        #User Label
        user = driver.find_element(By.XPATH,'//div[@class="loginName"]').text
        userLabel = Label(win,text=user,bg=cLogoColor,fg=textColor)
        userLabel.place(x=640-(len(user)*6.5),y=30)

        #Login Button
        mmBack = Button(win, text='× Logout',
                    command=logout,
                    width=8,bg=BGColor,fg=textColor)
        mmBack.place(x=10,y=15)

        #Check if client is already checked in and pass name through and check for bad entries

        #When multiple users are checked in they are created
        #in a way that using the xpath + [number] should be
        #able to differ between them. Thus, we need to create an
        #array containing ALL checked in clients and then allow
        #the user to click and determine which one to check out.

        #While loop to check for all Logged in Users
        
        try:
            driver.get('https://secure.therapservices.net/ma/schedule/staff')
            time.sleep(1) #Load Buffer
            client = driver.find_element(By.XPATH, "//div[@class='dhx_cal_event_line incomplete_event']").text

            #Reset to home page
            time.sleep(0.25) #Load Buffer
            driver.get('https://secure.therapservices.net/ma/newfpage/worklist')
        except:
            client = 'NoClient' #Do Nothing

            #Reset to home page
            time.sleep(0.25) #Load Buffer
            driver.get('https://secure.therapservices.net/ma/newfpage/worklist')

        #-----------------|
        #Main Menu Options|
        #-----------------|

        #Dummy Client for Debug
        #Comment out if client is actually logged in
            
        #Check-In
        mmCheckIn = Button(win, text='Check-In',
                        command=lambda: guiCheckIn('','','',''),
                        width=12, bg=cLogoColor, fg=textColor)
        mmCheckIn.place(x=25,y=75)

        #Check-Out
        if client != 'NoClient':
            mmCheckOut = Button(win, text='Check-Out',
                            command=lambda: guiCheckOut(client,'','','','',''),
                            width=12, bg=cLogoColor, fg=textColor)
            mmCheckOut.place(x=25,y=115)
        else:
            mmCheckOut = Button(win, text='Check-Out',
                            command=alertNoClientCheckOut,
                            width=12, bg=noServiceColor, fg=textColor)
            mmCheckOut.place(x=25,y=115)

    updateCursor(1)

#-----------------------------------------------------------|
#                                                           |
#       Therap - Scheduler                                  |
#                                                           |
#-----------------------------------------------------------|

#Primary CheckIn Function
def guiCheckIn(clientFill,clientPFill,clientSFill,clientCFill):
    updateCursor(0)
    
    #Clear and re-build GUI
    for child in win.winfo_children():
            child.destroy()

    #Application Label
    companyLogo = Label(win,image=cImage,bg=cLogoColor,width='640',height='50')
    companyLogo.place(x=0,y=0)

    #Application Label and to Main Menu
    title = Label(win, text='Therap Check-In', font='times 18 bold', bg=cLogoColor, fg=textColor)
    title.place(x=425,y=9)

    mmBack = Button(win, text='◄ Back',
                    command=lambda:guiMain('',''),
                    width=8, bg=BGColor, fg=textColor)
    mmBack.place(x=10,y=15)
    mmBack.bind('<Enter>',lambda x:updateCursor(0))
    mmBack.bind('<Leave>',lambda x:updateCursor(1))

    #Separate Sections with "bars"
    divH = Frame(win, height=5, width=640)
    divH.place(x=0,y=50)

    #Client Section
    clientLabel = Label(win, text='Client Full Name', bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=55)
    clientBox = Entry(win)
    clientBox.place(x=2,y=75,width=260)

    if clientFill == '':
        clientBox.configure(fg=placeHText)
        clientBox.insert(0,'Client Name (Ex: Jane Doe)')

    clientBox.bind('<FocusIn>',lambda x:on_focus_in(clientBox,False))
    clientBox.bind('<FocusOut>',lambda x:on_focus_out(clientBox,'Client Name (Ex: Jane Doe)',False))

    #Client Program Section
    clientLabel = Label(win, text='Client Program', bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=100)
    clientPBox = Entry(win)
    clientPBox.place(x=2,y=120,width=260)

    if clientPFill == '':
        clientPBox.configure(fg=placeHText)
        clientPBox.insert(0,'Client Region (Ex: Ramsey)')

    clientPBox.bind('<FocusIn>',lambda x:on_focus_in(clientPBox,False))
    clientPBox.bind('<FocusOut>',lambda x:on_focus_out(clientPBox,'Client Region (Ex: Ramsey)',False))

    #Client Service Section
    clientLabel = Label(win, text='Client Service', bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=145)
    clientSBox = Entry(win)
    clientSBox.place(x=2,y=165,width=260)

    if clientSFill == '':
        clientSBox.configure(fg=placeHText)
        clientSBox.insert(0,'Client Activity (Ex: Employment Services)')

    clientSBox.bind('<FocusIn>',lambda x:on_focus_in(clientSBox,False))
    clientSBox.bind('<FocusOut>',lambda x:on_focus_out(clientSBox,'Client Activity (Ex: Employment Support)',False))

    #Confirm Billable Service
    clientLabel = Label(win, text='Billable:', bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=190)
    billOptionT = Radiobutton(win, text='Yes', variable=billable, value=1, bg=BGColor, fg=textColor,
                              activebackground=BGColor, command=setBillableT)
    billOptionF = Radiobutton(win, text='No', variable=billable, value=0, bg=BGColor, fg=textColor,
                              activebackground=BGColor, command=setBillableF)
    billOptionT.place(x=44,y=190)
    billOptionF.place(x=85,y=190)

    #Select default selection (Same as Therap)
    if billable == 1:
        billOptionT.select()
    else:
        billOptionF.select()

    #Client Check-In Comments
    clientLabel = Label(win, text='Check-In Comments', bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=215)
    clientCBox = Text(win,wrap=WORD)
    clientCBox.place(x=2,y=238,width=313,height=118)

    if clientCFill == '':
        clientCBox.configure(fg=placeHText)
        clientCBox.insert('1.0','Notes regarding anything check-in related (Ex: Discrepancy with location)')

    clientCBox.bind('<FocusIn>',lambda x:on_focus_in(clientCBox,False))
    clientCBox.bind('<FocusOut>',lambda x:on_focus_out(clientCBox,'Notes regarding anything check-in related (Ex: Discrepancy with location)',False))

    #Update any existing information
    clientBox.insert(0,clientFill)
    clientPBox.insert(0,clientPFill)
    clientSBox.insert(0,clientSFill)
    clientCBox.insert('1.0',clientCFill)

    #Check if Client Verification passes to submit information
    if verified == 1:
        bCheckIn = Button(win, text='Check-In',
                    command=lambda:checkIn(clientBox.get()),
                    width=12, bg=cLogoColor, fg=textColor)
        bCheckIn.place(x=275,y=365)
        bCheckIn.bind('<Enter>',lambda x:updateCursor(0))
        bCheckIn.bind('<Leave>',lambda x:updateCursor(1))
        
    else:
        #Verify the Client information input by the User
        verifyClient = Button(win, text='Verify Client',
                                command=lambda: checkInVerify(clientBox.get(),clientPBox.get(),clientSBox.get(),billable,clientCBox.get('1.0','end')),
                                width=10,bg=cLogoColor, fg=textColor)
        verifyClient.place(x=280,y=65)
        verifyClient.bind('<Enter>',lambda x:updateCursor(0))
        verifyClient.bind('<Leave>',lambda x:updateCursor(1))

        #Label to inform user that verification must happen first
        verifyLabel = Label(win, text='Verify Client to Submit', font='times 12', fg=textColor, bg=BGColor)
        verifyLabel.place(x=250,y=365)
            
    #Check if Client exists
    if checkClient:
        verifyLabel = Label(win, text='No Matching Client', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=50,y=365)
            
    #Check if Client Program exists
    elif checkClientP:
        verifyLabel = Label(win, text='No Matching Program', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=48,y=365)

    #Check if Client Service exists
    elif checkClientS:
        verifyLabel = Label(win, text='No Matching Service', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=50,y=365)

    #Check if Comments for client exists
    elif checkClientC:
        verifyLabel = Label(win, text='Comment Required', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=55,y=365)

    updateCursor(1)

#Function to verify client information before submitting
def checkInVerify(client,clientProgram,clientService,isBillable,clientComments):
    updateCursor(0)
    
    #Add checks to allow us to edit and notify the user of bad input
    global checkClient,checkClientP,checkClientS,checkClientC
    checkClient = 0
    checkClientP = 0
    checkClientS = 0
    checkClientC = 0

    if client in checkInPH:
        client = ''
        checkClient = 1
    if clientProgram in checkInPH:
        clientProgram = ''
        checkClientP = 1
    if clientService in checkInPH:
        clientService = ''
        checkClientS = 1
    if clientComments in checkInPH:
        clientComments = ''
        checkClientC = 1
    
    #Make sure everything is filled out, else prompt user to try again
    if not client:
        checkClient = 1

    if not clientProgram:
        checkClientP = 1

    if not clientService:
        checkClientS = 1

    for s in clientComments:
        if s in ['a','e','i','o','u']:
            checkClientC = 0
            break
        else:
            checkClientC = 1

    #If missing or bad input, prompt user for new information
    if checkClient == 1 or checkClientP == 1 or checkClientS == 1 or checkClientC == 1:
        guiCheckIn(client,clientProgram,clientService,clientComments) #Update GUI with new information
        
    else:
        #Go to scheduler - Refreshed in case of retries
        driver.get('https://secure.therapservices.net/ma/newfpage/worklist')
        driver.get('https://secure.therapservices.net/ma/schedule/staff')
        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "createSelfCheckInEvent")))
        time.sleep(0.2) #Load Buffer
        driver.find_element(By.ID, 'createSelfCheckInEvent').click()

        #Wait for menu to pop up
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-id='client']")))
        time.sleep(0.1) #Load Buffer

        #Enter Client Check-In Information
        #Client Name
        driver.find_element(By.XPATH, "//button[@data-id='client']").click()
        actions.send_keys(client + Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(0.1) #Buffer
        actions.send_keys(Keys.ENTER)
        actions.perform()
        checkClient = 0
        time.sleep(0.1) #Buffer
        if '- Please Select -' in driver.find_element(By.XPATH,"//button[@data-id='client']").text:
            #Perform action to deselect any inputs
            actions.send_keys(Keys.TAB)
            actions.perform()

            checkClient = 1

        time.sleep(0.1) #Load Buffer
                
        #Client Program
        driver.find_element(By.XPATH, "//button[@data-id='program']").click()
        actions.send_keys(clientProgram + Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(0.1) #Buffer
        actions.send_keys(Keys.ENTER)
        actions.perform()
        checkClientP = 0
        time.sleep(0.1) #Buffer
        if '- Please Select -' in driver.find_element(By.XPATH,"//button[@data-id='program']").text:
            #Perform action to deselect any inputs
            actions.send_keys(Keys.TAB)
            actions.perform()

            checkClientP = 1

        time.sleep(0.1) #Load Buffer
            
        #Client Service
        driver.find_element(By.XPATH, "//button[@data-id='service1']").click()
        actions.send_keys(clientService + Keys.ARROW_DOWN)
        actions.perform()
        time.sleep(0.1) #Buffer
        actions.send_keys(Keys.ENTER)
        actions.perform()
        checkClienS = 0
        time.sleep(0.1) #Buffer
        if '- Please Select -' in driver.find_element(By.XPATH,"//button[@data-id='service1']").text:
            #Perform action to deselect any inputs
            actions.send_keys(Keys.TAB)
            actions.perform()

            checkClientS = 1

        time.sleep(0.1) #Load Buffer

        #Set Billable
        if billable == 1:
            driver.find_element(By.XPATH,"//input[@value='true']").click()
        else:
            driver.find_element(By.XPATH,"//input[@value='false']").click()
        
        time.sleep(0.1) #Load Buffer

        #Client Comments
        driver.find_element(By.XPATH, "//textarea[@id='checkInComment']").send_keys(clientComments)
        actions.send_keys(Keys.BACKSPACE) #To remove extra line created after entry
        actions.perform()

        Nclient = str(driver.find_element(By.XPATH, "//button[@data-id='client']").get_attribute('title'))
        NclientP = str(driver.find_element(By.XPATH, "//button[@data-id='program']").get_attribute('title'))
        NclientS = str(driver.find_element(By.XPATH, "//button[@data-id='service1']").get_attribute('title'))

        #Reset variables is failed
        if '- Please Select -' in Nclient:
            Nclient = client
        if '- Please Select -' in NclientP:
            NclientP = clientProgram
        if '- Please Select -' in NclientS:
            NclientS = clientService
        
        #Check if all inputs are good - Set Verification to true to allow submissions
        if checkClient == 0 and checkClientP == 0 and checkClientS == 0 and checkClientC == 0:
            setVerifyT()

        guiCheckIn(Nclient,NclientP,NclientS,clientComments)

def checkIn(client):
    updateCursor(0)
    
    #Submit Check-In DO NOT USE UNLESS ON A TEST ACCOUNT OR PRACTICAL - To use, uncomment #Safety marked line
    try:
        driver.find_element(By.XPATH, "//input[@id='checkin']").click()
        time.sleep(0.2) #Load Buffer
        
        if not demoMode:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Confirm']")))
            time.sleep(0.2) #Load Buffer
            
            driver.find_element(By.XPATH,"//input[@value='Confirm']").click() #Safety

            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(0.1) #Load Buffer

        alertClientCheckedIn(client)
        
        setVerifyF()
        guiMain('','')
    except TimeoutError as error:
        messagebox.showerror("Check Out Error", "Something went wrong - Please try again or contact IT")
        raise('Something went wrong: ' + error)

def guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global checkISPOneC,checkISPTwoC,checkISPThreeC,checkISPC,checkOutC
    updateCursor(0)
    
    #Clear and re-build GUI
    for child in win.winfo_children():
            child.destroy()

    #Application Label
    companyLogo = Label(win,image=cImage,bg=cLogoColor,width='640',height='50')
    companyLogo.place(x=0,y=0)

    #Application Label and to Main Menu
    title = Label(win, text='Therap Check-Out', font='times 18 bold', bg=cLogoColor, fg=textColor)
    title.place(x=425,y=9)

    mmBack = Button(win, text='◄ Back',
                    command=lambda:guiMain('',''),
                    width=8, bg=BGColor, fg=textColor)
    mmBack.place(x=10,y=15)
    mmBack.bind('<Enter>',lambda x:updateCursor(0))
    mmBack.bind('<Leave>',lambda x:updateCursor(1))

    #Separate Sections with "bars"
    divH = Frame(win, height=5, width=640)
    divH.place(x=0,y=50)

    #Client Section
    clientLabel = Label(win, text=('Client: ' + client), bg=BGColor, fg=textColor)
    clientLabel.place(x=1,y=55)

    #ISP Task Questions Section
    #ISP One
    ispOneLabel = Label(win, text='Did you assist the individual during their work day?', bg=BGColor, fg=textColor)
    ispOneLabel.place(x=1,y=76)

    scoreLabelOne = Label(win, text='Score:', bg=BGColor, fg=textColor)
    scoreLabelOne.place(x=1,y=94)

    scoreOneT = Radiobutton(win, text='Yes', variable=scoreOne, value=1, bg=BGColor, fg=textColor,
                            activebackground=BGColor,command=lambda:setScoreOneT(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreOneF = Radiobutton(win, text='No', variable=scoreOne, value=2, bg=BGColor, fg=textColor,
                            activebackground=BGColor,command=lambda:setScoreOneF(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreOneNA = Radiobutton(win, text='N/A', variable=scoreOne, value=3, bg=BGColor, fg=textColor,
                             activebackground=BGColor,command=lambda:setScoreOneNA(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreOneT.place(x=45,y=94)
    scoreOneF.place(x=85,y=94)
    scoreOneNA.place(x=125,y=94)

    ispOneBox = Text(win,wrap=WORD)
    ispOneBox.place(x=2,y=114,width=300,height=55)

    if ispOneCFill == '':
        ispOneBox.configure(fg=placeHText)
        ispOneBox.insert('1.0','What type of tasks did you assist with during their work day?')

    ispOneBox.bind('<FocusIn>',lambda x:on_focus_in(ispOneBox,False))
    ispOneBox.bind('<FocusOut>',lambda x:on_focus_out(ispOneBox,'What type of tasks did you assist with during their work day?',False))

    #ISP Two
    ispTwoLabel = Label(win, text='Did the individual work on an outcome during this shift?', bg=BGColor, fg=textColor)
    ispTwoLabel.place(x=1,y=169)

    scoreLabelTwo = Label(win, text='Score:', bg=BGColor, fg=textColor)
    scoreLabelTwo.place(x=1,y=187)

    scoreTwoT = Radiobutton(win, text='Yes', variable=scoreTwo, value=1, bg=BGColor, fg=textColor,
                            activebackground=BGColor,command=lambda:setScoreTwoT(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreTwoF = Radiobutton(win, text='No', variable=scoreTwo, value=2, bg=BGColor, fg=textColor,
                            activebackground=BGColor,command=lambda:setScoreTwoF(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreTwoNA = Radiobutton(win, text='N/A', variable=scoreTwo, value=3, bg=BGColor, fg=textColor,
                             activebackground=BGColor,command=lambda:setScoreTwoNA(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreTwoT.place(x=45,y=187)
    scoreTwoF.place(x=85,y=187)
    scoreTwoNA.place(x=125,y=187)
    
    ispTwoBox = Text(win,wrap=WORD)
    ispTwoBox.place(x=2,y=207,width=300,height=55)

    if ispTwoCFill == '':
        ispTwoBox.configure(fg=placeHText)
        ispTwoBox.insert('1.0','Description of the goal worked on, or what staff did to support the person')

    ispTwoBox.bind('<FocusIn>',lambda x:on_focus_in(ispTwoBox,False))
    ispTwoBox.bind('<FocusOut>',lambda x:on_focus_out(ispTwoBox,'Description of the goal worked on, or what staff did to support the person',False))

    #ISP Three
    ispThreeLabel = Label(win, text='Were there any incidents that occurred on this shift?', bg=BGColor, fg=textColor)
    ispThreeLabel.place(x=1,y=262)

    scoreLabelThree = Label(win, text='Score:', bg=BGColor, fg=textColor)
    scoreLabelThree.place(x=1,y=280)

    scoreThreeT = Radiobutton(win, text='Yes', variable=scoreThree, value=1, bg=BGColor, fg=textColor,
                              activebackground=BGColor,command=lambda:setScoreThreeT(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreThreeF = Radiobutton(win, text='No', variable=scoreThree, value=2, bg=BGColor, fg=textColor,
                              activebackground=BGColor,command=lambda:setScoreThreeF(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreThreeNA = Radiobutton(win, text='N/A', variable=scoreThree, value=3, bg=BGColor, fg=textColor,
                               activebackground=BGColor,command=lambda:setScoreThreeNA(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),checkOutCBox.get('1.0','end')))
    scoreThreeT.place(x=45,y=280)
    scoreThreeF.place(x=85,y=280)
    scoreThreeNA.place(x=125,y=280)

    ispThreeBox = Text(win,wrap=WORD)
    ispThreeBox.place(x=2,y=300,width=300,height=55)

    if ispThreeCFill == '':
        ispThreeBox.configure(fg=placeHText)
        ispThreeBox.insert('1.0','Description of the incident and report. If no incident occured, indicate so in this box')

    ispThreeBox.bind('<FocusIn>',lambda x:on_focus_in(ispThreeBox,False))
    ispThreeBox.bind('<FocusOut>',lambda x:on_focus_out(ispThreeBox,'Description of the incident and report. If no incident occured, indicate so in this box',False))

    #Set Radio Selections
    if scoreOne == 1:
        scoreOneT.select()
    elif scoreOne == 2:
        scoreOneF.select()
    elif scoreOne == 3:
        scoreOneNA.select()

    if scoreTwo == 1:
        scoreTwoT.select()
    elif scoreTwo == 2:
        scoreTwoF.select()
    elif scoreTwo == 3:
        scoreTwoNA.select()

    if scoreThree == 1:
        scoreThreeT.select()
    elif scoreThree == 2:
        scoreThreeF.select()
    elif scoreThree == 3:
        scoreThreeNA.select()

    #Client ISP Task Comments
    ispCommentLabel = Label(win, text='ISP Task Comments', bg=BGColor, fg=textColor)
    ispCommentLabel.place(x=336,y=197)
    ispCommentBox = Text(win,wrap=WORD)
    ispCommentBox.place(x=337,y=220,width=300,height=55)

    if ispCommentFill == '':
         ispCommentBox.configure(fg=placeHText)
         ispCommentBox.insert('1.0','Other comments regarding the work day')

    ispCommentBox.bind('<FocusIn>',lambda x:on_focus_in(ispCommentBox,False))
    ispCommentBox.bind('<FocusOut>',lambda x:on_focus_out(ispCommentBox,'Other comments regarding the work day',False))

    #Client Check-In Comments
    checkOutCLabel = Label(win, text='Check-Out Comments', bg=BGColor, fg=textColor)
    checkOutCLabel.place(x=336,y=277)
    checkOutCBox = Text(win,wrap=WORD)
    checkOutCBox.place(x=337,y=300,width=300,height=55)

    if checkOutCFill == '':
        checkOutCBox.configure(fg=placeHText)
        checkOutCBox.insert('1.0','Any other comments - i.e. Reason for location discrepancy')

    checkOutCBox.bind('<FocusIn>',lambda x:on_focus_in(checkOutCBox,False))
    checkOutCBox.bind('<FocusOut>',lambda x:on_focus_out(checkOutCBox,'Any other comments - i.e. Reason for location discrepancy',False))

    #Update any existing information
    ispOneBox.insert('1.0',ispOneCFill)
    ispTwoBox.insert('1.0',ispTwoCFill)
    ispThreeBox.insert('1.0',ispThreeCFill)
    ispCommentBox.insert('1.0',ispCommentFill)
    checkOutCBox.insert('1.0',checkOutCFill)
    
    #User Notes
    notesLabel = Label(win,text='Select the N/A option ONLY if the\nclient was not present for work',bg=BGColor,fg=infoTextColor)
    notesLabel.place(x=405,y=73)

    #Check if Client Verification passes to submit information
    if verified == 1:
        bCheckOut = Button(win, text='Check-Out',
                    command=lambda:checkOut(client),
                    width=12, bg=cLogoColor, fg=textColor)
        bCheckOut.place(x=275,y=365)
        bCheckOut.bind('<Enter>',lambda x:updateCursor(0))
        bCheckOut.bind('<Leave>',lambda x:updateCursor(1))
    
    #Default Information for user
    else:
        #Verify the Client information input by the User
        verifyClient = Button(win, text='Confirm Data',
                                command=lambda: checkOutVerify(client,ispOneBox.get('1.0','end'),ispTwoBox.get('1.0','end'),
                                                               ispThreeBox.get('1.0','end'),ispCommentBox.get('1.0','end'),
                                                               checkOutCBox.get('1.0','end')),
                                width=10,bg=cLogoColor, fg=textColor)
        verifyClient.place(x=282,y=65)
        verifyClient.bind('<Enter>',lambda x:updateCursor(0))
        verifyClient.bind('<Leave>',lambda x:updateCursor(1))

        verifyLabel = Label(win, text='Confirm Data to Submit', font='times 12', fg=textColor, bg=BGColor)
        verifyLabel.place(x=248,y=365)
            
    #Check if ISP Task Comment exists
    if checkISPOneC:
        verifyLabel = Label(win, text='Check ISP Task 1', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=50,y=365)
            
    #Check if ISP Task Comment exists
    elif checkISPTwoC:
        verifyLabel = Label(win, text='Check ISP Task 2', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=50,y=365)

    #Check if ISP Task Comment exists
    elif checkISPThreeC:
        verifyLabel = Label(win, text='Check ISP Task 3', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=50,y=365)

    #Check if ISP Comment exists
    elif checkISPC:
        verifyLabel = Label(win, text='ISP Comment Required', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=40,y=365)

    #Check if ISP Comment exists
    elif checkOutC:
        verifyLabel = Label(win, text='Check Out Comment Required', font='times 12 bold', fg=errorText, bg=BGColor)
        verifyLabel.place(x=20,y=365)

    updateCursor(1)

def checkOutVerify(client,ispOneC,ispTwoC,ispThreeC,ispComment,checkOutComment):
    updateCursor(0)

    if ispOneC in ispNotes:
        ispOneC = ''
    if ispTwoC in ispNotes:
        ispTwoC = ''
    if ispThreeC in ispNotes:
        ispThreeC = ''
    if ispComment in ispNotes:
        ispComment = ''
    if checkOutComment in ispNotes:
        checkOutComment = ''
    
    #Check for bad input/missing input
    global checkISPOneC,checkISPTwoC,checkISPThreeC,checkISPC,checkOutC,driver
    checkISPOneC = 1
    checkISPTwoC = 1
    checkISPThreeC = 1
    checkISPC = 1
    checkOutC = 1

    for s in ispOneC:
        if s in ['a','e','i','o','u']:
            checkISPOneC = 0
            break
        else:
            checkISPOneC = 1
    for s in ispTwoC:
        if s in ['a','e','i','o','u']:
            checkISPTwoC = 0
            break
        else:
            checkISPTwoC = 1
    for s in ispThreeC:
        if s in ['a','e','i','o','u']:
            checkISPThreeC = 0
            break
        else:
            checkISPThreeC = 1
    for s in ispComment:
        if s in ['a','e','i','o','u']:
            checkISPC = 0
            break
        else:
            checkISPC = 1
    for s in checkOutComment:
        if s in ['a','e','i','o','u']:
            checkOutC = 0
            break
        else:
            checkOutC = 1

    #Check if all inputs are good - Set Verification to true to allow submissions
    if checkISPOneC == 1 or checkISPTwoC == 1 or checkISPThreeC == 1 or checkISPC == 1 or checkOutC == 1:
        guiCheckOut(client,ispOneC,ispTwoC,ispThreeC,ispComment,checkOutComment)

    else:
        #Go to scheduler - Refreshed in case of retries
        driver.get('https://secure.therapservices.net/ma/newfpage/worklist')
        driver.get('https://secure.therapservices.net/ma/schedule/staff')

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dhx_cal_event_line incomplete_event']")))
        time.sleep(0.1) #Load Buffer

        #Open current client service info
        actions.double_click(driver.find_element(By.XPATH, "//div[@class='dhx_cal_event_line incomplete_event']")).perform()

        #Select ISP Data for Service Button
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addIspDataForService1']")))
        time.sleep(0.1) #Load Buffer

        #Click on JavaScript Button for ISP Data
        jsElement = driver.find_element(By.XPATH, "//input[@id='addIspDataForService1']")
        driver.execute_script("arguments[0].click();", jsElement)
        time.sleep(0.1) #Load Buffer

        #Change driver focus to new tab
        existingDriver = driver
        primaryPage = driver.current_window_handle
        newPage = driver.window_handles

        for aPage in newPage:
            if aPage != primaryPage:
                driver.switch_to.window(aPage)

        time.sleep(0.1) #Load Buffer

        #ISP Task 1
        outSelection = driver.find_element(By.XPATH, "//select[@id='ispData.taskScores[0].score']")
        outSelection.click()
            
        for dummy in range(scoreOne):
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            time.sleep(0.1) #Buffer
                
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(0.1) #Buffer

        #ISP Task 1 - Comment
        outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.taskScores[0].comments']")
        outSelection.send_keys(ispOneC)
        time.sleep(0.1) #Buffer

        #ISP Task 2
        outSelection = driver.find_element(By.XPATH, "//select[@id='ispData.taskScores[1].score']")
        outSelection.click()
            
        for dummy in range(scoreTwo):
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            time.sleep(0.1) #Buffer
                
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(0.1) #Buffer

        #ISP Task 2 - Comment
        outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.taskScores[1].comments']")
        outSelection.send_keys(ispTwoC)
        time.sleep(0.1) #Buffer

        #ISP Task 3
        outSelection = driver.find_element(By.XPATH, "//select[@id='ispData.taskScores[2].score']")
        outSelection.click()
            
        for dummy in range(scoreThree):
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            time.sleep(0.1) #Buffer
                
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(0.1) #Buffer

        #ISP Task 3 - Comment
        outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.taskScores[2].comments']")
        outSelection.send_keys(ispThreeC)
        time.sleep(0.1) #Buffer

        if demoMode:
            #Demo Mode has extra tasks to fill
            #ISP Task 4
            outSelection = driver.find_element(By.XPATH, "//select[@id='ispData.taskScores[3].score']")
            outSelection.click()
                
            for dummy in range(2):
                actions.send_keys(Keys.ARROW_DOWN)
                actions.perform()
                time.sleep(0.1) #Buffer
                    
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(0.1) #Buffer

            #ISP Task 4 - Comment
            outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.taskScores[3].comments']")
            outSelection.send_keys('DummyInfo')
            time.sleep(0.1) #Buffer

            #ISP Task 5
            outSelection = driver.find_element(By.XPATH, "//select[@id='ispData.taskScores[4].score']")
            outSelection.click()
                
            for dummy in range(2):
                actions.send_keys(Keys.ARROW_DOWN)
                actions.perform()
                time.sleep(0.1) #Buffer
                    
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(0.1) #Buffer

            #ISP Task 5 - Comment
            outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.taskScores[4].comments']")
            outSelection.send_keys('DummyInfo')
            time.sleep(0.1) #Buffer
            

        #ISP Comment
        outSelection = driver.find_element(By.XPATH, "//textarea[@id='ispData.comments']")
        outSelection.send_keys(ispComment)
        time.sleep(0.1) #Buffer

        #Submit ISP
        try:
            driver.find_element(By.XPATH, "//input[@name='_action_save']").click()
        except:
            driver.find_element(By.XPATH, "//input[@name='_action_update']").click()

        time.sleep(0.25) #Load Buffer

        #Return to Main tab after Submiting ISP Data
        driver.close()
        driver.switch_to.window(primaryPage)

        #Check Out Comment
        outSelection = driver.find_element(By.XPATH, "//textarea[@id='checkOutComment']")
        outSelection.send_keys(checkOutComment)
        time.sleep(0.2) #Buffer

        if checkClient == 0 and checkClientP == 0 and checkClientS == 0 and checkClientC == 0:
            setVerifyT()

        guiCheckOut(client,ispOneC,ispTwoC,ispThreeC,ispComment,checkOutComment)

def checkOut(client):
    updateCursor(0)
    
    try:
        #Click on JavaScript Element
        jsElement = driver.find_element(By.XPATH,"//input[@id='checkout']")
        driver.execute_script("arguments[0].click();", jsElement)
        time.sleep(0.1) #Load Buffer

        if not demoMode:
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//input[@value='Confirm']")))
                time.sleep(0.2)
                
                driver.find_element(By.XPATH,"//input[@value='Confirm']").click #Safety

                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(0.1) #Load Buffer
                
            except:
                print('Failed to find')

        alertClientCheckedOut(client)

        setVerifyF()
        guiMain('','')
        #guiCheckOut('','','','','','')
    except:
        messagebox.showerror("Check Out Error", "Something went wrong - Please try again or contact IT")
        raise('Something went wrong')

#-----------------------------------------------------------|
#                                                           |
#       Therap - Admin                                      |
#                                                           |
#-----------------------------------------------------------|

def guiAdmin():
    print('')
    
#-----------------------------------------------------------|
#                                                           |
#       Login Related                                       |
#                                                           |
#-----------------------------------------------------------|

#Function to confirm required inputs
def checkLogin(username,password):
    global windowSmall,windowX,windowY
    updateCursor(0)
    
    if demoMode:
        #Forced Login Credentials
        username = 'demo8'
        password = 'welcome'
    
    if username != '' and password != '':
        #Perform Login
        driver.get('https://secure.therapservices.net/auth/login')

        #Input user's login information into Therap Login
        driver.find_element(By.ID, 'loginName').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        providerElement = driver.find_element(By.ID, 'providerCode')

        #In the case of a second login, the provider is automatically set so ignore it.
        if providerElement.get_attribute('value') == '':
            providerElement.send_keys(getCProviderCode())

        #Submit the login information
        driver.find_element(By.ID, 'submitButton').click()
        time.sleep(0.1) #Buffer

        #Verify if username and password are correct, otherwise, have user check input
        try:
            if driver.find_element(By.XPATH, '//*[@id="pageContent"]/div/b').text == 'Login Failed':
                setLoggedInF()
                setCheckInputT()

                if username == 'Username':
                    username = ''
                if password == 'Password':
                    password = ''
                    
                guiMain(username,password) #Update GUI with new information

        #In the case where the login is successful, there is no Login Failed page, so accept terms and conitnue
        except NoSuchElementException:
            driver.find_element(By.NAME, '_action_agree').click()

            #Get current window position
            windowX = win.winfo_x()
            windowY = win.winfo_y()

            windowSmall = 0
            setLoggedInT()
            setCheckInputF()
            guiMain('','') #Update GUI with new information
    else:  
        setLoggedInF()
        setCheckInputT()
        guiMain(username,password) #Update GUI with new information

#Function to log user out and save window properties
def logout():
    global windowSmall,postLogin
    driver.get('https://secure.therapservices.net/auth/logout')

    windowSmall = 1
    postLogin = 0
    setLoggedInF()
    setCheckInputF()
    guiMain('','') #Update GUI with new information

#-----------------------------------------------------------|
#                                                           |
#       Event Functions                                     |
#                                                           |
#-----------------------------------------------------------|

#Remove placeholder if user is making changes
def on_focus_in(entry,secure):
    if entry.cget('fg') == placeHText:
        entry.configure(fg=textColor)
        try:
            entry.delete('1.0','end')
        except:
            entry.delete(0,'end')

    if secure:
        entry.configure(show="*")

#Check if Place Holder is needed in the input
def on_focus_out(entry,placeholder,secure):
    try:
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.configure(fg=placeHText)
            
        #Specifially just for password login
        if secure and entry.get() != '':
            entry.configure(show="*")
        if secure and entry.get() == "Password":
            entry.configure(show="")
    except:
        if entry.get('1.0','end') == '\n':
            entry.insert('1.0',placeholder)
            entry.configure(fg=placeHText)

#Update Mouse Cursot
def updateCursor(update):
    if update == 0:
        win.configure(cursor="watch")
    else:
        win.configure(cursor="")

#-----------------------------------------------------------|
#                                                           |
#       Alerts                                              |
#                                                           |
#-----------------------------------------------------------|

def alertNoClientCheckOut():
    messagebox.showerror("No Existing Client", "You currently have no Client(s) to Check-Out")

def alertClientCheckedIn(client):
    messagebox.showinfo("Check-In Successful", client + " has been Checked-in!")

def alertClientCheckedOut(client):
    messagebox.showinfo("Check-Out Successful", client + " has been Checked-Out! You can now Verify with a signature using the Mobile App!")

#-----------------------------------------------------------|
#                                                           |
#       Set Global Variables                                |
#                                                           |
#-----------------------------------------------------------|

#Scheduler Variable Sets
def setBillableT():
    global billable
    billable = 1

def setBillableF():
    global billable
    billable = 0

def setVerifyT():
    global verified
    verified = 1

def setVerifyF():
    global verified
    verified = 0

def setLoggedInT():
    global loggedIn
    loggedIn = 1

def setLoggedInF():
    global loggedIn
    loggedIn = 0

def setCheckInputT():
    global checkInput
    checkInput = 1

def setCheckInputF():
    global checkInput
    checkInput = 0

def setCheckOutT():
    global doCheckOut
    doCheckOut = 1

def setCheckOutF():
    global doCheckOut
    doCheckOut = 0

def setCheckOutE():
    global doCheckOut
    doCheckOut = 2

def setScoreOneT(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreOne
    scoreOne = 1
    
    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
    
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreOneF(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreOne
    scoreOne = 2

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreOneNA(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreOne
    scoreOne = 3

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''

    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreTwoT(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreTwo
    scoreTwo = 1

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreTwoF(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreTwo
    scoreTwo = 2

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreTwoNA(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreTwo
    scoreTwo = 3

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreThreeT(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreThree
    scoreThree = 1

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreThreeF(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreThree
    scoreThree = 2

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)

def setScoreThreeNA(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill):
    global scoreThree
    scoreThree = 3

    if ispOneCFill in ispNotes:
        ispOneCFill = ''
    if ispTwoCFill in ispNotes:
        ispTwoCFill = ''
    if ispThreeCFill in ispNotes:
        ispThreeCFill = ''
    if ispCommentFill in ispNotes:
        ispCommentFill = ''
    if checkOutCFill in ispNotes:
        checkOutCFill = ''
        
    guiCheckOut(client,ispOneCFill,ispTwoCFill,ispThreeCFill,ispCommentFill,checkOutCFill)
    
#-----------------------------------------------------------|
#                                                           |
#       Closing Statements                                  |
#                                                           |
#-----------------------------------------------------------|

#Main Menu
guiMain('','')

#Closing Functions
win.mainloop()
driver.close()
