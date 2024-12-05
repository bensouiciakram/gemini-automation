import sys 
import json 
import subprocess
from pathlib import Path 
from typing import Optional
from playwright.sync_api import sync_playwright 


class GeminiBot:

    def __init__(self,executable:str,port:str):
        self.executable = executable 
        self.port = port 
        self.config = self.load_config()
        self.start_playwright_page() 

    def start_real_browser_instance(self):
        self.process = subprocess.Popen(
            [
                self.executable,
                f'--remote-debugging-port={self.port}'
            ]
        )

    def start_playwright_page(self):
        self.start_real_browser_instance()
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.connect_over_cdp(
            f"http://localhost:{self.port}"
        )
        self.context = self.browser.contexts[0]
        self.page = self.context.new_page()
        self.page.goto('https://gemini.google.com/')
    
    def search_text(self,prompt:str) -> str :
        self.page.fill('//rich-textarea//p',prompt)
        self.page.click('//button[contains(@class,"send-button")]')
        self.page.wait_for_selector('//message-actions')
        return self.page.query_selector_all('//message-content')[-1].inner_text()

    def search(self) -> str:
        upload_file = self.config['prompt']['file']
        self.upload(Path(upload_file)) if upload_file else None
        return self.search_text(self.config['prompt']['text'])

    def upload(self,file_path:Path):
        def activate_input_button():
            with self.page.expect_file_chooser() as fc_info:
                self.page.click('//button[@id="upload-local-image-button"]')

        activate_input_button()
        self.page.query_selector('//input[@name="Filedata"]')\
            .set_input_files(file_path) 
        
    def load_config(self) -> dict:
        return json.load(open('config.json','r'))
    
    def export(self,content:str):
        with open(Path(self.config['output_file']),'a') as file:
            file.write(content)
            file.write('\n\n#---------------------------------#\n\n')
        self.process.terminate()


if __name__ == '__main__':
    bot = GeminiBot(
        executable=sys.argv[1],
        port=sys.argv[2]
    )
    bot.export(bot.search())
