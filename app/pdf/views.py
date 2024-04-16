
import os
import fitz
from flask import current_app, request
from . import pdfbp

@pdfbp.route('/split', methods=['POST'])
def split_pdf():
    file = request.files['file']
    pages_per_file = request.form['pages_per_file']
    if file:
        file.save(file.filename)
        return __split_pdf(file.filename, int(pages_per_file))
    
def __split_pdf(source_file_path, pages_per_file):
    # 首先确认文件存在
    if not os.path.exists(source_file_path):
        print("Error: Source file not found!")
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
        output_filename = f"{filename}_part_{part_number}{file_extension}"
        # 将输出文档保存为新文件
        output_pdf.save(output_filename, garbage=4, deflate=True)
        output_pdf.close()
        current_app.logger.info(f"Created: {output_filename}")
        # 更新部分文件号码
        part_number += 1

    # 关闭源PDF文件
    source_pdf.close()
