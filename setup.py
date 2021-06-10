import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='OSRSBytes',  
    version='1.2.4',
    author="Coffee Fueled Deadlines",
    author_email="cookm0803@gmail.com",
    description="An all-in-one OSRS Library with Hiscores and Grand Exchange Market Information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Coffee-fueled-deadlines/OSRSBytes",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
)
