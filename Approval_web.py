import streamlit as st  #pip install streamlit
import pandas  as pd
import os
import datetime
import calendar
# from Approval_Datamake import ReadMasterFile

master_file_path = 'C:\\Users\\0425\\01_work\\01_Python\\02_data\\05_KessaiData//master.csv'
#master_file_path = '\\\\nfs01\\all\\管理本部\\新決裁承認申請（仮）//master.csv'
#master_file_path = 'master.csv'

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
    if import_file_path is not None:
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
            df_AppendData.to_csv(master_file_path, encoding="cp932") #新規マスターファイル作成
        else:
            df_AppendData.to_csv(master_file_path,mode='a', header=False , encoding="cp932") #マスターファイルに追記

        df_Master = pd.read_csv(master_file_path, encoding="cp932",index_col=0)
        return len(df_AppendData),df_Master
    else:
        return 0,''
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【コールバック関数】
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
def callback_billset():
    print('----------------------コールバックテスト～請求書情報確定---------------------')
    print('')
    print('---------------------------------------------------------------------')
def callback_billedit():
    print('----------------------コールバックテスト～請求書情報編集---------------------')
    print('')
    print('---------------------------------------------------------------------')
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【マスターデータ読み込み】
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
if os.path.exists(master_file_path):
    print('---------------------read')
    df_Master = pd.read_csv(master_file_path, encoding="cp932",index_col=0)
    lst_Section = df_Master['申請者所属組織'].unique().tolist()
    lst_Section.append('全て')
    flg_master_exist = True
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
#【ブラウザ画面作成】
# 絞り込み、ファイル読み込み、決裁承認リスト
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
st.set_page_config(page_title='請求書管理',layout='wide')
st.title('請求書管理')
TextHorder = st.text('【Main_Info】')
TextHorder_Side = st.text('【Side_Info】')

#--------------------------------------------
# サイドバー
#--------------------------------------------
with st.sidebar:
    #---CSV読み込み
    with st.form(key='Append_form'):
        st.subheader('データ更新＠システム管理者')
        file = st.file_uploader('選択したCSVファイルの新規分をデータベースに追加します', type="CSV")
        if st.form_submit_button('データ更新'):
            result = AppendData(file)
            TextHorder_Side.write('【Side_Info】'+str(result[0]) + '件のデータを追加しました')
            if result[0]:
                df_Master = result[1]
                flg_master_exist = True
                print('--------------------------dats set')
                lst_Section = df_Master['申請者所属組織'].unique().tolist()
                lst_Section.append('全て')
    #---絞り込み
    with st.form(key='Refine_foram'):
        print('================== RefineMenu Set')
        st.subheader('絞り込み')
        Cnt = len(lst_Section) - 1
        box_Section = st.selectbox('部署',lst_Section,index = Cnt)
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
#--------------------------------------------
# メイン
#--------------------------------------------
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
# 決裁承認リスト表示、請求書確定入力
#◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇
__ = '''
# デバッグ用の処理
print('--------------------------main run')
if flg_master_exist:
    print('--------------------------data reroad')
    TextHorder.write('【Main_Info】請求書処理日付の入力をお願いします（右端以外のセルは編集しないで～）')
    df_Dsp = df_Master[['申請日',
                        '申請者所属組織',
                        '申請者',
                        '申請事項',
                        '発注先',
                        '合計(税抜)',
                        '分割金額',
                        '確定処理済(請求書処理済)']].copy()
    df_Dsp['確定処理済(請求書処理済)'] = pd.to_datetime(df_Master['確定処理済(請求書処理済)'])
    #---------------絞り込み適用
    if box_Section != '全て':
        df_Dsp = df_Dsp[df_Dsp['申請者所属組織'] == box_Section]
    if btn_Billon:
        time_st = datetime.datetime(box_BillStart.year,box_BillStart.month,box_BillStart.day,12,00,00)
        time_ed = datetime.datetime(box_BillEnd.year,box_BillEnd.month,box_BillEnd.day,12,00,00)
        df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] >= time_st) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
        df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] <= time_ed) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
    if btn_bill:
        #----------None判定
        df_Dsp = df_Dsp[df_Dsp['確定処理済(請求書処理済)'].isnull() == False]
    st.subheader('決裁承認申請書リスト')
    print('--------------------------Set_Data_Editor')
    btn_Fin = st.button('請求書確定をデータベースに反映',on_click = callback_billset)
    ed_data = st.data_editor(df_Dsp,
                                key='Change_data',
                                disabled=['自動連番','申請日','申請者所属組織','申請者','申請事項','発注先','合計(税抜)','分割金額'])
                                #use_container_width=True)
                                #on_change = callback_billedit)
    Change_Rows = st.session_state.Change_data
    st.write(st.session_state['Change_data'])
    if btn_Fin:
        print(Change_Rows)
        TextHorder.write('データベース更新中')
        #変更箇所の反映
        lst_Index =[]
        lst_Date = []
        lst_Index.clear()
        lst_Date.clear()
        for ed_r, ed_d in Change_Rows['edited_rows'].items():
            lst_Index.append(df_Dsp.index[ed_r])
            lst_Date.append(ed_d['確定処理済(請求書処理済)'])
        print('o----------------------------o')
        print(lst_Date)
        print(lst_Index)
        print('◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆')
        print(flg_master_exist)
        df_Master.loc[lst_Index,'確定処理済(請求書処理済)'] = lst_Date
        df_Master.to_csv(master_file_path, encoding="cp932")
        TextHorder.write('【Main_Info】'+ str(len(lst_Date)) + '件の請求書確定情報を更新しました')
        #■■■■■■■■■■■■■■■■■2回に1度しか更新されない不具合を以下で強引に対応してみる
        st.session_state['key'] = 'value2'
        #st.session_state['key'] = 'value2'
    st.text(str(len(df_Dsp)) + ' Data')
    st.text('金額合計：¥' + str(format(df_Dsp['合計(税抜)'].sum(),',')) + '（税抜き）')

else:
    TextHorder.write('【Main_Info】データの登録がありません')
'''

