#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
import re,  sys


class translation(object):
    def __init__(self, word, func=0):
        self.word = word
        self.func = func
        self.status = 0
        self.soup = bs('', 'lxml')
        self.pron = {}
        self.data = []
        self.error_message = ''
        self.crawl_html()
        self.get_def()

    def crawl_html(self):
        base_url = 'https://dictionary.cambridge.org/dictionary/english/'
        if len(self.word) == 0:
            self.status = 2  # no input
            self.error_message = "No input!"
            return
        else:
            url = base_url+self.word

        headers = {'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch, br',
                   'Accept-Language': 'zh-CN,zh;q=0.8', }

        if self.status == 0:
            try:
                response = requests.get(url, headers=headers, auth=('user', 'pass'))
            except requests.exceptions.RequestException as e:
                self.error_message = e
                return

        if response.status_code != 200:
            self.status = 400  # requests error
            self.error_message = "Requests related error"
            return
        else:
            html = response.text
            self.soup = bs(html, 'lxml')

    def get_pron(self):
        tmp = []
        if self.status == 1:
            for i in self.soup.findAll('span', 'uk'):
                if i.find('span', 'pron'):
                    a = i
                    break
            tmp.append(a.text)
            tmp.append(self.soup.find('span', 'uk').find(attrs={'class': "circle circle-btn sound audio_play_button uk"})['data-src-mp3'])
            self.pron['uk'] = tmp
            tmp = []
            for i in self.soup.findAll('span', 'us'):
                if i.find('span', 'pron'):
                    a=i
                    break
            tmp.append(a.text)
            tmp.append(self.soup.find('span', 'us').find(attrs={'class': "circle circle-btn sound audio_play_button us"})['data-src-mp3'])
            self.pron['us'] = tmp

    def get_def(self):
        if self.status == 0:
            for i in self.soup.findAll('div', "sense-block"):
                meaning = {}
                a = i
                if a:
                    meaning['category'] = a.get('id')
                    pharse = a.find('span', 'phrase')
                    if pharse:
                        meaning['phrase'] = pharse.text

                    abc = a.find(attrs={'class': re.compile('epp\-xref.*')})
                    if abc:
                        meaning['level'] = abc.text

                    prop = a.find('span', 'gc')
                    if prop:
                        meaning['class'] = prop.text

                    meaning['def'] = a.find('b', 'def').text
                    example = []
                    for j in i.findAll('span', 'eg'):
                        example.append(j.text)
                    meaning['eg'] = example
                self.data.append(meaning)
            if len(self.data) == 0:
                self.status = -1  # no results found error.
                self.error_message = "No results found! \n Please cheack your spelling."
            else:
                self.status = 1

    def return_result(self):
        if self.func == 0:
            b = []
            for i in self.data:
                if i['category'].startswith('amer'):
                    b.append(i)
            if len(b) == 0:
 #               self.func=1
                for i in self.data:
                    if i['category'].startswith('bri'):
                        b.append(i)
            for i in self.data:
                if i['category'].startswith('busi'):
                    b.append(i)
        else:
            b = []
            for i in self.data:
                if i['category'].startswith('bri'):
                    b.append(i)
            if len(b) == 0:
#                self.func=0
                b = self.data
            else:
                for i in self.data:
                    if i['category'].startswith('busi'):
                        b.append(i)
        if len(b) != 0:
            html_head="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><title>translation</title><style type=\"text/css\">\n" \
                "p, li { white-space: pre-wrap; }\n" \
                "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n" \
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16px; font-weight:600;\">Meaning in the Cambridge English Dictionary </span></p>\n"
            html_tail = "</body></html>"
            body = []
            for i in b:
                if 'class' in i:
                    str = "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Times New Roman,Georgia,Serif\'; font-size:28px; font-weight:600; font-style:italic; color:#00aa00;\">{}  </span>".format(i['class'])
                else:
                    str = ''
                str = str + "<span style=\" font-family:\'Times New Roman,Georgia,Serif\'; font-size:24px; color:#0000ff;\">{}</span></p>\n".format(i['def'])
                str = str + "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:20px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:19px; font-family: Helvetica, Tahoma, Arial;font-style:italic;\">" + "<br />".join(i['eg'])+"</span></p>\n<hr />\n"
                body.append(str)
            return html_head + ''.join(body)+html_tail

    def show_cmd(self):
        if self.status != 1:
            print(self.error_message)
            print("Usage: query.py word")
        else:
            print(BOLD + UNDERLINE + self.word.replace('-', ' ') + NORMAL)
            print(RED + "Translations from " + "Cambridge Dictionary" + DEFAULT)
            for i in self.data:
                if i['category'].startswith('british'):
                    if 'class' in i:
                        print(GREEN + i['class']+'  '+i['def'] + DEFAULT)
                    else:
                        print(GREEN + i['def'] + DEFAULT)
                    print('\n'.join(i['eg']))

if __name__ == "__main__":
    word = '-'.join(sys.argv[1:])
    results = translation(word)
    GREEN = "\033[1;32m"
    DEFAULT = "\033[0;49m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    NORMAL = "\033[m"
    RED = "\033[1;31m"
    results.show_cmd()
