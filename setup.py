from setuptools import setup

setup(
    name='smms.py',
    version='0.0.1',
    author='Queensferry',
    author_email='queensferry.me@gmail.com',
    description='command line toolkit for managing images at https://sm.ms',
    long_description=open('README.md', 'rt').read(),
    long_description_content_type='text/markdown',
    py_modules=['main'],
    include_package_data=True,
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        smms=main:cli
    ''',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)