with st.form(key='form_main'):
    print('--------------------------main run')
    if flg_master_exist:
        print('--------------------------data reroad')
        TextHorder.write('【Main_Info】請求書処理日付の入力をお願いします（右端以外のセルは編集しないで～）')
        df_Dsp = df_Master[['申請日',
                            '申請者所属組織',
                            '申請者',
                            '申請事項',
                            '発注先',
                            '合計(税抜)',
                            '分割金額',
                            '確定処理済(請求書処理済)']].copy()
        df_Dsp['確定処理済(請求書処理済)'] = pd.to_datetime(df_Master['確定処理済(請求書処理済)'])
        #---------------絞り込み適用
        if box_Section != '全て':
            df_Dsp = df_Dsp[df_Dsp['申請者所属組織'] == box_Section]
        if btn_Billon:
            time_st = datetime.datetime(box_BillStart.year,box_BillStart.month,box_BillStart.day,12,00,00)
            time_ed = datetime.datetime(box_BillEnd.year,box_BillEnd.month,box_BillEnd.day,12,00,00)
            df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] >= time_st) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
            df_Dsp = df_Dsp[(df_Dsp['確定処理済(請求書処理済)'] <= time_ed) | df_Dsp['確定処理済(請求書処理済)'].isnull()]
        if btn_bill:
            #----------None判定
            df_Dsp = df_Dsp[df_Dsp['確定処理済(請求書処理済)'].isnull() == False]
        st.subheader('決裁承認申請書リスト')
        print('--------------------------Set_Data_Editor')
        col1,col2 = st.columns([2, 3])
        with col1:
            btn_Fin = st.form_submit_button('請求書確定をデータベースに反映',on_click = callback_billset)
        with col2:
            btn_Refresh = st.form_submit_button('【仮】続けてデータ入力する場合ここを1回押してください')
        ed_data = st.data_editor(df_Dsp,
                                 key='Change_data',
                                 disabled=['自動連番','申請日','申請者所属組織','申請者','申請事項','発注先','合計(税抜)','分割金額'])
                                 #use_container_width=True)
                                 #on_change = callback_billedit)
        Change_Rows = st.session_state.Change_data
        #st.write(st.session_state['Change_data'])
        if btn_Fin:
            print(Change_Rows)
            TextHorder.write('データベース更新中')
            #変更箇所の反映
            lst_Index =[]
            lst_Date = []
            lst_Index.clear()
            lst_Date.clear()
            for ed_r, ed_d in Change_Rows['edited_rows'].items():
                lst_Index.append(df_Dsp.index[ed_r])
                lst_Date.append(ed_d['確定処理済(請求書処理済)'])
            print('o----------------------------o')
            print(lst_Date)
            print(lst_Index)
            print('◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆')
            print(flg_master_exist)
            df_Master.loc[lst_Index,'確定処理済(請求書処理済)'] = lst_Date
            df_Master.to_csv(master_file_path, encoding="cp932")
            TextHorder.write('【Main_Info】'+ str(len(lst_Date)) + '件の請求書確定情報を更新しました')
            #■■■■■■■■■■■■■■■■■2回に1度しか更新されない不具合を以下で強引に対応してみる
        st.text(str(len(df_Dsp)) + ' Data')
        st.text('金額合計：¥' + str(format(df_Dsp['合計(税抜)'].sum(),',')) + '（税抜き）')

    else:
        TextHorder.write('【Main_Info】データの登録がありません')
_ = '''
バグや改善点など

▼バグ

・サイドバー更新を2回押さないとリストが更新されない → 【解決】df_Masterが関数内のみで定義されていた為、返値として再指定

・請求書確定入力消える、規則正しく2回に1回消える・・・

▼今後の改善点、注意点

・請求書確定日選択の時に時間まで出てしまうのを消す

・Pythonのみで管理している為将来的に動作が重たくなる心配アリ。データベース部はSQLに置き換える。

・セキュリティは今時点ノーガード、周辺で固めるか別のwebアップ方法を考える、まずはユーザーIDとPassword対応

・個人単位で前回設定が引き継がれるようにする

・見た目のケアはしてないので、環境によっては操作し辛い、スマフォ対応も行う

・取り合えず最小限、最速で組める範囲で作成している為、使ってもらって色々な問題や要望に対応する

・変更日、変更者もシステム管理者用情報として記録に残す

・分納行、確定行を色分けして見やすくする

・データのバックアップ、イレギュラー操作への対応

・画面を広く使える様、上部のstreamlit情報領域を消す

・決裁初認リストの請求書確定以外は編集不可にする

▼warning

・df_AppendData = df_AppendData[df['_merge'] == 'left_only']

・df_Dsp['確定処理済(請求書処理済)'] = pd.to_datetime(df_Dsp['確定処理済(請求書処理済)']) → 【解決】:df_dspが「参照」なのか「コピー」なのか不明、copy()で明示

'''