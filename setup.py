import io
from setuptools import find_packages, setup

with io.open('requirements.txt') as f_in:
    install_requires = f_in.read()

setup(
    name='tweet-crawler',
    author='Robin Schaefer',
    author_email='robin.schaefer@uni-potsdam.de',
    description='A tool for crawling tweets using Tweepy.',
    long_description=io.open('README.md', mode='r', encoding='utf-8').read(),
    keywords='twitter api crawling',
    license='mit',
#    namespace_packages=
#    packages=
    install_requires=install_requires,
#    entry_points={
#        'console_scripts': [
#
#        ]
#    }
)
