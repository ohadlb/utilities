from distutils.core import setup

setup(name='utils',
      version='0.0.1',
      py_modules=['utils'],
      requires=['timeout-decorator',
                'tqdm',
                'typeguard'])
