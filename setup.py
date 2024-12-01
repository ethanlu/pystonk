from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name="pystonk",
    version="2.1.1",
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
    python_requires='>=3.9',
    packages=find_packages(),
    package_data={'pystonk': ['conf/*.conf']},
    install_requires=[
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
        "wheel",
        "urllib3"
    ],
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
