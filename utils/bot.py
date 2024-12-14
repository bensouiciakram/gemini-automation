import json 
import subprocess
from time import sleep 
from pathlib import Path 
from typing import Optional,Literal,Tuple
from playwright.sync_api import sync_playwright 
from playwright.sync_api._generated import Page
from .exceptions import CloseWindowException

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
        self.pages = {}

    def start_real_browser_instance(self):
        self.process = subprocess.Popen(
            [
                self.executable,
                f'--remote-debugging-port={self.port}',
                '--headless'
            ]
        )
        sleep(2)

    def close_empty_tab(self):
        for context in self.browser.contexts:
            for page in context.pages:
                if not page.url or page.url == 'chrome://new-tab-page/':
                    page.close() if self.check_pages_count() else None 

    def check_pages_count(self):
        pages = [
            page 
            for context in self.browser.contexts
            for page in context.pages    
        ]
        return len(pages) > 1

    def get_new_page(self,config_file:str) :
        self.pages[config_file] = {
            'page':self.context.new_page()
        }
        self.pages[config_file]['page'].goto('https://gemini.google.com/') 
        self.pages[config_file]['advanced'] = self.check_advanced(config_file)

    def start_playwright_page(self):
        self.start_real_browser_instance()
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.connect_over_cdp(
            f"http://localhost:{self.port}",
            slow_mo=100
        )
        self.context = self.browser.contexts[0]
    
    def search_text(self,prompt:str,index:int,config_file:str) -> str :
        page = self.pages[config_file]['page']
        page.fill('//rich-textarea//p',prompt)
        page.click('//button[contains(@class,"send-button")]')
        # page.wait_for_selector('//message-actions')
        page.wait_for_selector(
            f'//div[contains(@class,"message-actions-hover-boundary") and position()={index+1}]'
        )
        page.wait_for_timeout(1000)
        page.wait_for_selector(
            '//div[contains(@class,"message-actions-hover-boundary")'
            ' and position()=last()]//div[@data-test-lottie-animation-status="completed"]'
        )
        content = page.query_selector_all('//message-content')[-1].inner_text()
        return content

    def search(self,config_file:str) -> str:
        prompts_objs = json.load(open(config_file,'r'))
        self.close_empty_tab()
        self.get_new_page(config_file)
        content_list = []
        for index,prompt_obj in enumerate(prompts_objs) :
            if prompt_obj['prompt']['text'] in ('close_tab','close_window'):
                self.pages[config_file]['page'].close()
                break
            self.upload(prompt_obj,config_file) if self.check_update(prompt_obj) else None
            content_list.append(self.search_text(prompt_obj['prompt']['text'],index,config_file))
        return '\n#---------------------------------------#\n'.join(content_list)

    def check_update(self,prompt_obj:dict) -> bool:
        return prompt_obj['prompt']['image'] or prompt_obj['prompt']['files']

    def upload(self,prompt_obj:dict,config_file:str):
        page = self.pages[config_file]['page']
        advanced = self.pages[config_file]['advanced']
        def activate_input_button():
            with page.expect_file_chooser() as fc_info:
                page.click('//uploader')
                page.click(f'//button[@id="{"image" if prompt_obj["prompt"]["image"] else "file"}-uploader-local"]') \
                    if advanced else None  

        activate_input_button()
        if prompt_obj['prompt']['image'] :
            page.query_selector('//input[@name="Filedata"]')\
                .set_input_files(prompt_obj['prompt']['image'])
        elif prompt_obj['prompt']['files'] and advanced:
            page.query_selector('//input[@name="Filedata"  and @multiple ]')\
                .set_input_files(prompt_obj['prompt']['files'])
        else :
            pass 
        
    def load_config(self) -> dict:
        return json.load(open('config.json','r',encoding='utf-8'))
    
    def close_config_page(self,config_file:str):
        self.pages[config_file].close()

    def close_all_tabs(self):
        [
            page.close() 
            for context in self.browser.contexts
            for page in context.pages
        ]
        self.context.close()

    def export(self,content:str,base_path:Path,input_file:str):
        output_path = base_path.joinpath(f'output_for_{Path(input_file).name.replace('.','_')}.txt')
        with open(Path(output_path),'a' if not self.overloading_export else 'w',encoding='utf-8') as file:
            file.write(content)
            file.write('\n\n#---------------------------------#\n\n')

    def check_advanced(self,config_file:str):
        return 'advanced' in self.pages[config_file]['page'].query_selector(
            '//bard-mode-switcher'
        ).inner_text().lower()
    
    def check_close_window(self,config_file:str):
        last_prompt_obj = json.load(open(config_file,'r'))[-1]
        if last_prompt_obj['prompt']['text'] == 'close_window':
            self.close_all_tabs()
            raise CloseWindowException
