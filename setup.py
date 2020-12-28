from setuptools import find_packages, setup

setup(
    name='flask web project',
    author="Itai Dotan",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'passlib',
    ],
    extras_require={"test": ["pytest", "coverage"]},
)
