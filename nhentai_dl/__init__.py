import requests
from pyquery import PyQuery
from urllib.parse import urljoin

HOSTNAME = 'https://nhentai.net'

class Manga:
  _pq:          PyQuery
  
  code:         str
  title:        str
  page_count:   int

  def __init__(self, code: str):
    self.code       = code

    self._pq        = PyQuery(self.request.content)
    self.title      = self._get_title()
    self.page_count = self._get_page_count()

  @property
  def request(self):
    return requests.get(self.url)
  @property
  def url(self) -> str:
    return f'{HOSTNAME}/g/{self.code}'
  
  def _get_title(self) -> str:
    d = self._pq('h1.title').find('span.pretty')
    return d.text()

  def page(self, n: int):
    return Page(self, n)
  
  def _get_page_count(self) -> int:
    d = self._pq('div.tag-container.field-name').eq(-2).find('span.name')
    return int(d.text())
  
  def download_cover(self):
    pass

class Page:
  manga:  Manga
  n:      int

  def __init__(self, manga: Manga, n: int):
    self.manga  = manga
    self.n      = n

  @property
  def url(self) -> str:
    return f'{self.manga.url}/{self.n}'
  
  @property
  def request(self):
    return requests.get(self.url)
  
  def download(self):
    pq    = PyQuery(self.request.content)
    i_url = pq('#image-container').find('img').attr('src')
    
    return requests.get(i_url)