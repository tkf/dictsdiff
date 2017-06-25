from setuptools import setup, find_packages

setup(
    name='dictsdiff',
    version="0.0.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Takafumi Arakaki',
    author_email='aka.tkf@gmail.com',
    # url='https://github.com/tkf/dictsdiff',
    license='BSD-2-Clause',  # SPDX short identifier
    # description='dictsdiff - THIS DOES WHAT',
    long_description=open('README.rst').read(),
    # keywords='KEYWORD, KEYWORD, KEYWORD',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: BSD License',
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': ['dictsdiff = dictsdiff.cli:main'],
    },
)
