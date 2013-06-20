#!/usr/bin/env python

from distutils.core import setup

setup(name='LUCID',
      version='1.0',
      description='Loops and Micro Cristals IDentifier',
      author='Etienne Francois',
      author_email='etienne.francois@esrf.fr',
      packages=['lucid'],
      package_data={'lucid':['reference.png']},
      install_requires=[
      'Python<=2.7',
      'Opencv>=2.1',
      'PyFAI',
      'numpy',
      'scipy'
      ],
     )

