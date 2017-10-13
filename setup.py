import re
from setuptools import setup, find_packages

# Get version without importing, which avoids dependency issues


def get_version():
    with open('app/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


setup(
    name='docker-volume-manager',
    version=get_version(),
    py_modules=['app'],
    include_package_data=True,
    install_requires=['click', 'future'],
    setup_requires=['pytest-runner', 'pytest'],
    tests_require=['pytest', 'pytest-cov', 'coverage'],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        docker-volume-manager=app.manager:cli
    ''',
)
