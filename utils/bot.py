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
            ):
        self.executable = executable 
        self.port = port 
        self.overloading_export = int(overloading_export)
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
    
    def search_text(self,prompt:str,index:int) -> str :
        self.page.fill('//rich-textarea//p',prompt)
        self.page.click('//button[contains(@class,"send-button")]')
        # self.page.wait_for_selector('//message-actions')
        self.page.wait_for_selector(
            f'//div[contains(@class,"message-actions-hover-boundary") and position()={index+1}]'
        )
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(
            '//div[contains(@class,"message-actions-hover-boundary")'
            ' and position()=last()]//div[@data-test-lottie-animation-status="completed"]'
        )
        content = self.page.query_selector_all('//message-content')[-1].inner_text()
        return content

    def search(self,config_file:str) -> str:
        prompts_objs = json.load(open(config_file,'r'))
        content_list = []
        for index,prompt_obj in enumerate(prompts_objs) :
            self.upload(prompt_obj)
            content_list.append(self.search_text(prompt_obj['prompt']['text'],index))
        return '\n#---------------------------------------#\n'.join(content_list)

    def upload(self,prompt_obj:dict):
        def activate_input_button():
            with self.page.expect_file_chooser() as fc_info:
                self.page.click('//uploader')
                self.page.click(f'//button[@id="{"image" if prompt_obj["prompt"]["image"] else "file"}-uploader-local"]') \
                    if self.advanced else None  


        activate_input_button()
        if prompt_obj['prompt']['image'] :
            self.page.query_selector('//input[@name="Filedata"]')\
                .set_input_files(prompt_obj['prompt']['image'])
        elif prompt_obj['prompt']['files'] and self.advanced:
            self.page.query_selector('//input[@name="Filedata"]')\
                .set_input_files(prompt_obj['prompt']['files'])
        else :
            pass 
        
    def load_config(self) -> dict:
        return json.load(open('config.json','r',encoding='utf-8'))
    
    def free_up_playwright_resources(self):
        self.page.close()
        self.context.close()
        self.browser.close()
    
    def export(self,content:str,base_path:Path,input_file:str):
        output_path = base_path.joinpath(f'output_for_{Path(input_file).name.replace('.','_')}.txt')
        with open(Path(output_path),'a' if not self.overloading_export else 'w',encoding='utf-8') as file:
            file.write(content)
            file.write('\n\n#---------------------------------#\n\n')
        self.free_up_playwright_resources()
        self.process.terminate()

    def check_advanced(self):
        self.advanced = 'advanced' in self.page.query_selector(
            '//bard-mode-switcher'
        ).inner_text().lower()

#//div[@lottie-animation]
#//div[@data-test-lottie-animation-status="completed"]