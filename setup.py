#!/usr/bin/env python

"""The setup script."""
import setuptools
from setuptools import setup
from src.deproj import __author__, __email__, __version__

# with open('README.rst') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

install_requires = [
    'requests==2.28.2',
    "pyaml==21.10.1",
    'serde==0.9.0',
    "pytz==2022.7.1",
    "pyjq==2.6.0",
    "python-dateutil==2.8.2"
    "numpy==1.24.1",
    "pandas==1.5.3",
    "six==1.16.0",
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest>=3',
    "mock==4.0.3"
]

setup(
    name='deproj',
    author=__author__,
    author_email=__email__,
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description="This project creates a baseball card, minus the graphic design.",
    entry_points={
        'console_scripts': [
            'deproj=deproj.cli:main',
        ],
    },
    install_requires=install_requires,
    license="Apache Software License 2.0",
    # long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='deproj',
    # packages=find_packages(include=['deproj', 'deproj.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nikolauspschuetz/deproj',
    version=__version__,
    zip_safe=False,
    packages=setuptools.find_packages("./src"),
    package_data={"configs": [
        'configs/deproj/**',
        "configs/endpoint-statsapi.yaml"
    ]},
    package_dir={
        "": "src"
    }
)
