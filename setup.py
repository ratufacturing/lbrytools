from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
  
setup(
    name="lbrytools",
    version="0.1.0",
    author="ratufacturing",
    description="Belikor's lbrytools repository", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ratufacturing/lbrytools/",
    packages=find_packages(),
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[                      # External dependencies (if any)
        "requests",
        "PyMuPDF",
        "regex",
        "numpy",
        "pyexcel",
        "pyexcel-ods",
    ],
    include_package_data=True,              # Automatically include non-Python files specified in MANIFEST.in (optional)
    python_requires=">=3.6",                 # Python version requirements
)
