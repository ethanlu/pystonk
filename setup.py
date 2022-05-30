from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

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
    install_requires=[
        "boto3",
        "numpy",
        "prettytable",
        "pyhocon",
        "quickchart.io",
        "requests",
        "scipy",
        "slack_bolt",
        "termcolor",
        "wheel"
    ],
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
