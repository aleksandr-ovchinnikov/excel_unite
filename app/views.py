import zipfile
import shutil
import os
import chardet
import string
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from time import sleep
import pandas as pd


def is_valid_filename(filename):
    try:
        filename.encode('cp437').decode('cp866')
        return True
    except UnicodeEncodeError:
        return False


def delete_recursive_directory(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")


def unzip_file():
    with zipfile.ZipFile(os.path.join('uploads', 'temp.zip'), 'r') as zip_ref:
        for file in zip_ref.namelist():
            if is_valid_filename(file):
                try:
                    zip_ref.extract(file, os.path.join(settings.MEDIA_ROOT, 'uploads'))
                    source = os.path.join(settings.MEDIA_ROOT, 'uploads', file)
                    target = os.path.join(settings.MEDIA_ROOT, 'uploads', file.encode('cp437').decode('cp866'))
                    if os.path.exists(source):
                        shutil.move(source, target)
                except (UnicodeEncodeError, FileNotFoundError) as e:
                    pass
        old_floder = "/".join(map(str, source.split('/')[:2]))
        delete_recursive_directory(path=old_floder)


def delete_files_in_directory(directory):
    needed_dirs = ["Пробеги_Глонасс", "Пробеги_УАТХ", "Топливо_Глонасс", "Топливо_УАТХ"]
    for root, dirs, files in os.walk(directory):
        if os.path.basename(root) in needed_dirs:
            shutil.move(root, f'data/{os.path.basename(root)}')
    shutil.rmtree('uploads')
    # for filename in os.listdir(directory):
    #     file_path = os.path.join(directory, filename)
    #     try:
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)
    #             continue
    #         if os.path.isdir(file_path) and filename not in needed_dirs:
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print(f"Error: {e}")

def handle_uploaded_file(f):
    upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(os.path.join(upload_dir, 'temp.zip'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def extract_data_from_excel(file_path):
    if file_path.endswith('.xlsx'):
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
    else:
        return None


def get_data():
    # init
    mileage_glonass = []
    mileage_uath = []
    fuel_glonass = []
    fule_uath = []
    needed_dirs = ["Пробеги_Глонасс", "Пробеги_УАТХ", "Топливо_Глонасс", "Топливо_УАТХ"]
    
    # Process
    for root, dirs, files in os.walk('data'):
        root_name = os.path.basename(root)
        if root_name in needed_dirs:
            if root_name == "Пробеги_Глонасс":
                for file in os.listdir(root):
                    if file.endswith('.xlsx') and not file.startswith('~'):
                        file_path = os.path.join(root, file)
                        df = pd.read_excel(file_path)
                        for index, row in df.iterrows():
                            mileage_glonass.append(row.to_list())
                            
            elif root_name == "Пробеги_УАТХ":
                for file in os.listdir(root):
                    if file.endswith('.xlsx') and not file.startswith('~'):
                        file_path = os.path.join(root, file)
                        df = pd.read_excel(file_path)
                        for index, row in df.iterrows():
                            mileage_uath.append(row.to_list())

            elif root_name == "Топливо_Глонасс":
                for file in os.listdir(root):
                    if file.endswith('.xlsx') and not file.startswith('~'):
                        file_path = os.path.join(root, file)
                        df = pd.read_excel(file_path)
                        for index, row in df.iterrows():
                            fuel_glonass.append(row.to_list())
            
            elif root_name == "Топливо_УАТХ":
                for file in os.listdir(root):
                    if file.endswith('.xlsx') and not file.startswith('~'):
                        file_path = os.path.join(root, file)
                        df = pd.read_excel(file_path)
                        for index, row in df.iterrows():
                            fule_uath.append(row.to_list())

    return {
        "Пробеги_Глонасс" : mileage_glonass, 
        "Пробеги_УАТХ": mileage_uath,
        "Топливо_Глонасс": fuel_glonass,
        "Топливо_УАТХ": fule_uath
    }



def home(request):
    if request.method == 'POST':
        shutil.rmtree('data')
        handle_uploaded_file(request.FILES['file'])
        unzip_file()
        os.remove(os.path.join('uploads', 'temp.zip'))
        sleep(2)
        delete_files_in_directory('uploads')
        data = get_data()
        return HttpResponse("Файл успешно загружен и распакован!")
    return render(request, 'app/index.html')

