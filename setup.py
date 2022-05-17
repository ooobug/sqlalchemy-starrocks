import os
import io
import sys
from setuptools import setup, find_packages

v = open(os.path.join(
    os.path.dirname(os.path.realpath(sys.argv[0])),
    'starrocks_dialect',
    '__init__.py')
)
v.close()


this_directory = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sqlalchemy_starrocks',
      version='0.1.0',
      description='Starrocks for SQLAlchemy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      install_requires=[
          'sqlalchemy',
          'pymysql'
      ],
      keywords='SQLAlchemy Starrocks',
      author='ooobug',
      license='',
      url='',
      download_url=''
      '0.1.0.tar.gz',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'sqlalchemy.dialects': [
              'starrocks = starrocks_dialect.starrocks:StarrocksDialect'
          ]
      }
)