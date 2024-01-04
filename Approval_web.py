import streamlit as st  #pip install streamlit
import pandas  as pd
import os
import datetime
import calendar
# from Approval_Datamake import ReadMasterFile

#master_file_path = 'C:\\Users\\0425\\01_work\\01_Python\\02_data\\05_KessaiData//master.csv'
#master_file_path = '\\\\nfs01\\all\\管理本部\\新決裁承認申請（仮）//master.csv'
master_file_path = 'master.csv'

flg_master_exist = False
lst_Section = ['全て']
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【関数定義】
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【新規登録データ作成】
# 既存データ除去、分納対応
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
def AppendData(import_file_path):
    df_AppendData = pd.read_csv(import_file_path, encoding="cp932",index_col=0)
    if os.path.exists(master_file_path):
        df_Master = pd.read_csv(master_file_path, encoding="cp932",index_col=0)
        df = pd.merge(df_AppendData,df_Master, on=['自動連番'], how='outer', indicator=True)
        df_AppendData = df_AppendData[df['_merge'] == 'left_only']
    df_AppendData = df_AppendData.sort_index()
    lst_split = []
    lst_split.clear()
    colm_split = ['分納②','分納③','分納④','分納⑤','分納⑥','分納⑦','分納⑧']
    for num_df in df_AppendData.index:
        if df_AppendData.loc[num_df,'分割orNot'] != 'Not':
            #▽▲▽▲▽▲▽▲▽▲ 分納処理 ▽▲▽▲▽▲▽▲▽▲ 
            lst_split.append(df_AppendData.loc[num_df,'分納①'])
            for num_split in range(int(df_AppendData.loc[num_df,'分割orNot'])-1):
                #▽▲▽▲▽▲▽▲▽▲ 分納行を追加 ▽▲▽▲▽▲▽▲▽▲
                lst_split.append(df_AppendData.loc[num_df][colm_split[num_split]])
                #df_AppendData.loc[num_df+'_'+colm_split[num_split]] = ''
                df_AppendData.loc[num_df+'_'+colm_split[num_split]] = df_AppendData.loc[num_df]           
        else:
            lst_split.append('')
    df_AppendData = df_AppendData.sort_index()
    df_AppendData['分割金額'] = lst_split
    if os.path.exists(master_file_path) == False:
        df_AppendData.to_csv(master_file_path, encoding="cp932")
    else:
        df_AppendData.to_csv(master_file_path,mode='a', header=False , encoding="cp932")

    df_Master = pd.read_csv(master_file_path, encoding="cp932",index_col=0)
    lst_Section = df_Master['申請者所属組織'].unique().tolist()
    lst_Section.append('全て')
    flg_master_exist = True
    return len(df_AppendData)
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【マスターデータ読み込み】
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
if os.path.exists(master_file_path):
    df_Master = pd.read_csv(master_file_path, encoding="cp932",index_col=0)
    lst_Section = df_Master['申請者所属組織'].unique().tolist()
    lst_Section.append('全て')
    flg_master_exist = True
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【ブラウザ画面作成】
# 絞り込み、ファイル読み込み、決裁承認リスト
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
st.set_page_config(layout='wide')
st.title('請求書管理')
TextHorder = st.empty()
TextHorder_Side = st.empty()
btn_Fin = st.button('請求書確定をデータベースに反映')

