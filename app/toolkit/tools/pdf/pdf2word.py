


import os
from pdf2docx import Converter
# from ...common.factory import AbsToolFunc


class Pdf2Word():

    def __init__(self):
        self.name = "pdf_2_word"

    def run(self, args):
        pdf_file_path = args.get("pdf_file_path")
        docx_file_path = os.path.split(pdf_file_path)[0] + '.docx'
        print(docx_file_path)
        cv = Converter(pdf_file_path)
        cv.convert(docx_file_path)
        cv.close()



