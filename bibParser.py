from bibMaker import Bibliography, Page
import time
import re

class ParserTemplate:
    id: str # TLD.SLD
    def __call__(self, bib: Bibliography, page: Page) -> Bibliography:
        pass

class Default(ParserTemplate):
    id = "default"
    def __call__(self, bib: Bibliography, page: Page) -> Bibliography:
        print("Parsing with default parser")
        bib.set_title(page.content.find('title').text)
        bib.set_author("Unknown author")
        bib.set_year(time.strftime("%Y", time.localtime()))
        bib.set_month(time.strftime("%B", time.localtime()))
        return bib

class Github(ParserTemplate):
    id = "github.com"
    def __call__(self, bib: Bibliography, page: Page) -> Bibliography:
        bib = Default()(bib, page)
        print("Parsing with GitHub parser")
        commit = page.content.find('include-fragment', attrs={'aria-label': 'Loading latest commit'})['src'].split('/')[-1]
        head = page.content.find('title').text.split(' - ')[1].split(': ')
        bib.set_title(f"GitHub repository {head[0].split('/')[1]}")
        bib.set_author(head[0].split('/')[0])
        bib.add_note(f"{head[1]}")
        bib.add_note(f"Commit {commit[:7]}")
        return bib
        
