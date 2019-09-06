import sys
import re

INTERNAL_LINKS = ('pybit.es', 'codechalleng.es')

def make_html_links():
    for i, line in enumerate(sys.stdin, start=1):
        good_line = re.match(r'^(http[^,]*),(.*)$', line.strip())
        if (good_line):
            link = good_line.groups()[0].strip()
            description = good_line.groups()[1].strip()
            if (any([l in link for l in INTERNAL_LINKS])):
                print(f'<a href="{link}">{description}</a>')
            else:
                print(f'<a href="{link}" target="_blank">{description}</a>')

if __name__ == '__main__':
    make_html_links()