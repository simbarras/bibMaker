# MIT License

# Copyright (c) 2023 Simon Barras

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Make a bibtex entry from an URL
"""

# Imports
from typing import Any
import requests
from bs4 import BeautifulSoup
from bibParser import *


# Constants
TEST_URL = "https://github.com/celeritas-project/celeritas"


class Bibliography:
    slug = ""
    title = ""
    author = ""
    year = ""
    howPublished = ""
    note = ""

    def __init__(self, url):
        self.howPublished = url

    def set_title(self, title) -> Any:
        self.title = title
        return self

    def set_author(self, author) -> Any:
        self.author = author
        return self

    def set_year(self, year) -> Any:
        self.year = year
        return self

    def set_month(self, month) -> Any:
        self.month = month
        return self

    def set_url(self, url) -> Any:
        self.url = url
        return self

    def set_note(self, note) -> Any:
        self.note = note
        return self
    
    def __call__(self, ) -> str:
        # Create slug from title and author using snake case
        # i.e: title = "Dormand-Prince method", author = "John Doe" -> slug = "dormandPrinceMethodJohnDoe"
        self.slug = self.title.replace(" ", "_").lower() + "_" +self.author.replace(" ", "_").lower()
        return self.__str__()


    def __str__(self) -> str:
        return f"""@misc{{{self.slug},
    title = {{{self.title}}},
    author = {{{self.author}}},
    year = {{{self.year}}},
    howpublished = {{{self.howPublished}}},
    note = {{{self.note}}}
}}"""


class Page:
    url = ""
    content = ""
    website = ""

    def __init__(self, url):
        self.url = url
        self.content = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        # Get TLD and SLD from URL
        self.website = '.'.join(self.url.split('/')[2].split('.')[-2:])
        print(f"Create a page for {self.website}")


    def parse(self) -> Bibliography:
        """
        Parse the webpage from HTML
        """
        bib = Bibliography(self.url)
        for psr in ParserTemplate.__subclasses__():
            if psr.id == self.website:
                return psr()(bib, self)
        else:
            return Default()(bib, self)

    def __call__(self) -> str:
        return self.parse()



def main():
    """
    Main function
    """
    print(Page(TEST_URL)())


if __name__ == '__main__':
    main()
