import re
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# Get version without importing, which avoids dependency issues


def get_version():
    with open('app/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


setup(
    name='docker-volume-manager',
    description="Convenient cli app for docker volume management.",
    long_description=long_description,
    version=get_version(),
    py_modules=['app'],
    license='MIT',
    include_package_data=True,
    install_requires=['click', 'future'],
    setup_requires=['pytest-runner', 'pytest'],
    tests_require=['pytest', 'pytest-cov', 'coverage'],
    packages=find_packages(),
    zip_safe=False,
    author="Ankur Srivastava",
    download_url="https://github.com/ansrivas/docker-volume-manager/archive/1.0.0.tar.gz",
    classifiers=[
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6", ],
    entry_points='''
        [console_scripts]
        docker-volume-manager=app.manager:cli
    ''',
)
