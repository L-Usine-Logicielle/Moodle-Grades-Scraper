from setuptools import setup

setup(
    name='mootse-runner',
    packages=['application'],
    version='1.2',
    install_requires=[
        'APScheduler==3.10.1',
        'beautifulsoup4==4.12.2',
        'bs4==0.0.1',
        'certifi==2023.7.22',
        'charset-normalizer==3.1.0',
        'idna==3.4',
        'requests==2.31.0',
        'mysql-connector-python==8.0.33',
        'setuptools==65.5.1',
        'soupsieve==2.4',
        'urllib3>=1.26.18'
    ],
    description='Système de notifications pour Mootse, le Moodle de Télécom Saint-Etienne',
)
