import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__),fname)).read()

setup(
    name = "yify",
    version = "0.2.5",
    author = "vitaminC",
    author_email = "dmakhil@gmail.com",
    url="https://github.com/AkhilMaskery/yify",
    description = ("browse yify on your command line"),
    entry_points={'console_scripts':['yify=yify.command_line:main']},
    license = "GPLv3",
    keywords = "yify torrent download",
    packages = ['yify'],
    install_requires=[
              'requests',
          ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)

