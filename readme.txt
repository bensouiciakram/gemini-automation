I- Setting up the project : 
    1- make sure you have python installed in your system and it's added into your envirement variable path (you can check this by typing python in cmd and see if you have a python shell)
    2- install the requirements by double clicking install_requirements.bat file 
    3- run the script but double clicking run.bat 

II- Notes: 
    1- A demonstration demo video is included in the delivery compressed file.
    2- when running the script close all chrome instances 
    3- If chrome is not  installed in C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" correct this path with your correct path by modifying run.bat
        (just replace C:\\Program Files\\Google\\Chrome\\Application with the folder where you have chrome)
    4- You can use the script as command line tools by typing -->  python main.py "path_to_your_chrome_executable" port_value (choose and empty port like 9222) overloading_export_value (0 or 1) example : python main.py "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 9222 0
    5- Unfortunately we can only use chormium based browser (chrome,edge,brave ...etc) to connect over cdp (you can check the note here in documention : https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp)
    6- The export is being appended to the file so if you don't want this set the last value into 1 instead (python main.py "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 9222 1)