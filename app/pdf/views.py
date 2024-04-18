
import os
import fitz
from flask import current_app, jsonify, request

from . import pdfbp, bpapp
from ..tp import executor, tpool
from .. import app_holder

@pdfbp.route('/split', methods=['POST'])
def split_pdf():
    current_app.logger.info(f'start splitting pdf file')
    file = request.files['file']
    pages_per_file = request.form['pages_per_file']
    if file:
        file.save(file.filename)
        current_app.logger.info(f'pdf saved to {file.filename}')
        pdf_splitter_task = PdfSplitterTask(file.filename, int(pages_per_file), bpapp)
        executor.submit_task(pdf_splitter_task)
        current_app.logger.info(f'submitted task {pdf_splitter_task.get_id()}')
        return jsonify({'task_id': pdf_splitter_task.get_id()})
    else:
        return jsonify({'error': 'No file uploaded'})
    
class PdfSplitterTask(tpool.Task):

    def __init__(self, pdf_path, pages_per_file, app) -> None:
        self.pdf_path = pdf_path
        self.pages_per_file = pages_per_file
        self.__app = app
        super().__init__()

    def run(self):
        with app_holder.app_.app_context():
            return self.__split_pdf(self.pdf_path, int(self.pages_per_file))

    def __split_pdf(self, source_file_path, pages_per_file):
        current_app.logger.info(f'start splitting pdf file: {source_file_path}')
        # 首先确认文件存在
        if not os.path.exists(source_file_path):
            current_app.logger.debug("Error: Source file not found!")
            return
        # 打开源PDF文件
        source_pdf = fitz.open(source_file_path)
        total_pages = len(source_pdf)
        current_app.logger.info(f'total pdf pages: {total_pages}')

        filename, file_extension = os.path.splitext(os.path.basename(source_file_path))

        part_number = 1
        for page_start in range(0, total_pages, pages_per_file):
            current_app.logger.info(f'page start : {page_start}')
            # 创建PDF对象来保存一页页数据
            output_pdf = fitz.open()
            # 确定分割的范围
            for page_num in range(page_start, min(page_start + pages_per_file, total_pages)):
                output_pdf.insert_pdf(source_pdf, from_page=page_num, to_page=page_num)

            for each_page in output_pdf:
                # image_list = each_page.getImageList()
                #  for image_info in image_list:
                #     pix = fitz.Pixmap(output_pdf, image_info[0])
                #      png = pix.tobytes()  # return picture in png format
                #     if png == watermark_image:
                #        document._deleteObject(image_info[0])
                xref = each_page.get_contents()[0]
                cont = bytearray(each_page.read_contents())
                if cont.find(b"/Subtype/Watermark") > 0:
                    current_app.logger.info("marked-content watermark present")
                while True:
                    i1 = cont.find(b"/Artifact")  # start of definition
                    if i1 < 0: break  # none more left: done
                    i2 = cont.find(b"EMC", i1)  # end of definition
                    cont[i1-2 : i2+3] = b""  # remove the full definition source "q ... EMC"
                output_pdf.update_stream(xref, cont)  # replace the original source
            
            output_filename = f"{filename}_part_{part_number}{file_extension}"
            # 将输出文档保存为新文件
            output_pdf.save(output_filename, garbage=4, deflate=True)
            output_pdf.close()
            current_app.logger.info(f"Created: {output_filename}")
            # 更新部分文件号码
            part_number += 1

        # 关闭源PDF文件
        source_pdf.close()

        return 'ok'
