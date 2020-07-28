from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader(
    'version', 'sentry_chalice/version.py'
).load_module()

test_requires = [
    'pytest==5.4.3',
    'pytest-cov==2.10.0',
    'black==19.10b0',
    'isort[pipfile]==4.3.21',
    'flake8==3.8.3',
    'mypy==0.782',
    'pytest-chalice==0.0.5',
]

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='sentry_chalice',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='exceptions on chalice',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/sentry_chalice',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cuenca_validations=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'chalice==1.16.0',
        'sentry-sdk==0.16.2',
        'dataclasses>=0.6;python_version<"3.7"',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
