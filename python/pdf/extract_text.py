#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@desc: 提取pdf文件的内容
"""

# !chapter_005/src/snippet_005.py
import typing
from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


def main():
    # read the Document
    doc: typing.Optional[Document] = None
    print(1)
    l: SimpleTextExtraction = SimpleTextExtraction()
    print(2)
    with open("output.pdf", "rb") as in_file_handle:
        print(3)
        doc = PDF.loads(in_file_handle, [l])
        print(4)

    # check whether we have read a Document
    assert doc is not None
    print(5)
    # print the text on the first Page
    print(l.get_text_for_page(0))
    print(6)


if __name__ == "__main__":
    main()
