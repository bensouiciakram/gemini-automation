import json 
import subprocess
from time import sleep 
from pathlib import Path 
from typing import Optional,Literal
from playwright.sync_api import sync_playwright 



class GeminiBot:

    def __init__(
            self,
            executable:str,
            port:str,
            overloading_export:Literal[0,1]=0,
            input_path:str=None,
            output_path:str=None):
        self.executable = executable 
        self.port = port 
        self.overloading_export = int(overloading_export)
        self.config = self.load_config()
        self.start_playwright_page() 

    def start_real_browser_instance(self):
        self.process = subprocess.Popen(
            [
                self.executable,
                f'--remote-debugging-port={self.port}'
            ]
        )
        sleep(2)

    def close_empty_tab(self):
        for context in self.browser.contexts:
            for page in context.pages:
                if not page.url or page.url == 'chrome://new-tab-page/':
                    page.close()

    def start_playwright_page(self):
        self.start_real_browser_instance()
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.connect_over_cdp(
            f"http://localhost:{self.port}"
        )
        self.close_empty_tab()
        self.context = self.browser.contexts[0]
        self.page = self.context.new_page()
        self.page.goto('https://gemini.google.com/')
        self.check_advanced()
    
    def search_text(self,prompt:str) -> str :
        self.page.fill('//rich-textarea//p',prompt)
        self.page.click('//button[contains(@class,"send-button")]')
        self.page.wait_for_selector('//message-actions')
        return self.page.query_selector_all('//message-content')[-1].inner_text()

    def search(self) -> str:
        self.upload()
        return self.search_text(self.config['prompt']['text'])

    def upload(self):
        def activate_input_button():
            with self.page.expect_file_chooser() as fc_info:
                self.page.click('//uploader')
                self.page.click(f'//button[@id="{"image" if self.config["prompt"]["image"] else "file"}-uploader-local"]') \
                    if self.advanced else None  


        activate_input_button()
        if self.config['prompt']['image'] :
            self.page.query_selector('//input[@name="Filedata"]')\
                .set_input_files(self.config['prompt']['image'])
        elif self.config['prompt']['files'] and self.advanced:
            self.page.query_selector('//input[@name="Filedata"]')\
                .set_input_files(self.config['prompt']['files'])
        else :
            pass 
        
    def load_config(self) -> dict:
        return json.load(open('config.json','r',encoding='utf-8'))
    
    def free_up_playwright_resources(self):
        self.page.close()
        self.context.close()
        self.browser.close()
    
    def export(self,content:str):
        with open(Path(self.config['output_file']),'a' if not self.overloading_export else 'w',encoding='utf-8') as file:
            file.write(content)
            file.write('\n\n#---------------------------------#\n\n')
        self.free_up_playwright_resources()
        self.process.terminate()

    def check_advanced(self):
        self.advanced = 'advanced' in self.page.query_selector(
            '//bard-mode-switcher'
        ).inner_text().lower()

