#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="dados.br",
      version="0.1",
      description="Python wrapper for dados.gov.br API",
      license="MIT",
      install_requires=[],
      author="Maycon Bordin",
      author_email="mayconbordin@gmail.com",
      url="http://github.com/mayconbordin/dados.br",
      packages=['dadosbr'],
      package_dir={'dadosbr': 'dadosbr'},
      keywords= "open data, api wapper, brasil",
      zip_safe = True)
