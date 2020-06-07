#!/usr/bin/env python3

from typing import List, Tuple, Dict

from docx import Document  # type: ignore


def import_lines(fname: str = "sample.docx") -> Dict[str, str]:
    # print("File: %s" % fname)
    doc = Document(fname)
    book_prefix = int(fname.split("/")[-1].split("-")[0])
    # print("Book: %s" % book_prefix)

    book_index = {}
    for page in doc.tables:
        page_name = page.cell(0, 0).text
        page_rows_nums = page.cell(1, 0).text.split("\n")
        page_rows = page.cell(1, 1).text.split("\n")
        # print(len(page_rows_nums))
        # print(page_rows_nums)
        # print(len(page_rows))
        # print(page_rows)
        assert len(page_rows_nums) == len(page_rows)
        for i, n in enumerate(page_rows_nums):
            # print(page_name)
            # print(n)
            row_idx = "%d/%s%d" % (book_prefix, page_name, int(n))
            book_index[row_idx] = page_rows[i]

    return book_index


if __name__ == "__main__":
    # import_lines("../text/01-slovo1-tab.docx")
    book_lines = import_lines("../text/00-Prolog-tab.docx")
