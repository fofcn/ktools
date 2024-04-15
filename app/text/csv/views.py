import os
from random import randint
import zipfile
from flask import current_app, request, send_file
import pandas as pd

from . import csvbp
from app.error.exceptions import custom


@csvbp.route('/split', methods=['POST'])
def split():
    current_app.logger.info('split csv file')
    filename, csv_filepath, rows_per_files = __save_raw_csv_file()
    if not __is_csv_suffix(csv_filepath):
        current_app.logger.error(f'{csv_filepath} is not a CSV file')
        raise custom.CustomError('Only CSV files are allowed')
    
    is_csv_fmt = __is_csv_fmt(csv_filepath)
    if not is_csv_fmt:
        current_app.logger.error(f'{csv_filepath} is not a valid CSV file format')
        raise custom.CustomError('Only CSV files are allowed')
    
    current_app.logger.debug(f'read csv header')
    header = __read_csv_header(csv_filepath)

    current_app.logger.debug(f'generate output filename')
    output_filename = __gene_out_filename(filename)

    current_app.logger.debug(f'create temp dir')
    # 创建一个临时目录来存储分割后的CSV文件
    temp_dir = './app1/splitted_csv_file'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    current_app.logger.debug(f'split csv file')
    csv_files = __split_csv_files(csv_filepath, rows_per_files, temp_dir, output_filename, header)
    
    current_app.logger.debug(f'zip csv file')
    # 将所有CSV文件压缩到ZIP文件中
    zip_filename = f"{temp_dir}/{output_filename}.zip"
    zip_path = __create_zip_file(zip_filename, csv_files)
   
    current_app.logger.debug(f'clean resources')
    __clean_resources(raw_csvfile=csv_filepath, csv_files=csv_files, temp_dir=temp_dir)

    return send_file(zip_path, as_attachment=True)
    

def __is_csv_suffix(filename):
    if filename.endswith('.csv'):
        return True
    else:
        return False
    
def __is_csv_fmt(filepath):
    try:
        pd.read_csv(filepath)
        return True
    except pd.errors.ParserError:
        return False
    except Exception as e:
        return False

def __clean_resources(raw_csvfile, csv_files, temp_dir):
    os.remove(raw_csvfile)
    # 清理临时文件夹
    for file in csv_files:
        os.remove(file)
    # os.rmdir(temp_dir)

def __save_raw_csv_file():
    f = request.files['file']
    if f is None:
        raise custom.CustomError('No file uploaded')
    
    rows_per_files = request.form['rows_per_files']
    if rows_per_files is None:
        raise custom.CustomError('No rows_per_files specified')
    
    # changeme
    tmp_dir = './app1/raw_csv_file'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    filepath = f'{tmp_dir}/{f.filename}'

    f.save(filepath)

    return f.filename, filepath, int(rows_per_files)

def __read_csv_header(filename):
    with open(filename, 'r') as file:
        columns = file.readline().strip().split(',')
        return columns

def __create_zip_file(zip_filename, csv_files):
    zip_path = os.path.abspath(zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in csv_files:
            zipf.write(file, os.path.basename(file))

    return zip_path

def __split_csv_files(csv_filepath, rows_per_files, temp_dir, output_filename, header):
    csv_files = []

    current_app.logger.debug(f'chunk size: {rows_per_files}')
    # 分块读取数据
    reader = pd.read_csv(csv_filepath, chunksize=rows_per_files)

    os.makedirs(temp_dir, exist_ok=True)
    # 初始化文件索引
    file_index = 1

    # 遍历数据块，分别存为CSV文件
    for chunk in reader:
        # 创建文件名
        filename = __gene_splited_out_filename(output_filename, file_index)
        file_path = os.path.join(temp_dir, filename)
        csv_files.append(file_path)
        
        # 存储CSV文件
        chunk.to_csv(file_path, index=False, header=header)
        
        # 更新文件索引
        file_index += 1
    return csv_files

def __gene_out_filename(filename) -> str:
    # 生成一个1000到9999之间的随机数
    random_value = randint(1000, 9999)  
    return f"{filename}_{random_value}"

def __gene_splited_out_filename(filename, index) -> str:
    # 生成一个1000到9999之间的随机数
    random_value = randint(1000, 9999)  
    return f"{filename}_{random_value}_{index}.csv"
