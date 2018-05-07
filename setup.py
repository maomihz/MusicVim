from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='musicvim',
      version='0.0.1',
      description='When music meets Vim',
      url='https://maomao.blog',
      author='MaomiHz',
      author_email='null@example.com',
      license='MIT',
      packages=['musicvim'],
      install_requires=[
          'requests',
          'mutagen',
          'pyperclip'
      ],
      entry_points = {
          'console_scripts': [
              'img=musicvim.img:main'
          ],
      },
      zip_safe=False)
