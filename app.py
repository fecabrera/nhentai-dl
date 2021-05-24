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

  cursor = m.cursor

  while cursor.is_valid:
    print(f'Downlading page {cursor.n}/{page_count}')

    path = os.path.join(dir_name, f'{cursor.n}.jpg')
    open(path, 'wb').write(cursor.download().content)

    cursor.next()
  
  if options.archive:
    print('Archiving...')

    shutil.make_archive(m.code, 'zip', dir_name)

  print('')