'''
□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■
2023年12月28日
決裁承認申請データ管理
Tnetからcsv出力したデータを加工してデータベース化
□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■
'''
import os
import pandas  as pd
import io
import sqlite3

import japanize_matplotlib # プロンプトで「pip install japanize-matplotlib」を実行

master_file_path = 'C:\\Users\\0425\\01_work\\01_Python\\02_data\\05_KessaiData//master.csv'
import_file_path = 'C:\\Users\\0425\\01_work\\01_Python\\02_data\\05_KessaiData//決裁承認申請書.csv'
export_file_path = 'C:\\Users\\0425\\01_work\\01_Python\\01_Project//export'

#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【マスターファイル読み込み】
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
print('======================= マスターファイル 読み込み =================================')
#★★★★★★★★　マスターファイルが無い場合csv読み込みへ
def ReadMasterFile(File_path):
    if os.path.exists(master_file_path):
        return pd.read_csv(master_file_path, encoding="cp932",index_col=0)
        #print(df_Master)
    #else:
        #★★★★★CSV読み込みへ
        #★★★★★CSV読み込みへ

df_Master = ReadMasterFile(master_file_path)
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【新規登録データ作成】
# 既存データ除去、分納対応
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
print('======================= CSV 読み込み =================================')
df_AppendData = pd.read_csv(import_file_path, encoding="cp932",index_col=0)
print(df_AppendData)
print('======================= DFの比較 新規のみ残す=================================')
if os.path.exists(master_file_path):
    df = pd.merge(df_AppendData,df_Master, on=['自動連番'], how='outer', indicator=True)
    df_AppendData = df_AppendData[df['_merge'] == 'left_only']
    print(df_AppendData)
#'''
lst_split = []
colm_split = ['分納②','分納③','分納④','分納⑤','分納⑥','分納⑦','分納⑧']
for num_df in df_AppendData.index:
    if df_AppendData.loc[num_df,'分割orNot'] != 'Not':
       #▽▲▽▲▽▲▽▲▽▲ 分納処理 ▽▲▽▲▽▲▽▲▽▲ 
       lst_split.append(df_AppendData.loc[num_df,'分納①'])
       for num_split in range(int(df_AppendData.loc[num_df,'分割orNot'])-1):
           #▽▲▽▲▽▲▽▲▽▲ 分納行を追加 ▽▲▽▲▽▲▽▲▽▲
           lst_split.append(df_AppendData.loc[num_df][colm_split[num_split]])
           df_AppendData.loc[num_df+'_'+colm_split[num_split]] = ''           
    else:
        lst_split.append('')
df_AppendData = df_AppendData.sort_index()
df_AppendData['分割金額'] = lst_split
print('======================= 加工ファイル =================================')
print(df_AppendData)
print(lst_split)
if os.path.exists(master_file_path) == False:
    df_AppendData.to_csv(master_file_path, encoding="cp932")


#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
# SQLite管理へ
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
conn = sqlite3.connect((export_file_path+'//'+'決裁承認.db'))
cur = conn.cursor()

df_AppendData.to_sql('sample', conn, if_exists='replace')

cur.close()
conn.close()