#--------------------------------------------
# サイドバー
#--------------------------------------------
with st.sidebar:
    #---絞り込み
    with st.form(key='Refine_foram'):
        st.subheader('絞り込み')
        Cnt = len(lst_Section) - 1
        box_Section = st.selectbox('部署',lst_Section,index = Cnt)
        _ = '''
        col1,col2 = st.columns(2)
        with col1:
            box_SeasonStart = st.date_input('申請日[start]',datetime.date.today() - datetime.timedelta(days=30))
        with col2:
            box_SeasonEnd = st.date_input('申請日[end]')
        btn_Seasonoff = st.checkbox('申請日を有効にする')
        '''
        col1,col2 = st.columns(2)
        dt = datetime.date.today()
        dt_st = dt.replace(day=1)
        dt_end = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
        with col1:
            box_BillStart = st.date_input('請求確定[start]',dt_st)
        with col2:
            box_BillEnd = st.date_input('請求確定[end]',dt_end)        
        btn_Billon = st.checkbox('請求書確定日を有効にする')
        btn_bill = st.checkbox('請求書未処理を表示しない')
        btn_Refine = st.form_submit_button('反映')
        if btn_Refine:
            #表示データの絞り込み
            TextHorder_Side.write('【Side_Info】表示データ絞り込み条件適用')
            #df_Dsp = df_Dsp[df_Dsp['申請者所属組織']== box_Section]
    #---CSV読み込み
    with st.form(key='Append_form'):
        st.subheader('データ更新＠システム管理者')
        file = st.file_uploader('選択したCSVファイルの新規分をデータベースに追加します', type="CSV")
        btn_Uplode_OK = st.form_submit_button('データ更新')
        Cnt=0
        if file is not None:
            print('★★★★★★★★★★★★★★★★★★')
            print(file)
            Cnt = AppendData(file)
        if btn_Uplode_OK:
            TextHorder_Side.write('【Side_Info】'+str(Cnt) + '件のデータを追加しました')
#--------------------------------------------
# メイン
#--------------------------------------------
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
# 決裁承認リスト表示、請求書確定入力
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
if flg_master_exist:
    TextHorder.write('【Main_Info】請求書処理日付の入力をお願いします（右端以外のセルは編集しないで～）')
    df_Dsp = df_Master[['申請日',
                        '申請者所属組織',
                        '申請者',
                        '申請事項',
                        '発注先',
                        '合計(税抜)',
                        '分割金額',
                        '確定処理済(請求書処理済)']]
    df_Dsp['確定処理済(請求書処理済)'] = pd.to_datetime(df_Dsp['確定処理済(請求書処理済)'], format='%Y/%m/%d')
    #---------------絞り込み適用
    if box_Section != '全て':
        df_Dsp = df_Dsp[df_Dsp['申請者所属組織'] == box_Section]
    if btn_Billon:
        time_st = datetime.datetime(box_BillStart.year,box_BillStart.month,box_BillStart.day,12,00,00)
        time_ed = datetime.datetime(box_BillEnd.year,box_BillEnd.month,box_BillEnd.day,12,00,00)
        print(time_st)
        print(time_ed)
        df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] >= time_st) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
        df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] <= time_ed) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
    if btn_bill:
        #----------None判定
        df_Dsp = df_Dsp[df_Dsp['確定処理済(請求書処理済)'].isnull() == False]
    st.subheader('決裁承認申請書リスト')
    st.data_editor(df_Dsp,key='Change_data')
    if btn_Fin:
        TextHorder.write('データベース更新中')
        #変更箇所の反映
        Change_Rows = st.session_state['Change_data']
        lst_Index =[]
        lst_Date = []
        lst_Index.clear()
        lst_Date.clear()
        for ed_r, ed_d in Change_Rows['edited_rows'].items():
            lst_Index.append(df_Dsp.index[ed_r])
            lst_Date.append(ed_d['確定処理済(請求書処理済)'])
        df_Master.loc[lst_Index,'確定処理済(請求書処理済)'] = lst_Date
        df_Master.to_csv(master_file_path, encoding="cp932")
        TextHorder.write('【Main_Info】'+ str(len(lst_Date)) + '件の請求書を確定しました')
    st.text(str(len(df_Dsp)) + ' Data')
    st.text('金額合計：¥' + str(format(df_Dsp['合計(税抜)'].sum(),',')) + '（税抜き）')

else:
    TextHorder.write('【Main_Info】データの登録がありません')