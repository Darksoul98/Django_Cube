# from .base import *
import os
# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
file = os.environ.get('DJANGO_ENV')
if file == 'production':
   from .production import *
else:
   from .local import *
