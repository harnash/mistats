from setuptools import setup

setup(
    name='purifier2prometheus',
    version='0.1.1',
    packages=['server'],
    url='https://github.com/harnash/mistats',
    license='MIT',
    author='Łukasz Harasimowicz',
    author_email='developer@harnash.eu',
    description='',
    python_requires='>=3.4',
    install_requires=['python-miio', 'prometheus_client', 'structlog[dev]'],
)
