import os
import sys
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def get_platform():
    platforms = {
        'Windows' : 'Windows',
        'Linux' : 'Linux',
        'win32' : 'Windows',
        'linux' : 'Linux'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

browser = ""
firefox_driver = ""
user_agent = ""

if get_platform() == "Windows":
    firefox_driver = os.path.join(os.getcwd(), "Driver", "Windows", "geckodriver_firefox.exe")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
elif get_platform() == "Linux":
    firefox_driver = os.path.join(os.getcwd(), "Driver", "Linux", "geckodriver_firefox")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'


firefox_service = Service(firefox_driver)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)

def get_browser():
    browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
    return browser
