import os
from datetime import (
    datetime, 
    timedelta
)
from threading import Timer
from data.models import BankDetail
import requests
from bs4 import BeautifulSoup as bs
from pandas import ExcelFile

def data_download(url, download_path, log_file):
    print("Downloading files.....")
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.text, "lxml")
        all_table = soup.find_all("table", class_="tablebg")
        if len(all_table) != 2:
            return 0
        req_table = all_table[-1]
        all_banks = req_table.find_all("tr")
        for each_bank in all_banks:
            get_href = each_bank.find("a").get("href")
            print(get_href)
            try:
                quick_response = requests.get(
                    get_href, timeout=25, allow_redirects=True
                )
                file_name = os.path.join(
                    download_path, get_href.split("/")[-1]
                )
                open(file_name, 'wb').write(quick_response.content)
            except requests.exceptions.ConnectionError:
                print("[+].....Error Found for {}".format(each_bank.text))
                log_file.write(f"{ each_bank.text } ---->  {get_href }\n")
    return 1

def read_and_save(file_name, log_file):
    print(f"Reading {file_name }")
    xls = ExcelFile(file_name)
    data = xls.parse(xls.sheet_names[0])
    for row_index, row in data.iterrows():
        try:
            if 'OFFICE' in row.keys():
                branch = row['OFFICE']
            else:
                branch = row['BRANCH']
            if 'BANK NAME' in row.keys():
                bank_name = row['BANK NAME']
            else:
                bank_name = row['BANK']
            
            # checking if already there or not
            obj = BankDetail.objects.filter(
                ifsc_code=row['IFSC']
            )
            if obj:
                obj.update(
                    branch_name=branch,
                    bank_name=bank_name,
                    branch_address = row['ADDRESS']
                )
            else:
                BankDetail(
                    ifsc_code = row['IFSC'],
                    branch_name = branch,
                    bank_name = bank_name,
                    branch_address = row['ADDRESS']
                ).save()
                
        except KeyError as e:
            log_file.write(file_name)
            print(e)
            print(f"Error while reading file { file_name.split(os.sep)[-1] }\nSkipping.")
            break

def main_function():
    url = "https://www.rbi.org.in/Scripts/bs_viewcontent.aspx?Id=2009"
    download_path = os.path.join(
        os.getcwd(), 'IFSC Files'
    )
    log_file = open("download_log.txt", "w")
    skip_log_file = open("FileSkipped.txt", "w")
    print("log_file_created.")

    # this will clear the directory and make it fresh
    for root, dirs, files in os.walk(download_path):
        if files:
            for file in files:
                os.remove(os.path.join(root, file))

    bool_out = data_download(url, download_path, log_file)
    # bool_out = True
    log_file.close()
    if bool_out:
        list_of_files = list()
        for root, dirs, files in os.walk(download_path):
            for file in files:
                read_and_save(os.path.join(root, file), skip_log_file)
    skip_log_file.close()
    
def run():
    now = datetime.today()
    last_day = now.replace(day=now.day, hour=16, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = last_day - now

    secs = delta_t.total_seconds()

    t = Timer(secs, main_function)
    t.start()