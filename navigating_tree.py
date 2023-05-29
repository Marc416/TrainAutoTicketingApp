html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
# 어떻게 Html을 네비게이팅하는지 알아보자
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.head)
# <head><title>The Dormouse's story</title></head>

print(soup.title)
# <title>The Dormouse's story</title>

### 특정 태그안의 child 리스트를 .contents 로 가져오는 법
head_tag = soup.head
print(head_tag)
# <head><title>The Dormouse's story</title></head>

print(head_tag.contents)
#[<title>The Dormouse's story</title>]