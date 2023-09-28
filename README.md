# TherapController
<h2><b>Introduction</b></h2>
This application will be used to control the functions of the Therap Web Service
Currently, there is no firm path that we're taking with this project since there are a TON of unknowns. The program is currently running on Python but could switch into Java or even Javascript + HTML/PHP. Only time will tell.

Currently there is not much planned for the project beyond trial and error and seeing what we can do, but more things will come as the project is developed further and further.

Ideas:

[✓] User Login w/ User + Password Verification</br>
[✓] Automated Client Inputs</br>
[✓] Dynamic Login/Logout</br>
[✓] Dynamic Client Inputs</br>
[] HR Role-Based User Creation</br>
[] HR Assign/Edit User Profile and Permissions</br>
[] Automated Check-In and Check-Out</br>
[] Save States (Questionable Feature)</br>
[] Dropdowns for Client Input</br>
[] Bypass Misc Pages on Login</br>
[] Finalize Check-In and Check-Out on non-Demo</br>
[] Admin VS User GUI Distinction</br>
[] App Auto Update Feature - Over Internet</br>
[] WhenIWork Integration</br>
...

<hr>

<h2><b>Initial Setup</b></h2>

1) Get the latest version of Python - <a href="https://www.python.org/downloads/" target="_blank">Download</a></br>
2) During installation, add Python to your PATH</br>
<img src="https://user-images.githubusercontent.com/95884459/145596270-ae3d8ffd-6559-42d9-97b5-739a07ec1b28.png" height="350px">
3) Open CMD and type "python" to make sure Python is installed correctly</br>
4) Download Github Desktop - <a href="https://central.github.com/deployments/desktop/desktop/latest/win32">Download</a></br>
5) Open Github Desktop and sign into your Github Account</br>
6) Link and download the existing TherapController repo to your device somewhere</br>
7) Open the "misc" folder and run "InstallPythonDependencies.bat" to install the required packages.</br>
8) To start editing, right-click 'TherapController.py' inside the repo, hover 'Edit with IDLE', then click 'Edit with IDLE 3.10 (64-bit)'</br>
9) To test the program within the IDLE editor, press F5 or in the top menus select Run < Run Module</br>
</br>

<hr>

<h2><b>Creating an EXE</b></h2>

Simply double click on the "Setup-EXE.bat" in order to create a new EXE file within ...\TherapController\build\exe.win-amd64-3.10 The EXE will be called TherapScheduler.exe

<hr>

<h2><b>Creating a Setup Install</b></h2>

1) Make sure an EXE is already created and functioning properly</br>
2) Download & Install Inno Setup - <a href="https://jrsoftware.org/isdl.php" target="_blank">Download</a></br>
3) Open the setup creation file found in ...\TherapController\misc\BuildUserSetup.iss</br>
4) In Inno Setup, Press F9 or using the top menu navigate to Run < Run</br>
5) The Setup will start working and should execute when it is finished, just close out of it or finish it to see if it operates as it should after being setup</br>
6) You will be able to find the transferable setup file inside your downloads folder called "TherapScheduler-Setup.exe"</br>
