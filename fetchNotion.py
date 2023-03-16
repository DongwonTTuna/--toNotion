from readCSV import getAllHoliday
from notion_client import Client
import pandas as pd
import os, datetime

def readTXTFile():
    lst = []
    with open("keys/toRead.txt",'r') as f:
        lines = f.readlines()
        for line in lines:
            lst.append(line.strip('\n'))
    return lst

def getAllHoliday():
    lst = readTXTFile()
    res = {}
    for item in lst:
        res[item.split('.')[0]] = pd.read_csv(f"csv/{item}",names=["日付","曜日","名前"],header=None)
    return res

API_KEY = os.environ["NOTION_TOKEN"]
DATABASE_KEY, VIEW_ID = map(str, os.environ["TABLE_LINK"].replace(
    'https://www.notion.so/', '').split('?v='))

notion = Client(auth=API_KEY)

items = getAllHoliday()
for item in items.values():
    df = pd.DataFrame(item)
    for index, item in df.iterrows():
        print(item['日付'])
        print(item['曜日'])
        print(item['名前'])
        date = date_obj = datetime.datetime.strptime(item['日付'], "%Y/%m/%d")

        new_page = {
            "名前": {"title": [{"text": {"content": item['名前']}}]},
            "日付": {"date": {"start": date_obj.date().isoformat()}},
            "必要品目": {"rich_text": [{"text": {"content": item["名前"]}}]},
            "タグ": {"multi_select": [{"name": "祝日"}]}
        }

        notion.pages.create(
            parent={"database_id": f"{DATABASE_KEY}"}, properties=new_page)
