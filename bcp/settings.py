# Settings for barcode printer

import os

# Barcode
BAR_HEIGHT = 30
BAR_WIDTH = 0.75 # default is 0.54
BAR_QUIET = False # include l/r whitespace padding.
BAR_CHECKSUM = True

# Label Config
FONT_SIZE = 8
FONT_NAME = 'regular'
FONT_PATH = os.path.join(os.path.split(__file__)[0], 'fonts', 'lucida_sans_regular.ttf',)

IMAGE_PATH = os.path.join(os.path.split(__file__)[0], 'img', 'bannner.png',)

IMAGE_REDE = os.path.join(os.path.split(__file__)[0], 'img', 'rede2.png',)
# IMAGE_POP = os.path.join(os.path.split(__file__)[0], 'img', 'pop.png',)
IMAGE_MASTER = os.path.join(os.path.split(__file__)[0], 'img', 'master.png',)
IMAGE_CDL = os.path.join(os.path.split(__file__)[0], 'img', 'cdl.png',)
IMAGE_MARKO = os.path.join(os.path.split(__file__)[0], 'img', 'solution.png',)

FONT_BOLD = 'bold'
FONT_PATH_BOLD = os.path.join(os.path.split(__file__)[0], 'fonts', 'LSANSDI.TTF',)
# NB It's a better idea to put your settings in a local_settings.py overrides file.
try:
    from local_settings import *
except ImportError:
    pass
