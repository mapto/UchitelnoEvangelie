#!/usr/bin/env python3

"""Using textract seems to be a very bad method to extract text from tables.
One of the reasons: it parses the text in tables in different formats in different order."""

import re
import textract


class DocumentHandler:
    column_number = r"\d\d[ac]"

    @staticmethod
    def create(filename):
        handlers = {"doc": DocHandler, "docx": DocxHandler, "odt": OdtHandler}
        ext = filename.split(".")[-1].lower()
        if ext in handlers:
            return handlers[ext](filename)
        else:
            raise NotImplmentedError

    def __init__(self, filename):
        self._pages = {}
        self.__content = textract.process(filename).decode("utf-8")

        self.__split_pages()
        self.__clean_footnotes()
        # self.clean_hyphens()

    def __split_pages(self):
        self.header = "%d%s" + self.in_header + "%d%s"
        content = self.__content
        fcol = re.search(self.column_number, content).start()
        count = int(content[fcol : fcol + 2])
        letter = content[fcol + 2 : fcol + 3]
        self.__first_key = str(count) + letter
        prev_key = None
        more = True
        doc_pages = {}

        while more:
            header = re.compile(
                self.header % (count, letter, count, chr(ord(letter) + 1))
            )
            parts = re.split(header, content)
            if prev_key:
                doc_pages[prev_key] = parts[0].strip()
            prev_key = str(count) + letter
            more = len(parts) > 1
            if more:
                content = parts[1]
                if letter == "c":
                    count += 1
                letter = "a" if letter == "c" else "c"
            else:
                self.__last_key = str(count) + chr(ord(letter) + 1)
        self.__pages_content = doc_pages
        for k in self.__pages_content.keys():
            self._process_page(k)

    def _page_parts(self, page: str, part: int):
        return re.split(self.page_separator, self.__pages_content[page])[part]

    def _process_page(self, page: str):
        """Process page for column-based parsers"""
        dirty_pages = re.split(self.column_index, self._page_parts(page, 0))
        first = page
        second = page[:-1] + chr(ord(page[-1]) + 1)
        self._pages[first] = []
        self._pages[second] = []
        # if len(dirty_pages) < 2:
        # 	print(first)
        # 	print(dirty_pages)
        rows = re.split(self.line_separator, dirty_pages[1])
        rows = [r.strip() for r in rows]
        while not rows[-1]:
            rows = rows[:-1]
        self._pages[first].extend(rows)
        if len(dirty_pages) > 2:
            rows = re.split(self.line_separator, dirty_pages[2])
        else:
            dirty_pages = re.split(self.column_index, self._page_parts(page, 1))
            rows = re.split(self.line_separator, dirty_pages[1])
        rows = [r.strip() for r in rows]
        while not rows[-1]:
            rows = rows[:-1]
        self._pages[second].extend(rows)

    def _clean_page(self, page_num):
        pass

    def __clean_footnotes(self):
        for k in self._pages.keys():
            self._clean_page(k)

    def clean_hyphens(self):
        prevpage = None
        ppi = None
        prevline = None
        for npi, nextpage in self._pages.items():
            for nli, nextline in enumerate(nextpage):
                if prevline and prevline[-1] == "-":
                    prevwords = re.split("\s", prevline)
                    nextwords = re.split("\s", nextline)
                    assert len(nextwords) > 0
                    assert len(prevwords) > 0
                    prevwords[-1] = prevwords[-1][:-1] + nextwords[0]
                    prevline = " ".join(prevwords)
                    nextline = " ".join(nextwords[1:])
                    if nli == 0:
                        self._pages[ppi][-1] = prevline
                    else:
                        self._pages[npi][nli - 1] = prevline
                    if len(self._pages[npi]) == nli and nextline:
                        self._pages[npi].append(nextline)
                    else:
                        self._pages[npi][nli] = nextline
                prevline = nextline
            prevpage = nextpage
            ppi = npi

    def extract_words(self, delims=r"[\s\.\(\)\!⁘]*"):
        result = []
        for page, content in self._pages.items():
            for num, row in enumerate(content):
                for word in re.split(delims, row):
                    if word:
                        result.append(("{}{}".format(page, num + 1), word, row))
        return result

    def stats(self):
        print(
            "format: {:s}; total columns: {:d} ({:s}-{:s})".format(
                self.ext, len(self.pages()), self.__first_key, self.__last_key
            )
        )
        print(
            "page chars: {:s}".format(
                ",".join(str(len(p)) for p in self.__pages_content.values())
            )
        )
        print(
            "column rows: {:s}".format(
                "; ".join(
                    "{:s}: {:d}".format(k, len(self.page(k)))
                    for k in self._pages.keys()
                )
            )
        )
        print()

    def pages(self):
        return self._pages

    def page(self, i: str):
        return self._pages[i]


