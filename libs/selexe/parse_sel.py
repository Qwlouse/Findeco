import re, BeautifulSoup
from htmlentitydefs import name2codepoint


class SeleniumParser(object):
    def __init__(self, fp):
        self.fp = fp
        self.soup = BeautifulSoup.BeautifulSoup(fp.read())
        baseUrlLink = self.soup.find('link', attrs={'rel': 'selenium.base'})
        self.baseuri = baseUrlLink['href'] if baseUrlLink else None

    def __iter__(self):
        body = self.soup.find('tbody')
        for tr in body.findAll('tr'):
            # return tuple (command, target, value) -> this corresponds to column names in Selenium IDE
            command, target, value = [td.renderContents() for td in tr.findAll('td')]
            v_value = handleTags(value)
            v_target = handleTags(target)
            v_value = htmlentitydecode(v_value)
            v_target = htmlentitydecode(v_target)
            yield (command, v_target, v_value)



def htmlentitydecode(s):
    """translate all HTML entities like &nbsp; into clean text characters"""
    return re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

def handleTags(s):
    s = re.sub("\s*<br />\s*", "\n", s)
    return re.sub("<.*>", "", s)


if __name__ == '__main__':
    import sys
    fp = open(sys.argv[1])
    p = SeleniumParser(fp)
    print list(p)
