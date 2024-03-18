import io
import os

from setuptools import find_packages
from setuptools import setup

# package meta-data.
NAME = "openai_rag_pkg"  # name of the package
DESCRIPTION = "Retrieval-Augmented Generation for Natural Language Processing (NLP)"  # brief description
URL = "https://github.com/iamvincenzo/rag-nlp"  # URL of the repository
EMAIL = "vincenzo.fraello@outlook.it"  # author's email
AUTHOR = "Vincenzo Fraello"  # author's name
REQUIRES_PYTHON = ">=3.7.0"  # required Python version
VERSION = None  # version of the package (will be populated later)

here = os.path.abspath(os.path.dirname(__file__))

# what packages are required for this module to be executed?
try:
    with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")  # reading required packages from requirements.txt
except:
    REQUIRED = []

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()  # reading long description from README.md
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, "__version__.py")) as f:
        exec(f.read(), about)  # executing __version__.py to get version info
else:
    about["__version__"] = VERSION

setup(
    name=NAME,  # name of the Python package
    version=about["__version__"],  # version number of the package
    description=DESCRIPTION,  # brief description of the package
    long_description=long_description,  # detailed description of the package
    long_description_content_type="text/markdown",  # type of long description content
    author=AUTHOR,  # author's name
    author_email=EMAIL,  # author's email
    python_requires=REQUIRES_PYTHON,  # Python version requirements for the package
    url=URL,  # URL where the package's documentation or source code can be found
    packages=find_packages(),  # list of packages to include in the distribution
    # if your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,  # list of dependencies required for installing the package
    include_package_data=True,  # whether to include additional files specified in MANIFEST.in
    license="MIT",  # license type for the package
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],  # list of Trove classifiers to categorize the package
)
