from distutils.core import setup, Extension

module = Extension('simplecsv', sources=['modules/simplecsv.c'])

setup(name='simplecsv',
      version='1.0',
      description='A simple CSV module',
      ext_modules=[module])
