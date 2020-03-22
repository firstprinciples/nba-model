import setuptools
import fps_nbamodel2

# Get the version of this package
version = fps_nbamodel2.version

# Get the long description of this package
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fps_nbamodel2',
    version=version,
    author="RichardP",
    author_email="rcpattison@gmail.com",
    description="cleaner project folder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firstprinciples/nbamodel2",
    packages=setuptools.find_packages(exclude=['unit_tests']),
    install_requires=[],
    package_data={'fps_nbamodel2': ['models/*.joblib']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
