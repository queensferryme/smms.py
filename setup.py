from setuptools import setup

setup(
    # package meta information
    name='smms.py',
    version='0.1.0',
    author='Queensferry',
    author_email='queensferry.me@gmail.com',
    description='command line toolkit for managing images at https://sm.ms',
    license='MIT',
    long_description=open('README.md', 'rt').read(),
    long_description_content_type='text/markdown',
    # installation options
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['smms=src.cli:cli']},
    install_requires=['Click >= 7.0', 'requests >= 2.20'],
    packages=['src']
)
