# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    spider                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cmaurici <cmaurici@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 11:41:11 by cmaurici          #+#    #+#              #
#    Updated: 2023/06/01 19:48:56 by cmaurici         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import urllib.request
import argparse
import requests
import shutil
import sys
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Function to extract images from a given URL recursively up to a certain depth level

def get_images(url, depth, base_path, extensions, count):
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    valid = 1
    if base_url.startswith("http"):
        web = 1
        try:
            r = requests.get(url)
        except:
            valid = 0
        if valid:
            soup = BeautifulSoup(r.content, 'html.parser')
    elif base_url.startswith("file://"):
        web = 0
        with urllib.request.urlopen(url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
    else:
        try:
            with open(url, 'r') as f:
                web = 0
                r = f.read()
                soup = BeautifulSoup(r, 'html.parser')
        except ValueError:
            print(f"{base_path} does not exist")
    if valid:
        images = soup.find_all('img')
        print(f"Total {len(images)} images found!")
        if len(images) != 0:
            for i, image in enumerate(images):
                try:
                    image_url = image.get('src')
                except:
                    pass
                _, ext = os.path.splitext(image_url)
                if ext.lower() not in extensions:
                    continue
                if web == 0:
                    image_name = os.path.basename(image_url)
                    url = url.replace("file://", "")
                    item_path = os.path.join(os.path.dirname(url), image_url)
                    try:
                        dest_path = os.path.join(base_path, image_name)
                        try:
                            shutil.copy2(item_path, dest_path)
                            count += 1
                        except:
                            print("IMAGE DOESN'T EXIST")
                    except:
                        pass
                else:
                    image_url = urljoin(base_url, image_url)
                    try:
                        r = requests.get(image_url).content
                        try:
                            r = str(r, 'utf-8')
                        except UnicodeDecodeError:
                            image_name = os.path.basename(image_url)
                            with open(f"{base_path}/{image_name}", "wb+") as f:
                                f.write(r)
                        count += 1
                    except:
                        pass
        if depth > 0:    
            for link in soup.find_all('a'):
                href = link.get('href')
                if not href:
                    continue
                href = urljoin(base_url, href)
                if href.startswith(base_url):
                    get_images(href, depth - 1, base_path, extensions, count)
        if count == len(images):
            print("All images downloaded!")
            return 1
        else:
            print(f"Total {i} images downloaded out of {len(images)}")
            return 1
    else:
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spider program to extract images from a URL")
    parser.add_argument('-r', action='store_true', help= 'recursively downloads images from the URL given as a parameter')
    parser.add_argument('-l', nargs="?", const=5, type=int, help='indicated the max depth level of recursive downloading')
    parser.add_argument('-p', default='./data/', help='download path')
    parser.add_argument('url', nargs="?", help='URL to extract images from')
    args = parser.parse_args()
    if args.l and not args.r:
        print("Need -r to download recursively")
        args.l = 0
    if not args.l:
        args.l = 0
    if str.startswith(args.p, "http") or str.endswith(args.p, ".html"):
        args.url = args.p
        args.p = "./data/"
    extensions = ('.jpg', '.jpeg', '.gif', '.png', '.bmp')
    if args.url == None:
        print("Usage: ./spider (-r) (-l [N]) (-p [PATH]) url")
        exit()
    if not os.path.exists(args.p):
        os.makedirs(args.p)
    count = 0
    v = get_images(args.url, args.l, args.p, extensions, count)
    if v == 0:
        print("URL not valid")
    elif args.r:
        print(f"Downloaded recursively with depth {args.l}")
    else:
        print("Downloaded non-recursively")              
