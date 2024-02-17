from setuptools import setup, find_packages

setup(
    name='paypal_adrew25_package',
    version='0.1',
    packages=find_packages(),
    author='adrew25',
    author_email='adrew.1997255@gmail.com',
    description='A package for paypal integration cause i am lazy to write the same code again and again',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    license='',
    install_requires=[
        'requests',
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)