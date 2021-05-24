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
    
    req             = requests.get(self.url)

    self._pq        = PyQuery(req.content)
    self.title      = self._get_title()
    self.page_count = self._get_page_count()

  @property
  def url(self) -> str:
    return f'{HOSTNAME}/g/{self.code}'
  
  def _get_title(self) -> str:
    d = self._pq('h1.title').find('span.pretty')
    return d.text()
  
  def _get_page_count(self) -> int:
    d = self._pq('div.tag-container.field-name').eq(-2).find('span.name')
    return int(d.text())
  
  def download_cover(self):
    pass
  
  @property
  def cursor(self):
    return Cursor(self)

class Cursor:
  manga:  Manga
  n:      int
  
  _prefix: str

  def __init__(self, manga: Manga, n: int = 1):
    self.manga    = manga
    self.n        = n
    self._prefix  = self._get_prefix()

  def next(self):
    self.n += 1
    return self
  
  @property
  def is_valid(self):
    return self.n <= self.manga.page_count
  
  def _get_prefix(self):
    p_url = f'{self.manga.url}/{self.n}'
    req   = requests.get(p_url)
    pq    = PyQuery(req.content)
    i_url = pq('#image-container').find('img').attr('src')

    return i_url
  
  @property
  def url(self) -> str:
    return urljoin(self._prefix, f'{self.n}.jpg')
  
  def download(self):
    return requests.get(self.url)