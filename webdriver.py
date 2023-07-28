import json

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib import request
from subprocess import CREATE_NO_WINDOW

import asyncio
import glob

service = ChromeService(ChromeDriverManager().install())
service.creationflags = CREATE_NO_WINDOW

AUTO_TRANSLATE = False


def add_cookies(driver, _cookies):
    for ck in _cookies:
        driver.add_cookie(ck)


def get_cookies_from_json(filename, allowed=None, exceptions=()):
    _cookies = json.load(open(filename, "r"))

    cookies = [{"name": el["name"], "value": el["value"]} for el in _cookies if el["name"] not in exceptions]
    if allowed:
        cookies = [e for e in cookies if e["name"] in allowed]
    return cookies


def login_driver(main_url, url=None, cookies=None):
    driver = webdriver.Chrome(service=service)
    driver.get(main_url)
    if cookies:
        add_cookies(driver, cookies)
        sleep(1)
        driver.get(url, )
    sleep(1)
    return driver


def get_filename(path):
    return path.replace("\\", "/").rsplit("/", 1)[1]


def format_num(st):
    return str(float(st)).rstrip("0").rstrip(".")


clear_js_script = """
var elements = document.getElementsByTagName("input");
for (var ii=0; ii < elements.length; ii++) {
  if (elements[ii].type == "text") {
    elements[ii].value = "";
  }
}
"""
