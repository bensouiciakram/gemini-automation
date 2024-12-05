import subprocess
from pathlib import Path 
from playwright.sync_api import sync_playwright 


class GeminiBot:

    def __init__(self,executable:str,port:str):
        self.executable = executable 
        self.port = port 

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
        self.browser = playwright.chromium.connect_over_cdp(f"http://localhost:{self.port}")
        self.context = self.browser.contexts[0]
        self.page = self.context.new_page()
        self.page.goto('https://gemini.google.com/')
        self.upload(Path(__file__).parent.joinpath('test.jpeg'))
        breakpoint()
        content = self.search('give me the textual content of the uploaded image')
        breakpoint()

    
    def search(self,prompt:str) -> str :
        self.page.fill('//rich-textarea//p',prompt)
        self.page.click('//button[contains(@class,"send-button")]')
        self.page.wait_for_selector('//message-content')
        return self.page.query_selector_all('//message-content')[-1].inner_text()
    

    def upload(self,file_path:Path):
        def activate_input_button():
            with self.page.expect_file_chooser() as fc_info:
                self.page.click('//button[@id="upload-local-image-button"]')

        activate_input_button()
        self.page.query_selector('//input[@name="Filedata"]')\
            .set_input_files(file_path) 

if __name__ == '__main__':
    bot = GeminiBot(
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        port=9222
    )
    bot.start_playwright_page() 
    breakpoint()