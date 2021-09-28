import os
import shutil
from pathlib import Path
from optparse import OptionParser

from nhentai_dl import Manga

p = OptionParser(usage='usage: %prog [options] code1 code2')
p.add_option('-a', '--archive', action="store_true", dest='archive', help='archive images to a zip file')
p.add_option('-c', '--cover', action="store_true", dest='cover', help='downloads the cover artwork')

(options, args) = p.parse_args()

for c in args:
  print(f'Fetching {c}...')

  m           = Manga(c)
  
  title       = m.title
  page_count  = m.page_count
  dir_name    = f'{m.code} - {title}'

  print(f'Title: {title}')

  Path(dir_name).mkdir(exist_ok=True)

  for i in range(page_count):
    p = m.page(i + 1)
    
    print(f'Downlading page {p.n}/{page_count}')

    dl = p.download()
    path = os.path.join(dir_name, os.path.basename(dl.url))
    open(path, 'wb').write(dl.content)
  
  if options.archive:
    print('Archiving...')

    shutil.make_archive(m.code, 'zip', dir_name)

  print('')