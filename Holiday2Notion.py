from notion_client import Client
import pandas as pd
import os, datetime

def readTXTFile():
    lst = []
    for file in os.listdir("csv"):
        if file.endswith('.csv'):
            lst.append(file)
    return lst

def getAllHoliday():
    lst = readTXTFile()
    res = {}
    for item in lst:
        res[item.split('.')[0]] = pd.read_csv(f"csv/{item}",names=["日付","曜日","名前"],header=None)
    return res

print("Notion API Keyを入力してください。")
API_KEY = input()
print("データベースのリンクを入力してください。")
DATABASE_KEY, VIEW_ID = map(str, input().replace(
    'https://www.notion.so/', '').split('?v='))

notion = Client(auth=API_KEY)

items = getAllHoliday()
for item in items.values():
    df = pd.DataFrame(item)
    for index, item in df.iterrows():
        
        date = date_obj = datetime.datetime.strptime(item['日付'], "%Y/%m/%d")

        new_page = {
            "名前": {"title": [{"text": {"content": item['名前']}}]},
            "日付": {"date": {"start": date_obj.date().isoformat()}},
            "タグ": {"multi_select": [{"name": "祝日"}]}
        }
        try:
            notion.pages.create(
            parent={"database_id": f"{DATABASE_KEY}"}, properties=new_page)
        except Exception as err:
            print(f"名前 : { item['名前']} 日付 : {item['日付']} を追加する途中にエラーが発生しました。")
            print("エラー：")
            print(err)
        print(f"名前 : { item['名前']} 日付 : {item['日付']} がデータベースに追加されました ")
