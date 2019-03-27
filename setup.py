from setuptools import setup

setup(name='curseless',
      version='0.1',
      description='''An opinionated framework for
                     python-based terminal applications''',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='terminal application framework',
      url='http://github.com/billy1kaplan/curseless',
      author='Billy Kaplan',
      author_email='billy1kaplan@gmail.com',
      license='MIT',
      packages=['curseless'],
      install_requires=[
        'curses'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
