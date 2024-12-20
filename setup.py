from setuptools import setup, find_packages

import os


with open('README.md', 'r') as fh:
    long_description = fh.read()


def load_requirements():
    if os.getenv('PYSTONK_RECEIVER_DEPLOY'):
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
            "numpy",
            "prettytable",
            "pyhocon",
            "quickchart.io",
            "requests",
            "scipy",
            "slack_bolt",
            "termcolor",
            "wheel",
            "urllib3"
        ]


setup(
    name="pystonk",
    version="2.2.0",
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
    python_requires='>=3.10',
    packages=find_packages(),
    package_data={'pystonk': ['conf/*.conf']},
    install_requires=load_requirements(),
    extras_require={
        "tests": [
            "coverage",
            "mock",
            "pytest"
        ],
    },
    entry_points={
        'console_scripts': [
            'pystonk = pystonk.slack_app:start',
        ]
    }
)
