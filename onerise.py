#!/usr/bin/env python3
# coded by vbiskit 

import aiohttp
import re
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import os
from colorama import Fore
from urllib.parse import urlparse, parse_qs
import sys
import argparse
import asyncio
import io

def fetch_metadata():
    url = "https://raw.githubusercontent.com/vbiskit/oneRise/refs/heads/main/metadata.json"
    return requests.get(url).json()

metadata = fetch_metadata()

user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
    "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
    "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
    "Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
    "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)"
]

def rgb(r, g, b, text):
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

def blue_green(text):
    gradient_colors = [
        (0, 180, 255),  
        (0, 220, 220),  
        (0, 255, 180),  
        (0, 255, 120),  
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def blue2(text):
    gradient_colors = [
        (0, 0, 255),       
        (0, 102, 255),     
        (0, 191, 255),     
        (30, 144, 255),    
        (70, 130, 180),    
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def vibrant_yellow_green(text):
    gradient_colors = [
        (255, 255, 0),   
        (220, 255, 0),   
        (180, 255, 0),   
        (120, 255, 0),  
        (60, 255, 0),    
    ]

    gradient_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        color_index = int((i / text_length) * (len(gradient_colors) - 1))
        r, g, b = gradient_colors[color_index]
        gradient_text += rgb(r, g, b, char)

    return gradient_text

def get_random_user_agent():
    return random.choice(user_agents)

async def check_username_on_website(session, site, username):
    url = site["uri_check"].replace("{account}", username)
    headers = {"User-Agent": get_random_user_agent()}

    try:
        async with session.get(url, headers=headers, timeout=19.6) as response:
            raw_bytes = await response.read()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = raw_bytes.decode("latin-1")

            if response.status == site["e_code"] and site["e_string"] in text:
                print(f"\033[38;2;255;255;255m[\033[38;2;0;191;255m{site['name']}\033[38;2;255;255;255m] \033[38;2;255;255;255m[\033[38;2;0;255;0m{site['cat']}\033[38;2;255;255;255m] {Fore.LIGHTBLACK_EX}{url}")
                return (site["name"], url, site["cat"])

            if "m_code" in site and "m_string" in site:
                if response.status == site["m_code"] and site["m_string"] in text:
                    return None

            return None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None

async def check_username_with_retries(session, site, username, max_retries=1):
    for attempt in range(max_retries):
        result = await check_username_on_website(session, site, username)
        if result is not None:
            return result
        await asyncio.sleep(0.03)  
    return None

def print_banner():
    logo = r"""                                                                    
                      ,------. ,--.               
 ,---. ,--,--,  ,---. |  .--. '`--' ,---.  ,---.  
| .-. ||      \| .-. :|  '--'.',--.(  .-' | .-. : 
' '-' '|  ||  |\   --.|  |\  \ |  |.-'  `)\   --. 
 `---' `--''--' `----'`--' '--'`--'`----'  `----' """
    print(f"{blue_green(logo)}\n")
    print(f"{vibrant_yellow_green(' Coded by BisKit V 6.7')}\n")
    print(f"{vibrant_yellow_green(' -h to see Usage and Arguments')}\n")
    print(f"\033[38;2;255;255;255m[{blue2('WRN')}\033[38;2;255;255;255m] you can do real names what i mainly use it for")
    print("\033[38;2;255;255;255m[\033[38;5;214mWRN\033[38;2;255;255;255m]\033[38;5;214m please give me github stars\033[38;2;255;255;255m\n")
    print(f"\033[38;2;255;255;255m[{blue2('WRN')}\033[38;2;255;255;255m] don't this for harm thats it you can find your crush thats ok with me 😉\n")

def setup_argparse():
    class CustomHelpFormatter(argparse.HelpFormatter):
        def format_help(self):
            help_text = """
Arguments:
  -sf  Save the output to a file
  -bf brute-force usernames from a .txt file
  -all Search With Duckduckgo And Userlinks
  -bd brute-force usernames with duckduckgo
  -bf name,name2
  -bd name,name2
Usage:
  - python3 onerise.py <example> -sf example.txt
  - python3 onerise.py <example> for just links
  - python3 onerise.py -bf usernames.txt
  - python3 onerise.py <example> -all
  - python3 onerise.py -bd example.txt
  - python3 onerise.py example -all -sf some.txt
  - python3 onerise.py -bf name,name2
  - python3 onerise.py -bd name,name2
"""
            return help_text

    parser = argparse.ArgumentParser(
        description="Search for usernames on various websites and DuckDuckGo.",
        formatter_class=CustomHelpFormatter,  
        add_help=False  
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message and exit."
    )

    parser.add_argument("username", nargs="?", type=str, help="The username to search for.")
    parser.add_argument("-bf", "--brute-force", type=str, help="Enable brute-force username variations from a .txt file.")
    parser.add_argument("-bd", "--brute-force-duckduckgo", type=str, help="Brute-force usernames from a .txt file and search DuckDuckGo.")
    parser.add_argument("-sf", "--save-file", type=str, help="Save the results to a file.")
    parser.add_argument("-all", "--search-all", action="store_true", help="Search additional sites like DuckDuckGo.")

    return parser

def process_bf_argument(bf_arg):
    if os.path.isfile(bf_arg):  
        with open(bf_arg, "r") as f:
            usernames = [line.strip() for line in f if line.strip()]
    else:  
        usernames = bf_arg.split(",")

    return usernames

def get_random_user_agent():
    return random.choice(user_agents)

async def search_username(username, save_file=None, search_all=False):
    start_time = time.time()
    found = []
    unique_sites = set()
    duckduckgo_results = [] 

    if save_file:
        output_capture = io.StringIO()
        sys.stdout = output_capture 

    async with aiohttp.ClientSession() as session:
        tasks = [check_username_with_retries(session, site, username) for site in metadata["sites"]]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result and result[0] not in unique_sites:
                unique_sites.add(result[0])
                found.append(result)

        if search_all:
            duckduckgo_results = scrape_duckduckgo_links(username)  
            print(f"\n\033[38;2;255;255;255m[{blue_green('Duckduckgo')}\033[38;2;255;255;255m]", flush=True)  
            for link in duckduckgo_results:
                highlighted_link = highlight_url(link)
                print(f"\033[97m{highlighted_link}\033[0m", flush=True)

    elapsed_time = time.time() - start_time

    print(f"\n\033[38;2;255;255;255m[{blue_green('INF')}\033[38;2;255;255;255m] [{blue2('sites')}\033[38;2;255;255;255m] \033[38;2;255;255;255m: {len(found)}")  
    print(f"[{blue_green('*')}\033[38;2;255;255;255m] [{blue2('Time Taken')}\033[38;2;255;255;255m] \033[38;2;255;255;255m{elapsed_time:.2f} seconds\n")

    if save_file:
        sys.stdout = sys.__stdout__  
        captured_output = output_capture.getvalue()  

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}+{Fore.LIGHTGREEN_EX}] Results saved to {save_file}")
        except Exception as e:
            print(f"\033[38;2;255;255;255m[\033[38;5;196mERR\033[38;2;255;255;255m] Failed to save results to {save_file}: {str(e)}")

