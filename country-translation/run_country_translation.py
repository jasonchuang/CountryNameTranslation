#!/usr/bin/python

import sys
import os

from AndroidCountryList import AndroidCountryList

def main():
    language_list = ['ar', 'de', 'es', 'fr', 'it', 'iw', 'ja', 'ko', 'pt', 'ru', 'th', 'zh-rCN', 'zh-rTW']
    android_country_list = AndroidCountryList(os.getcwd())
    android_country_list.translate_multi_langs(language_list)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()

