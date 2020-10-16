import os
import re
import sys
from collections import deque

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()

dir_name = sys.argv[1]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

history = deque()


def get_site_request(url):
    return requests.get(url)


def parsing(url):
    soup = BeautifulSoup(url, 'html.parser')
    content = ""
    for tag in soup.find_all(["p", re.compile("^h"), "a", "ul", "li", "ol"]):
        if tag.name == "a":
            content += Fore.BLUE + str(tag.string) + Style.RESET_ALL
        else:
            content += str(tag.string)
    return content


def save_site_content(content, url):
    history.append(url)
    with open(os.path.join(dir_name, url), "w") as f:
        f.write(content)


def go_site(site):
    address = site if site.startswith("https://") else f"https://{site}"
    site_request = get_site_request(address)
    parsed_content = parsing(site_request.content)
    save_site_content(parsed_content, site)
    print(parsed_content)


def go_back():
    history.pop()
    with open(os.path.join(dir_name, history.pop()), 'r') as f:
        print(f.read())


while True:
    command = input()
    if command == "exit":
        break
    if command == "back":
        go_back()
    elif "." in command:
        go_site(command)
    else:
        print("Error: Incorrect URL")
