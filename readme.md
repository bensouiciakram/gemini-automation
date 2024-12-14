# Project Setup and Usage Guide

## I. Setting Up the Project

1. **Ensure Python is installed**  
   Make sure Python is installed on your system and added to your environment variable path.  
   You can check this by typing `python` in the command prompt and verifying that a Python shell opens.

2. **Install the requirements**  
   Run the `install_requirements.bat` file by double-clicking it.

3. **Run the script**  
   Execute the `run.bat` file by double-clicking it.

---

## II. Notes

1. **Demo Video**  
   A demonstration video is included in the compressed delivery file.

2. **Close Chrome Instances**  
   Before running the script, make sure all Chrome instances are closed.

3. **Chrome Path Adjustment**  
   If Chrome is not installed in the default location (`C:\Program Files\Google\Chrome\Application\chrome.exe`), you need to update the `run.bat` file with the correct path.  
   Replace `C:\Program Files\Google\Chrome\Application` with the folder where Chrome is installed.

4. **Command-Line Usage**  
   You can use the script as a command-line tool with the following format:  
   ```bash
   python main.py "path_to_your_chrome_executable" port_value overloading_export_value
   ```
   Example :
   ```bash
   python main.py "C:\Program Files\Google\Chrome\Application\chrome.exe" 9222 0
   ```

5. **Chromium-Based Browsers Only**
The script only works with Chromium-based browsers (e.g., Chrome, Edge, Brave).
You can find more details in the Playwright documentation.

6. **Export Behavior**
   ```bash
   python main.py "C:\Program Files\Google\Chrome\Application\chrome.exe" 9222 1
   ```

## Update Notes (9/12/24)

* The empty tab for the first input file is intentionally left open.
This avoids cases where the close_tab command in the first input file might close all windows.
Opening a new Chrome instance using subprocess to handle this scenario could consume extra resources.
Thus, the behavior remains as is to optimize resource usage.
