import os
import sys
import shutil
from pathlib import Path

from nhentai_dl import Manga

for c in sys.argv[1:]:
  print(f'Fetching {c}...')
  m = Manga(c)
  
  title       = m.title
  page_count  = m.page_count
  dir_name    = f'{m.code} - {title}'

  print(f'Title: {title}')

  Path(dir_name).mkdir(exist_ok=True)

  for page in m.pages():
    print(f'Downlading page {page.n}/{page_count}')

    path = os.path.join(dir_name, f'{page.n}.jpg')
    open(path, 'wb').write(page.download().content)
    
  print('Archiving...')

  shutil.make_archive(m.code, 'zip', dir_name)

  print('')