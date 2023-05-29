# beautiful_soup

beautiful soup을 사용하기 위해서는 4가지 오브젝트를 사용할 줄 알아야한다.  
--> `Tag, NavigableString, BeautifulSoup, and Comment`.

**Quickstart Example**

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
type(tag)
```

### Tag

```python
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
type(tag)
```

### NavigableString

```python
tag.string
# u'Extremely bold'
type(tag.string)
# <class 'bs4.element.NavigableString'>
```

NavigableString을 문자열로 사용하기 위해서는 파이썬 유니코드로 변형해서 써야 한다

```python
unicode_string = unicode(tag.string)
unicode_string
# u'Extremely bold'
type(unicode_string)
# <type 'unicode'>
```

그렇게 하지 않았을 경우 메모리낭비를 많이 할 것이다.  
If you don’t, your string will carry around a reference to the entire Beautiful Soup parse tree, 
even when you’re done using Beautiful Soup. This is a big waste of memory.

### BeautifulSoup
html 을 파싱한 오브젝트를 말한다.
Html tree를 Navigating 하거나 Searching 할 수 있다.  
BeautifulSoup 오브젝트는 Tag 오브젝트와 같은 기능을 가지고 있다.

```python
doc = BeautifulSoup("<document><content/>INSERT FOOTER HERE</document", "xml")
footer = BeautifulSoup("<footer>Here's the footer</footer>", "xml")
doc.find(text="INSERT FOOTER HERE").replace_with(footer)
# u'INSERT FOOTER HERE'
print(doc)
# <?xml version="1.0" encoding="utf-8"?>
# <document><content/><footer>Here's the footer</footer></document>
```

### Comment
위 세가지정도면 충분히 스크래핑 할 수 있을 테지만 Comment가 남았다.  

```python   
markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup)
comment = soup.b.string
type(comment)
# <class 'bs4.element.Comment'>

comment
# u'Hey, buddy. Want to buy a used parser'
```
comment 는 NavigableString 에 포함되고 특별한 형식을 가진다.  
문서에 설명이 더 있지만 이 기능을 쓰지않을것 같아서 더이상 보지 않도록 한다.  
```python
print(soup.b.prettify())
# <b>
#  <!--Hey, buddy. Want to buy a used parser?-->
# </b>
```

---
# Selenium
스크래핑 자동화를 위해 셀레니움을 이용해보자.  
셀레니움은 브라우저에게 뭔가하라고 명령을 보내거나 request를 보내는 것이다.  
우선 셀레니움을 설치한다.  
다음으로 사용자의 크롭 버전에 맞는 크롬드라이버를 다운로드한다.  
[https://chromedriver.chromium.org/downloads]  
