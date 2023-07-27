import os
import sys
url="https://www.zscaler.com"

if not os.getenv("webbrowser"):
    web_browser="firefox"
    #sys.exit("Please define web browser chrome or firefox.")
else:
    web_browser = os.getenv("webbrowser")

if not os.getenv("headless"):
    headless="false"
    #sys.exit("Please define headless true or false.")
else:
    headless = os.getenv("headless")
