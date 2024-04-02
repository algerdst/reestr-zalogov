import time
import zipfile
import os
from time import sleep
from selenium import webdriver

PROXY_HOST = '94.103.188.163'
PROXY_PORT = 13804
PROXY_USER = 'umstvw'
PROXY_PASS = 'C8RBoM'


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""

background_js = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_driver(use_proxy=True):
    chrome_options=webdriver.ChromeOptions()
    path = os.path.dirname(os.path.abspath(__file__))

    prefs = {'download.default_directory': os.getcwd() + '\\pdfs', 'plugins.always_open_pdf_externally': True}
    chrome_options.add_experimental_option('prefs', prefs)
    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)

        chrome_options.add_extension(plugin_file)
    driver = webdriver.Chrome(
        options=chrome_options
    )
    return driver
