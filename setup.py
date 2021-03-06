from setuptools import setup, find_packages
requires = [
    "WebOb",
    "Jinja2",
    "SQLAlchemy",
    "transaction",
    "zope.sqlalchemy",
]

tests_require=[
    "nose",
    "WebTest",
]

setup(
    name="webstruct",
    version="0.0",
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "test":tests_require,
    },
    test_suite="nose.collector",
    packages=find_packages(exclude=['tests', 'examples'])
)