class OdtHandler(DocumentHandler):
    """ Incomplete because .odt import adds further dirty characters on footnotes """

    ext = "odt"
    in_header = r"\n\n"
    page_separator = r"\D\n\n\n"
    line_separator = r"\n"
    column_index = r"3\n{3}6\n{3}9\n{3}12\n{3}15\n{3}18\n{3}21\n{0,3}"

    def _clean_page(self, page_num):
        # TODO: .odt import adds further dirty characters on footnotes
        for i, l in enumerate(self._pages[page_num]):
            self._pages[page_num][i] = re.sub("\d+", "", l)


class DocxHandler(DocumentHandler):
    ext = "docx"
    in_header = r"\n\n\n\n"
    page_separator = r"\n\n\t\t\n\n"
    line_separator = r"\n\n"
    # column_index = r"([\d]{1,2}\n{6}){6}([\d]{2}\n*)?"
    # Assumes that there are at least 21 lines in a page
    column_index = r"3\n{6}6\n{6}9\n{6}12\n{6}15\n{6}18\n{6}21\n{0,6}"


class DocHandler(DocumentHandler):
    ext = "doc"
    in_header = r"\s*[\|]\s\s[\|]"
    page_separator = r"[ ]+\|\n(\n)+"
    line_separator = r"\|\n\|[ \d]{2}\|"
    column_separator = r"\|[ \d]{2}\|"

    def _process_page(self, page: str):
        """Row-based page processing"""
        dirty_lines = re.split(self.line_separator, self._page_parts(page, 0))
        first = page
        second = page[:-1] + chr(ord(page[-1]) + 1)
        self._pages[first] = []
        self._pages[second] = []
        for l in dirty_lines:
            if l:
                next = re.split(self.column_separator, l)
                if next[0].strip():
                    self._pages[first].append(next[0].strip())
                if next[1].strip():
                    self._pages[second].append(next[1].strip())

    def _clean_page(self, page_num):
        p = ";".join(self._pages[page_num])
        p = re.sub("\[\d+\];", " ", p)
        p = re.sub("\[\d+\]", "", p)
        self._pages[page_num] = p.split(";")


def parallel():
    path = "/home/mapto/work/uchenie-evangelsko/UE-Comp"
    name = "4slovo-Bg-LT"
    no_ext = "%s/%s" % (path, name)

    docs = [
        DocxHandler(no_ext + ".docx"),
        DocHandler(no_ext + ".doc"),
        OdtHandler(no_ext + ".odt"),
    ]
    for d in docs:
        d.stats()


def one(ext: str = "doc"):
    filename = "/home/mapto/work/uchenie-evangelsko/UE-Comp/4slovo-Bg-LT." + ext
    d = DocumentHandler.create(filename)
    d.stats()


def all():
    ext = ["doc", "docx", "odt"]
    for e in ext:
        filename = "/home/mapto/work/uchenie-evangelsko/UE-Comp/4slovo-Bg-LT." + e
        d = DocumentHandler.create(filename)
        d.stats()


if __name__ == "__main__":
    all()
    # one()
    # parallel()
