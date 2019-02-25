from setuptools import setup, find_packages

setup(
    name='dictsdiff',
    version="0.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Takafumi Arakaki',
    author_email='aka.tkf@gmail.com',
    url='https://github.com/tkf/dictsdiff',
    license='BSD-2-Clause',  # SPDX short identifier
    description='CLI & Python API for comparing multiple dictionaries',
    long_description=open('README.rst').read(),
    keywords='CLI, diff, JSON, YAML, Pickle',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        'pandas',
        'PyYAML',
        'toml',
        'jsonpath-rw',
    ],
    entry_points={
        'console_scripts': ['dictsdiff = dictsdiff.cli:main'],
    },
)
