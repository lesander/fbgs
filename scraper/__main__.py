#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from sys import exit
from .scraper import FacebookScraper
from .exceptions import ScraperException

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Facebook group scraper')
    parser.add_argument('--username', help='Facebook account username')
    parser.add_argument('--password', help='Facebook account password')
    parser.add_argument('--url', help='Facebook mobile group url')
    parser.add_argument('--output', help='Filepath to output json file')
    parser.add_argument('--shell', dest='shell', action='store_true', 
        help='Start an interactive selenium shell after finishing')
    parser.add_argument('--no-shell', dest='shell', action='store_false')
    parser.set_defaults(shell=True)
    args = parser.parse_args()

    try:
        scraper = FacebookScraper(
            username=args.username, password=args.password)
        scraper.login()

        g = scraper.scrape_group(url=args.url, out=args.output)

        if args.shell != False:
            scraper.interactive()

    except ScraperException as e:
        print(f'ScraperException: {e}')
        exit(1)
 
