import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shelly-test",
    version="0.0.2",
    author="Floplosion05",
    author_email="florfuchs2005@gmail.com",
    license='MIT',
    description="A test package for shelly devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='shelly login shelly-login'
    url="https://github.com/Floplosion05/Shelly",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  
        'requests>=2.24.0',
        'passlib >= 1.7.4'
    ],
    python_requires='>=3.6'
)
