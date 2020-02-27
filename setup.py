import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="sc_scraper",
    version="0.0.1",
    url="https://github.com/ammaraskar/supreme-court-scraping",
    license="Apache License 2.0",
    maintainer="Ammar Askar",
    maintainer_email="ammar@ammaraskar.com",
    description="Scrapes the Supreme Court site for case data.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["scrapy", "requests"],
    extras_require={"test": ["pytest", "coverage", "black"]},
)
