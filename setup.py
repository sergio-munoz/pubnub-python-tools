#from setuptools import setup

#setup(
    #name='ppt',
    #version='1.0.0',
    #py_modules=['src/pubnub_python_tools'],
    #install_requires=[
        #'Click',
    #],
    #entry_points={
        #'console_scripts': [
            #'ppt = cli.click:main',
        #],
    #},
#)

from setuptools import setup, find_packages

setup(
    name='pubnub-python-tools',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pubnub',
    ],
    entry_points={
        'console_scripts': [
            'pubnub-python-tools = pubnub_python_tools.scripts.cli:click',
        ],
    },
)