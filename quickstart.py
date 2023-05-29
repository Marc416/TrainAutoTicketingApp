from bs4 import BeautifulSoup
from lxml.builder import unicode

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
unicode(tag.string)
type(tag)