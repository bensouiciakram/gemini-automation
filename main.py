import subprocess
from playwright.sync_api import sync_playwright 


class GeminiBot:

    def __init__(self,chrome_path:str,port:str):
        self.chrome_path = chrome_path 
        self.port = port 

    def start_real_browser_instance(self,type:str='chrome'):
        if type == 'chrome':
            self.process = subprocess.Popen(
                [
                    self.chrome_path,
                    f'--remote-debugging-port={self.port}'
                ]
            )

    def start_playwright_page(self,type:str='chrome'):
        self.start_real_browser_instance(type)
        playwright = sync_playwright().start()
        if type == 'chrome':
            self.browser = playwright.chromium.connect_over_cdp(f"http://localhost:{self.port}")
        else :
            self.browser = playwright.firefox.connect_over_cdp(f"http://localhost:{self.port}")
        self.context = self.browser.contexts[0]
        self.page = self.context.new_page()
        self.page.goto('https://gemini.google.com/')

    

    def search(self,prompt:str) -> str :
        self.page.fill('//rich-textarea//p',prompt)
        self.page.click('//button[contains(@class,"send-button")]')
        return self.page.query_selector_all('//message-content')[-1].inner_text()


if __name__ == '__main__':
    bot = GeminiBot(
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        port=9222
    )
    bot.start_playwright_page() 
    breakpoint()