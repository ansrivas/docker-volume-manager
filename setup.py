from setuptools import setup

setup(
    name='docker-volume-manager',
    version='1.0',
    py_modules=['app'],
    include_package_data=True,
    install_requires=[
        'click', 'future'],
    entry_points='''
        [console_scripts]
        docker-volume-manager=app.manager:cli
    ''',
)
