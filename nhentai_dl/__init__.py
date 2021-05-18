import requests
from pyquery import PyQuery

HOSTNAME = 'https://nhentai.net'

class Manga:
  _pq:          PyQuery
  
  code:         str
  title:        str
  page_count:   int
  img_prefix:   str

  def __init__(self, code: str):
    self.code       = code
    
    req             = requests.get(self.url)

    self._pq        = PyQuery(req.content)
    self.title      = self.get_title()
    self.page_count = self.get_page_count()
    self.img_prefix = self.get_img_prefix()

  @property
  def url(self) -> str:
    return f'{HOSTNAME}/g/{self.code}'
  
  @property
  def cover_url(self) -> str:
    return f'{self.img_prefix}/cover.jpg'
  
  def get_title(self) -> str:
    d = self._pq('h1.title').find('span.pretty')
    return d.text()
  
  def get_page_count(self) -> int:
    d = self._pq('div.tag-container.field-name').eq(-2).find('span.name')
    return int(d.text())
  
  def get_img_prefix(self):
    d = self._pq('div#cover').find('img').attr('data-src')
    return d.replace('/cover.jpg', '')
  
  def download_cover(self):
    return requests.get(self.cover_url)
  
  def page(self, n: int):
    return Page(self, n)

  def pages(self):
    return [self.page(i + 1) for i in range(self.page_count)]

class Page:
  manga:  Manga
  n:      int
  _pq:    PyQuery

  def __init__(self, manga: Manga, n: int):
    self.manga  = manga
    self.n      = n
  
  @property
  def url(self) -> str:
    return f'{self.manga.img_prefix}/{self.n}.jpg'
  
  def download(self):
    return requests.get(self.url)