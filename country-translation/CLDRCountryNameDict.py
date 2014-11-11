#!/usr/bin/python

import sys
import os

class CLDRCountryNameDict:
    def __init__(self, cldr_root_path):
        self.cldr_root_path = cldr_root_path
        self.lang_xml_path = '/core/common/main/'
        self.not_found = 'N.A.'
        self.territory_start_tag = '<territory type=\"'
        self.territory_end_tag = '</territory>'

    def lookup_from_multi_langs(self, key, langs):
        # first match return
        for lang in langs:
            value = self.lookup(key, lang)
            if value.find(self.not_found) < 0:
                return value
        return self.not_found

    def lookup(self, key, lang):
        lang_file = self.cldr_root_path + self.lang_xml_path + lang + '.xml'
        keyword = self.territory_start_tag + key + '\">'
        file = open(lang_file, 'r')
        for line in file:
            statement = line[:line.find('\n')]
            if statement.find(keyword) >= 0:
                return self.get_string_from_context(statement, keyword, self.territory_end_tag)

        return self.not_found

    def get_keyword_end(self, line, keyword):
        return line.find(keyword) + len(keyword)

    def get_string_from_context(self, line, keyword_prefix, keyword_postfix):
        start = self.get_keyword_end(line, keyword_prefix)
        end = line.find(keyword_postfix)
        name = line[start:end]
        return name