def scrape_duckduckgo_links(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": get_random_user_agent()}

    try:  
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a_tag in soup.find_all("a", class_="result__a", href=True):
            href = a_tag.get("href")
            if "duckduckgo.com/l/?" in href:
                parsed_url = urlparse(href)
                real_url = parse_qs(parsed_url.query).get("uddg", [None])[0]
                if real_url:
                    links.add(real_url)
            elif "duckduckgo.com" not in href:
                links.add(href)

        return list(links)

    except requests.exceptions.RequestException as e:
        print(f"\033[91mError with DuckDuckGo request: {e}\033[0m")
        return []

def highlight_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    highlighted_url = f"{Fore.LIGHTBLACK_EX}{parsed_url.scheme}://\033[38;5;10m{domain}{Fore.LIGHTBLACK_EX}{path}"

    return highlighted_url

def read_usernames_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            usernames = [line.strip() for line in file if line.strip()]
        return usernames
    except Exception as e:
        print(f"\033[91mError reading file {file_path}: {e}\033[0m")
        return []

def process_brute_force_duckduckgo(usernames_input, save_file=None, max_retries=1):
    if os.path.isfile(usernames_input):
        usernames = read_usernames_from_file(usernames_input)
    else:
        usernames = usernames_input.split(',')

    total_links_found = 0
    start_time = time.time()

    if save_file:
        output_capture = io.StringIO()
        sys.stdout = output_capture  

    for username in usernames:
        retry_count = 0
        success = False

        print(f"\033[38;2;255;255;255m[{blue_green('INF')}\033[38;2;255;255;255m] Checking {username} with DuckDuckGo", flush=True)

        while retry_count < max_retries and not success:
            duckduckgo_results = scrape_duckduckgo_links(username)

            if not duckduckgo_results:
                if retry_count == 0:
                    print(f"[\033[38;2;255;255;255m\033[38;5;196mERR\033[38;2;255;255;255m]\033[38;5;196m No results found for \033[38;2;255;255;255m{username}", flush=True)
                    print(f"\033[38;2;255;255;255m[{blue2('INFO')}\033[38;2;255;255;255m] Retrying {username}...", flush=True)

                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.91)
                else:
                    break
            else:
                for link in duckduckgo_results:
                    highlighted_link = highlight_url(link)
                    print(highlighted_link, flush=True)
                    total_links_found += 1
                success = True

        time.sleep(6.5)

    elapsed_time = time.time() - start_time

    print(f"\n\033[38;2;255;255;255m[{blue_green('INF')}\033[38;2;255;255;255m] Links: {total_links_found}")
    print(f"[\033[38;2;255;255;255m{blue2('*')}\033[38;2;255;255;255m] Time Taken: {elapsed_time:.2f} seconds\n")

    if save_file:
        sys.stdout = sys.__stdout__  
        captured_output = output_capture.getvalue()  

        try:
            with open(save_file, "a") as f:
                f.write(captured_output)
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}+{Fore.LIGHTGREEN_EX}] Results saved to {save_file}")
        except Exception as e:
            print(f"[{blue2('ERR')}] Failed to save results to {save_file}: {str(e)}")

def main():
    print_banner()  
    parser = setup_argparse()
    args = parser.parse_args()

    if hasattr(args, 'help') and args.help:
        print(parser.format_help())  
        sys.exit(0)

    if not any([args.username, args.brute_force, args.brute_force_duckduckgo]):
        sys.exit(0)

    if args.username:
        print(f"\033[38;2;255;255;255m[{blue_green('INF')}\033[38;2;255;255;255m] Emulating websites for {args.username}")
        asyncio.run(search_username(args.username, save_file=args.save_file, search_all=args.search_all))

    elif args.brute_force:
        usernames = process_bf_argument(args.brute_force)

        for username in usernames:
            print(f"\033[38;2;255;255;255m[{blue_green('INF')}\033[38;2;255;255;255m] Emulating websites for {username}")
            asyncio.run(search_username(username, save_file=args.save_file, search_all=args.search_all))

    elif args.brute_force_duckduckgo:
        process_brute_force_duckduckgo(args.brute_force_duckduckgo, save_file=args.save_file)

if __name__ == "__main__":
    main()
