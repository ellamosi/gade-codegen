from setuptools import setup

setup(
  name='libgade-codegen',
  version='0.1',
  description='Ada source generator for libgade',
  url='https://github.com/ellamosi/libgade-codegen',
  author='Eduard Llamosi',
  license='MIT',
  packages=['libgade-codegen'],
  install_requires=[
    'stdio',
  ],
  zip_safe=False
)