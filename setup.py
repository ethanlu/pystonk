from setuptools import setup, find_packages

import os

with open('README.md', 'r') as fh:
    long_description = fh.read()


def load_requirements():
    if os.getenv('PYSTONK_LAMBDA_DEPLOY'):
        # only used for deploying first lambda function to aws (for production)
        return [
            "boto3",
            "pyhocon",
            "slack_bolt"
        ]
    else:
        #  used for all other situations
        return [
            "boto3",
            "dependency-injector",
            "numpy",
            "prettytable",
            "pyhocon",
            "quickchart.io",
            "requests",
            "scipy",
            "slack_bolt",
            "termcolor",
            "wheel"
        ]

setup(
    name="pystonk",
    version="1.0.0",
    author="Ethan Lu",
    author_email="fang.lu@gmail.com",
    description="Python Stocks & Options Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethanlu/pystonk",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>3.6',
    packages=find_packages(),
    package_data={'pystonk': ['conf/*.conf']},
    install_requires=load_requirements(),
    tests_require=[
        "coverage",
        "mock"
    ],
    entry_points={
        'console_scripts': [
            'pystonk_terminal = pystonk.terminal_app:terminal',
            'pystonk_slack = pystonk.slack_app:start',
        ]
    }
)
