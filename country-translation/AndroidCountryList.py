#!/usr/bin/python

import sys
import os

from CLDRCountryNameDict import CLDRCountryNameDict

class AndroidCountryList:
    def __init__(self, root_path):
        self.root_path = root_path
        self.country_list_path = '../../Dragon/res/xml-'
        self.country_list_file = 'country_codes.xml'
        self.code_element_start_tag = '<ISO_3166-1_Alpha-2_Code_element>'
        self.code_element_end_tag  = '</ISO_3166-1_Alpha-2_Code_element>'
        self.country_name_start_tag = '<ISO_3166-1_Country_name>'
        self.country_name_end_tag  = '</ISO_3166-1_Country_name>'
        self.country_name_dict = CLDRCountryNameDict(self.root_path + '/../CLDR')

    def translate_multi_langs(self, language_list):
        for language in language_list:
            print 'Translating lang: ' + language
            file_name = self.country_list_path + language  + '/' + self.country_list_file
            self.translate_lang(file_name, language)

    def translate_lang(self, file_name, lang):
        print 'Update ' + file_name
        output_result = ''
        default_country_name_line = ''
        file = open(file_name, 'r')
        for line in file:
            xml_line = line[:line.find('\n')]
            # Direct output line except for country name
            if xml_line.find(self.country_name_start_tag) < 0:
                # Output country name upon seeing code element
                if xml_line.find(self.code_element_start_tag) >= 0:
                    output_result += self.lookup_country_name(xml_line, default_country_name_line, lang)
                output_result += line
            else:
                default_country_name_line = line

        file.close()

        file = open(file_name, 'w')
        file.write(output_result)
        file.close()

    def lookup_country_name(self, line, default_country_name_line, lang):
        code_element = self.country_name_dict.get_string_from_context \
                (line, self.code_element_start_tag, self.code_element_end_tag)
        default_country_name = self.country_name_dict.get_string_from_context \
                (default_country_name_line, self.country_name_start_tag, self.country_name_end_tag)

        dicts = self.get_cldr_lang_dicts(lang)
        lookup_value = self.country_name_dict.lookup_from_multi_langs(code_element, dicts).upper()
        if lookup_value == default_country_name or lookup_value == 'N.A.':
            return default_country_name_line
        else:
            return '        ' + self.country_name_start_tag + lookup_value.upper() + self.country_name_end_tag + '\n'

    def get_cldr_lang_dicts(self, lang):
        list = []
        if lang.find('zh-rTW') >= 0:
            list.append('zh_Hant')
            list.append('zh')
        elif lang.find('zh-rCN') >= 0:
            list.append('zh')
        elif lang.find('iw') >= 0:
            list.append('he')
        else:
            list.append(lang)

        return list

