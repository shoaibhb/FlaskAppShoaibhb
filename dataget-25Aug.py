from csv import reader
from xlrd import open_workbook, xldate_as_tuple

import xlrd
from xlrd.timemachine import xrange

from datetime import datetime
from flask_login import login_required, current_user


from . import db, create_app
import os

from .models import Tbl_pm

# ************ Source Checking  **************

import pandas as pd
import numpy as np


# ************ End Source Checking *************
# ******** Train Availability NEW
def get_data_availability(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='M:O, P:R, S:U, W:Y, Z:AB, AC:AE',
                         skiprows=range(3), nrows=1)
    df = pd.DataFrame(data)
    df = df.round().astype(int)
    availtsl = df.values.flatten().tolist()
    # print(availtsl[16])

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='M, P, S, W, Z, AC', skiprows=range(4),nrows=1)
    df=pd.DataFrame(data)
    df=df.round().astype(int)
    availts = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='N:Q', skiprows=range(8), nrows=3)
    df = pd.DataFrame(data)
    # df = df.round().astype(int)
    mtustatus = df.values.flatten().tolist()


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A:I', skiprows=range(2),nrows=69)
    df=pd.DataFrame(data)

    # ******* Get PM date from Database **********

    a=[]
    for x in range(401, 425):
        pm2 = db.session.query(Tbl_pm).filter_by(pm_train=x).order_by(Tbl_pm.pm_id.desc()).first()
        a.append(pm2.pm_date)
    for x in range(501, 520):
        pm2 = db.session.query(Tbl_pm).filter_by(pm_train=x).order_by(Tbl_pm.pm_id.desc()).first()
        a.append(pm2.pm_date)
    for x in range(601, 627):
        pm2 = db.session.query(Tbl_pm).filter_by(pm_train=x).order_by(Tbl_pm.pm_id.desc()).first()
        a.append(pm2.pm_date)
    df.drop(df.columns[6], inplace=True, axis=1)
    df.insert(6,"6",a)

    # ********* END PM Date ***********
    # print(df)
    df[3]=df[3].astype(int).apply('{:,}'.format)
    df[4] = df[4].astype(int).apply('{:,}'.format)

    df4=df.loc[(df[1] == 'OK') | (df[2] == 'MU')]
    df4=df4[df[0].str.contains(r'TS4(?!$)')]
    drop_values = ['POK', 'NOK']
    df4 =df4[~df4[1].isin(drop_values)]
    tslistok4 = df4.values.tolist()

    # if len(tslistok4)==0:
    #     tslistok4=["None"]

    # df5 = df.loc[df[1] == 'OK']
    df5 = df.loc[(df[1] == 'OK') | (df[2] == 'MU')]
    df5 = df5[df[0].str.contains(r'TS5(?!$)')]
    df5 = df5[~df5[1].isin(drop_values)]
    tslistok5 = df5.values.tolist()
    # print(df5)
    # tslistok5 = df5[0].values.flatten().tolist()
    # if len(tslistok5)==0:
    #     tslistok5=["None"]

    # df6 = df.loc[df[1] == 'OK']
    df6 = df.loc[(df[1] == 'OK') | (df[2] == 'MU')]
    df6 = df6[df[0].str.contains(r'TS6(?!$)')]
    df6 = df6[~df6[1].isin(drop_values)]
    tslistok6 = df6.values.tolist()
    # print(df6)
    # tslistok6 = df6[0].values.flatten().tolist()
    # if len(tslistok6)==0:
    #     tslistok6=["None"]


    # df4 = df.loc[df[1] == 'POK']
    df4 = df.loc[(df[1] == 'POK')|(df[2] == 'MU')]
    df4 = df4[df[0].str.contains(r'TS4(?!$)')]
    # print(df4)
    drop_values = ['OK', 'NOK']
    df4 =df4[~df4[1].isin(drop_values)]
    tslistpok4 = df4.values.tolist()
    # tslistpok4 = df4[0].values.flatten().tolist()
    # if len(tslistpok4) == 0:
    #     tslistpok4 = ["None"]

    df5 = df.loc[(df[1] == 'POK')|(df[2] == 'MU')]
    df5 = df5[df[0].str.contains(r'TS5(?!$)')]
    df5 = df5[~df5[1].isin(drop_values)]
    # print(df5)
    tslistpok5 = df5.values.tolist()
    # print (df5)
    # tslistpok5 = df5[0].values.flatten().tolist()
    # if len(tslistpok5) == 0:
    #     tslistpok5 = ["None"]

    df6 = df.loc[(df[1] == 'POK')|(df[2] == 'MU')]
    df6 = df6[df[0].str.contains(r'TS6(?!$)')]
    df6 = df6[~df6[1].isin(drop_values)]
    tslistpok6 = df6.values.tolist()
    # tslistpok6 = df6[0].values.flatten().tolist()
    # if len(tslistpok6) == 0:
    #     tslistpok6 = ["None"]


    df4 = df.loc[(df[1] == 'NOK')|(df[2] == 'MU')]
    df4 = df4[df[0].str.contains(r'TS4(?!$)')]
    drop_values = ['POK', 'OK']
    df4 = df4[~df4[1].isin(drop_values)]
    tslistnok4 = df4.values.tolist()
    # tslistnok4 = df4[0].values.flatten().tolist()
    # if len(tslistnok4) == 0:
    #     tslistnok4 = ["None"]

    df5 = df.loc[(df[1] == 'NOK')|(df[2] == 'MU')]
    df5 = df5[df[0].str.contains(r'TS5(?!$)')]
    df5 = df5[~df5[1].isin(drop_values)]
    tslistnok5 = df5.values.tolist()
    # tslistnok5 = df5[0].values.flatten().tolist()
    # if len(tslistnok5) == 0:
    #     tslistnok5 = ["None"]

    df6 = df.loc[(df[1] == 'NOK')|(df[2] == 'MU')]
    # df6 = df.loc[df[1] == 'NOK']
    df6 = df6[df[0].str.contains(r'TS6(?!$)')]
    df6 = df6[~df6[1].isin(drop_values)]
    tslistnok6 = df6.values.tolist()
    # tslistnok6 = df6[0].values.flatten().tolist()
    # if len(tslistnok6) == 0:
    #     tslistnok6 = ["None"]

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='N, P, Q, R', skiprows=range(8), nrows=3)
    df = pd.DataFrame(data)
    mtustatus = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A:G', skiprows=range(74))
    df = pd.DataFrame(data)
    mtustatus2 = df.values.tolist()
    

    # USER LOGIN Details write in excel
    ctime = datetime.now()
    cdate = datetime.now()

    ctime= ctime.strftime("%I:%M" ' %p')
    cdate = cdate.strftime("%d-%b-%Y")

    try:
        df = pd.DataFrame({"Name": [current_user.name], "Date": [cdate], "Time": [ctime]})
        append_df_to_excel(df, "loginhistory.xlsx")
    except Exception:
        pass


    del df
    return (availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6,
            tslistnok4, tslistnok5, tslistnok6, mtustatus, mtustatus2)


def append_df_to_excel(df, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)

# ******** Train Availability KPI
def get_data_avakpi(sh_name, file_name, path='./data/rst_files_repo/'):

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='Z', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df['Datex'] = pd.to_datetime(df['Datex']).dt.strftime('%d-%b-%Y')
    kpil4date = df.values.tolist()
    kpil4date=list(map(lambda el:[el], kpil4date))
    udate = kpil4date[-1]
    # print (len(kpil4date))

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AA', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l4ava = df.values.tolist()
    # print (len(l4ava))

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AB', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l4target = df.values.tolist()
    # print (kpil4)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AC', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l4total = df.values.tolist()


    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AI', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l6ava = df.values.tolist()
    # print (len(l4ava))

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AJ', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l6target = df.values.tolist()
    # print (kpil4)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AK', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l6total = df.values.tolist()




    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AE', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l5ava = df.values.tolist()
    # print (len(l4ava))

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AF', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l5target = df.values.tolist()
    # print (kpil4)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AG', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    df = df.round().astype(int)
    l5total = df.values.tolist()


    return (kpil4date, l4ava, l4target, l4total, l6ava, l6target, l6total, l5ava, l5target, l5total, udate)


# ******** Configuration Line 4 data from Excel file
def get_data_configl4(sh_name, file_name, path='./data/rst_files_repo/'):
    # data = pd.read_excel(path+file_name,sheet_name=sh_name,header=0, usecols = 'B:B', converters={'Mileage': int})
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='B:B', skiprows=range(2),nrows=24)
    # df=pd.DataFrame(data)
    # df=df.round().astype(int)
    # tml4=df.values.tolist()

    # Checking Mileage sorting
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,B,C,E', skiprows=range(2),nrows=24)
    df=pd.DataFrame(data)
    df[1]=df[1].round().astype(int)
    df[2] = df[2].round().astype(int)
    df=df.sort_values([1], ascending=True)
    tml4=df[1].values.tolist()
    tmid=df[0].values.tolist()
    tsl4=df[[4]].values.tolist()
    pol4 =df[[2]].values.tolist()

    # End Mileage sorting

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='C:C', skiprows=range(2),nrows=24)
    # df=pd.DataFrame(data)
    # df=df.round().astype(int)
    # pol4=df.values.tolist()


    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='E:E', skiprows=range(2),nrows=24)
    # df = pd.DataFrame(data)
    # tsl4 = df.values.tolist()
    # print (tsl4)

    dic = {'POK':'0', 'OK':'', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl4pok = [dic.get(n, n) for n in np.concatenate(tsl4)]
    # tslpok=np.reshape(tslpok, [-1, 1]).tolist()
    dic = {'POK':'', 'OK':'0', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl4ok = [dic.get(n, n) for n in np.concatenate(tsl4)]

    dic = {'POK':'', 'OK':'', 'NOK': '0'}  # for replace item in list, specify more changes here
    tsl4nok = [dic.get(n, n) for n in np.concatenate(tsl4)]

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(2), nrows=24)
    df = pd.DataFrame(data)
    swl4= df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='H,J,L,N,P,R,T,V,X,Z', skiprows=range(2), nrows=24)
    df = pd.DataFrame(data)
    df=df.replace("BASELINE", "badge badge-success")
    df = df.replace("RESTRICTED", "badge badge-warning")
    df = df.replace("NOT OK", "badge badge-danger")
    swsl4= df.values.tolist()


    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,C', skiprows=range(2), nrows=24)
    # df = pd.DataFrame(data)
    # # df= df.apply (pd.to_numeric, errors='coerce')
    # df= df.dropna()
    # df = df.reset_index(drop=True) #drop NaN from the list
    # df = df.apply(lambda x: x.astype(str).str.upper())
    # issuel4= df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AE', skiprows=range(1), nrows=7)
    df = pd.DataFrame(data)
    df = df.round(1)
    statusl4 = df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(25), nrows=1)
    df = pd.DataFrame(data)
    df = df.round(1)
    bll4 = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df
    return(tml4, pol4, tsl4pok, tsl4ok, tsl4nok, swl4, swsl4, statusl4, bll4, udate,tmid)


# ******** Configuration Line 5 data from Excel file
def get_data_configl5(sh_name, file_name, path='./data/rst_files_repo/'):
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='B:B', skiprows=range(2),nrows=19)
    # df=pd.DataFrame(data)
    # df=df.round().astype(int)
    # tml5=df.values.tolist()
    # print(tml5)

    # Checking Mileage sorting
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,B,C,E', skiprows=range(2),nrows=19)
    df=pd.DataFrame(data)
    df[1]=df[1].round().astype(int)
    df[2] = df[2].round().astype(int)
    df=df.sort_values([1], ascending=True)
    tml5=df[1].values.tolist()
    tmid=df[0].values.tolist()
    tsl5=df[[4]].values.tolist()
    pol5=df[2].values.tolist()

    # print(tsl4)
    # End Mileage sorting



    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='C:C', skiprows=range(2),nrows=19)
    # df=pd.DataFrame(data)
    # df=df.round().astype(int)
    # pol5=df.values.tolist()


    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='E:E', skiprows=range(2),nrows=19)
    # df = pd.DataFrame(data)
    # tsl5 = df.values.tolist()

    dic = {'POK':'0', 'OK':'', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl5pok = [dic.get(n, n) for n in np.concatenate(tsl5)]
    # tslpok=np.reshape(tslpok, [-1, 1]).tolist()
    dic = {'POK':'', 'OK':'0', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl5ok = [dic.get(n, n) for n in np.concatenate(tsl5)]

    dic = {'POK':'', 'OK':'', 'NOK': '0'}  # for replace item in list, specify more changes here
    tsl5nok = [dic.get(n, n) for n in np.concatenate(tsl5)]

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(2), nrows=19)
    df = pd.DataFrame(data)
    df = df.apply(lambda x: x.astype(str).str.upper())
    swl5= df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='H,J,L,N,P,R,T,V,X,Z', skiprows=range(2), nrows=19)
    df = pd.DataFrame(data)
    df=df.replace("BASELINE", "badge badge-success")
    df = df.replace("RESTRICTED", "badge badge-warning")
    df = df.replace("NOT OK", "badge badge-danger")
    swsl5= df.values.tolist()

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,C', skiprows=range(2), nrows=19)
    # df = pd.DataFrame(data)
    # # df= df.apply (pd.to_numeric, errors='coerce')
    # df= df.dropna()
    # df = df.reset_index(drop=True) #drop NaN from the list
    # issuel5= df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AE', skiprows=range(1), nrows=7)
    df = pd.DataFrame(data)
    df = df.round(1)
    statusl5 = df.values.tolist()
    # print(statusl5)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(20), nrows=1)
    df = pd.DataFrame(data)
    df = df.round(1)
    bll5 = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df
    return(tml5, pol5, tsl5pok, tsl5ok, tsl5nok, swl5, swsl5, statusl5, bll5, udate, tmid)


# ******** User Privilage data from Excel file
def get_data_user(sh_name, file_name, path='./data/rst_files_repo/'):
    import re
    data = pd.read_excel(path + file_name, sheet_name='user-access', header=None, usecols='A:H', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.dropna()
    # df[0] = df[0].round().astype(int)
    print(current_user.email)

    # ua = re.findall("\d+", str(current_user))[0]
    # print(re.findall("\d+", str(current_user.email)))
    # df1 = df[(df[0] == int(ua))]
    df1 = df[(df[1] == current_user.email)]
    up = df1.values.flatten().tolist()
    if not up:
        print(df)
        df1=df.loc[df[1] == current_user.name]
        up = df1.values.flatten().tolist()
    return (up)

# ******** Configuration Line 6.html data from Excel file
def get_data_configl6(sh_name, file_name, path='./data/rst_files_repo/'):


    # Checking Mileage sorting
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,B,C,E', skiprows=range(2),nrows=26)
    df=pd.DataFrame(data)
    df[1]=df[1].round().astype(int)
    df[2] = df[2].round().astype(int)
    df=df.sort_values([1], ascending=True)
    tml6=df[1].values.tolist()
    tmid=df[0].values.tolist()
    tsl6=df[[4]].values.tolist()
    pol6 =df[2].values.tolist()

    # End Mileage sorting

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='C:C', skiprows=range(2),nrows=26)
    # df=pd.DataFrame(data)
    # df=df.round().astype(int)
    # pol6=df.values.tolist()

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='E:E', skiprows=range(2), nrows=26)
    # df = pd.DataFrame(data)
    # tsl6 = df.values.tolist()

    dic = {'POK':'0', 'OK':'', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl6pok = [dic.get(n, n) for n in np.concatenate(tsl6)]
    # tslpok=np.reshape(tslpok, [-1, 1]).tolist()
    dic = {'POK':'', 'OK':'0', 'NOK': ''}  # for replace item in list, specify more changes here
    tsl6ok = [dic.get(n, n) for n in np.concatenate(tsl6)]

    dic = {'POK':'', 'OK':'', 'NOK': '0'}  # for replace item in list, specify more changes here
    tsl6nok = [dic.get(n, n) for n in np.concatenate(tsl6)]

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(2), nrows=26)
    df = pd.DataFrame(data)
    df = df.apply(lambda x: x.astype(str).str.upper())
    swl6= df.values.tolist()
    # print(swl6)


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='H,J,L,N,P,R,T,V,X,Z', skiprows=range(2), nrows=26)
    df = pd.DataFrame(data)
    df=df.replace("BASELINE", "badge badge-success")
    df = df.replace("RESTRICTED", "badge badge-warning")
    df = df.replace("NOT OK", "badge badge-danger")
    swsl6= df.values.tolist()

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A,C', skiprows=range(2), nrows=26)
    # df = pd.DataFrame(data)
    # # df= df.apply (pd.to_numeric, errors='coerce')
    # df= df.dropna()
    # df = df.reset_index(drop=True) #drop NaN from the list
    # issuel6= df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='AE', skiprows=range(1), nrows=7)
    df = pd.DataFrame(data)
    df = df.round(1)
    statusl6 = df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='G,I,K,M,O,Q,S,U,W,Y', skiprows=range(27), nrows=1)
    df = pd.DataFrame(data)
    df = df.round(1)
    bll6 = df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()
    # print(tml6date)

    del df

    return(tml6,pol6,tsl6pok,tsl6ok,tsl6nok,swl6,swsl6,statusl6,bll6,udate,tmid)

# ******** Retrofit
def get_data_retrofit(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:J', skiprows=range(1))
    df = pd.DataFrame(data)
    r_sum_list = df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df
    return (r_sum_list,udate)

# ******** Software upgrade History
def get_data_swh(sh_name, file_name, path='./data/rst_files_repo/'):

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:F', skiprows=range(2))
    df = pd.DataFrame(data)
    df['Validation date on-site'] = pd.to_datetime(df['Validation date on-site']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')
    swh = df.values.tolist()
    # print (df)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df

    return (swh, udate)

# ********* Corrective MAINTENANCE  Train Status****************
def get_data_cmts(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:G', skiprows=range(1))
    df = pd.DataFrame(data)
    df = df.fillna('')
    df = df.astype(str)
    df['Open Date'] = pd.to_datetime(df['Open Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    # print(df.dtypes)
    btstatus= []
    l4 = ["401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415", "416",
          "417", "418", "419", "420", "421", "422", "423", "424", "501", "502", "503", "504", "505", "506", "507", "508",
          "509", "510", "511", "512", "513", "514", "515", "516","517", "518", "519", "601", "602", "603", "604", "605",
          "606", "607", "608", "609", "610", "611", "612", "613", "614", "615", "616", "617", "618", "619", "620", "621",
          "622", "623", "624", "625", "626"]
    for x in l4:
        if len(df[(df.TRAIN == x) & (df.IMPACT.isin(['High']))]) > 0:
            btstatus.append("btn-danger")
            continue
        elif len(df[(df.TRAIN == x) & (df.IMPACT.isin(['Medium']))]) > 0:
            btstatus.append("btn-warning")
            continue
        else:
            btstatus.append("btn-success")
            continue

    # print(btstatus)

    cmtslist = df.values.tolist()
    lenlist = len(cmtslist)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df
    return(cmtslist, lenlist, btstatus, udate)


# ********* TIR (Train Issue Report)  ****************
def get_data_tir(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A,B,E,F,G,N,O,P,Q,U,V,W', skiprows=range(1))
    df = pd.DataFrame(data)

    df = df.sort_values(by='TIR Date', ascending=False)

    df['TIR Date'] = pd.to_datetime(df['TIR Date']).dt.strftime('%d-%b-%Y')
    # df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    df['Closure Date'] = pd.to_datetime(df['Closure Date']).dt.strftime('%d-%b-%Y')
    # df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    tirlist = df.values.tolist()
    # print(df)

    # lenlist=len(ncrlist)
    # del df
    #
    data = pd.read_excel(path + file_name, sheet_name='KPI', usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df=df.dropna()

    start_word1 = next(iter(df[df['V'] == 'TIR Impact'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1=df.loc[start_word1+1:end_word1-1 , :]
    lbltir= df1["V"].tolist()
    valtir= df1["W"].tolist()
    # # ncr_status = df1.values.flatten().tolist()
    # print(ncr_status)
    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'
    #
    #
    start_word2 = next(iter(df[df['V'] == 'Origin'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    lblclosure= df2["V"].tolist()
    valclosure= df2["W"].tolist()
    # ncr_res = df2.values.flatten().tolist()
    # print(ncr_res)
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(df)

    start_word3 = next(iter(df[df['V'] == 'TIR status'].index), 'no match')
    end_word3 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df3 = df.loc[start_word3 + 1:end_word3 - 1, :]
    lblpic= df3["V"].tolist()
    valpic= df3["W"].tolist()
    # ncr_sub = df3.values.tolist()
    # print(ncr_sub)
    df.at[end_word3:end_word3, 'V'] = 'Grand TotalXxx'
    # print(df)


    start_word4 = next(iter(df[df['V'] == 'SAF'].index), 'no match')
    end_word4 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df4 = df.loc[start_word4 + 1:end_word4 - 1, :]
    lblorigin= df4["V"].tolist()
    valorigin= df4["W"].tolist()
    # ncr_sub = df3.values.tolist()
    # print(ncr_sub)
    df.at[end_word4:end_word4, 'V'] = 'Grand TotalXxx'
    # print(df)

    start_word5 = next(iter(df[df['V'] == 'TIR PIC'].index), 'no match')
    end_word5 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df5 = df.loc[start_word5 + 1:end_word5 - 1, :]
    df5 = df5.drop(df5[df5.W == 0].index)
    lblpicx = df5["V"].tolist()
    valpicx = df5["W"].tolist()
    # ncr_sub = df3.values.tolist()
    lblpicx=[x.split()[0] for x in lblpicx]
    # print([x.split()[-1] for x in lblpicx])
    # print(ncr_sub)
    df.at[end_word5:end_word5, 'V'] = 'Grand TotalXxx'
    # print(df5)



    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    return (tirlist, lbltir, valtir, lblorigin, valorigin, lblpic, valpic, lblclosure, valclosure, lblpicx, valpicx, udate)


# ********* PREVENTIVE MAINTENANCE  ****************
def get_data_pm(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:Z', skiprows=range(1),nrows=2)
    df=pd.DataFrame(data)
    pm2week=df.values.tolist()
    # print(pm2week)
    del df


    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:L', skiprows=range(4), nrows=2)
    df = pd.DataFrame(data)
    pmmonth = df.values.tolist()
    # pmmonth = df.values.flatten().tolist()
    # print(pmmonth)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:F', skiprows=range(7), nrows=2)
    df = pd.DataFrame(data)
    pm2month = df.values.tolist()
    # print(pm2month)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:D', skiprows=range(10), nrows=2)
    df = pd.DataFrame(data)
    pmquart = df.values.tolist()

    # ***** Tab Data *****
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:K', skiprows=range(15))
    df=pd.DataFrame(data)
    df = df.sort_values(by='Date', ascending=False)
    df=df.apply(lambda s: s.fillna({i: [] for i in df.index}))
    df['Date']=df['Date'].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))

    pm401=df.loc[df['TS'] == 401]
    pm401=pm401.values.tolist()

    pm402=df.loc[df['TS'] == 402]
    pm402=pm402.values.tolist()

    pm403=df.loc[df['TS'] == 403]
    pm403=pm403.values.tolist()

    pm404=df.loc[df['TS'] == 404]
    pm404=pm404.values.tolist()

    pm405=df.loc[df['TS'] == 405]
    pm405=pm405.values.tolist()

    pm406=df.loc[df['TS'] == 406]
    pm406=pm406.values.tolist()

    pm407=df.loc[df['TS'] == 407]
    pm407=pm407.values.tolist()

    pm408=df.loc[df['TS'] == 408]
    pm408=pm408.values.tolist()

    pm409=df.loc[df['TS'] == 409]
    pm409=pm409.values.tolist()

    pm410=df.loc[df['TS'] == 410]
    pm410=pm410.values.tolist()

    pm411=df.loc[df['TS'] == 411]
    pm411=pm411.values.tolist()

    pm412=df.loc[df['TS'] == 412]
    pm412=pm412.values.tolist()

    pm413=df.loc[df['TS'] == 413]
    pm413=pm413.values.tolist()

    pm414=df.loc[df['TS'] == 414]
    pm414=pm414.values.tolist()

    pm415=df.loc[df['TS'] == 415]
    pm415=pm415.values.tolist()

    pm416=df.loc[df['TS'] == 416]
    pm416=pm416.values.tolist()

    pm417=df.loc[df['TS'] == 417]
    pm417=pm417.values.tolist()

    pm418=df.loc[df['TS'] == 418]
    pm418=pm418.values.tolist()

    pm419=df.loc[df['TS'] == 419]
    pm419=pm419.values.tolist()

    pm420=df.loc[df['TS'] == 420]
    pm420=pm420.values.tolist()

    pm421=df.loc[df['TS'] == 421]
    pm421=pm421.values.tolist()

    pm422=df.loc[df['TS'] == 422]
    pm422=pm422.values.tolist()

    pm423=df.loc[df['TS'] == 423]
    pm423=pm423.values.tolist()

    pm424=df.loc[df['TS'] == 424]
    pm424=pm424.values.tolist()

    pm501 = df.loc[df['TS'] == 501]
    pm501 = pm501.values.tolist()
    pm502 = df.loc[df['TS'] == 502]
    pm502 = pm502.values.tolist()
    pm503 = df.loc[df['TS'] == 503]
    pm503 = pm503.values.tolist()
    pm504 = df.loc[df['TS'] == 504]
    pm504 = pm504.values.tolist()
    pm505 = df.loc[df['TS'] == 505]
    pm505 = pm505.values.tolist()
    pm506 = df.loc[df['TS'] == 506]
    pm506 = pm506.values.tolist()
    pm507 = df.loc[df['TS'] == 507]
    pm507 = pm507.values.tolist()
    pm508 = df.loc[df['TS'] == 508]
    pm508 = pm508.values.tolist()
    pm509 = df.loc[df['TS'] == 509]
    pm509 = pm509.values.tolist()
    pm510 = df.loc[df['TS'] == 510]
    pm510 = pm510.values.tolist()
    pm511 = df.loc[df['TS'] == 511]
    pm511 = pm511.values.tolist()
    pm512 = df.loc[df['TS'] == 512]
    pm512 = pm512.values.tolist()
    pm513 = df.loc[df['TS'] == 513]
    pm513 = pm513.values.tolist()
    pm514 = df.loc[df['TS'] == 514]
    pm514 = pm514.values.tolist()
    pm515 = df.loc[df['TS'] == 515]
    pm515 = pm515.values.tolist()
    pm516 = df.loc[df['TS'] == 516]
    pm516 = pm516.values.tolist()
    pm517 = df.loc[df['TS'] == 517]
    pm517 = pm517.values.tolist()
    pm518 = df.loc[df['TS'] == 518]
    pm518 = pm518.values.tolist()
    pm519 = df.loc[df['TS'] == 519]
    pm519 = pm519.values.tolist()
    
    pm601=df.loc[df['TS'] == 601]
    pm601=pm601.values.tolist()
    pm602=df.loc[df['TS'] == 602]
    pm602=pm602.values.tolist()
    pm603=df.loc[df['TS'] == 603]
    pm603=pm603.values.tolist()
    pm604=df.loc[df['TS'] == 604]
    pm604=pm604.values.tolist()
    pm605=df.loc[df['TS'] == 605]
    pm605=pm605.values.tolist()
    pm606=df.loc[df['TS'] == 606]
    pm606=pm606.values.tolist()
    pm607=df.loc[df['TS'] == 607]
    pm607=pm607.values.tolist()
    pm608=df.loc[df['TS'] == 608]
    pm608=pm608.values.tolist()
    pm609=df.loc[df['TS'] == 609]
    pm609=pm609.values.tolist()
    pm610=df.loc[df['TS'] == 610]
    pm610=pm610.values.tolist()
    pm611=df.loc[df['TS'] == 611]
    pm611=pm611.values.tolist()
    pm612=df.loc[df['TS'] == 612]
    pm612=pm612.values.tolist()
    pm613=df.loc[df['TS'] == 613]
    pm613=pm613.values.tolist()
    pm614=df.loc[df['TS'] == 614]
    pm614=pm614.values.tolist()
    pm615=df.loc[df['TS'] == 615]
    pm615=pm615.values.tolist()
    pm616=df.loc[df['TS'] == 616]
    pm616=pm616.values.tolist()
    pm617=df.loc[df['TS'] == 617]
    pm617=pm617.values.tolist()
    pm618=df.loc[df['TS'] == 618]
    pm618=pm618.values.tolist()
    pm619=df.loc[df['TS'] == 619]
    pm619=pm619.values.tolist()
    pm620=df.loc[df['TS'] == 620]
    pm620=pm620.values.tolist()
    pm621=df.loc[df['TS'] == 621]
    pm621=pm621.values.tolist()
    pm622=df.loc[df['TS'] == 622]
    pm622=pm622.values.tolist()
    pm623=df.loc[df['TS'] == 623]
    pm623=pm623.values.tolist()
    pm624=df.loc[df['TS'] == 624]
    pm624=pm624.values.tolist()
    pm625=df.loc[df['TS'] == 625]
    pm625=pm625.values.tolist()
    pm626=df.loc[df['TS'] == 626]
    pm626=pm626.values.tolist()

    # print(pm501)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()


    return (
    udate, pm2week, pmmonth, pm2month, pmquart, pm401, pm402, pm403, pm404, pm405, pm406, pm407, pm408, pm409, pm410, pm411,
    pm412, pm413, pm414, pm415, pm416, pm417, pm418, pm419, pm420, pm421, pm422, pm423, pm424,
    pm501, pm502, pm503, pm504, pm505, pm506, pm507, pm508, pm509, pm510, pm511,pm512, pm513, pm514, pm515, pm516,
    pm517, pm518, pm519,
    pm601, pm602, pm603, pm604, pm605, pm606, pm607, pm608, pm609, pm610, pm611, pm612, pm613, pm614, pm615, pm616, 
    pm617, pm618, pm619, pm620, pm621, pm622, pm623, pm624, pm625, pm626)

# ********* PREVENTIVE MAINTENANCE Test (Online)****************
def get_data_pmtest(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:Z', skiprows=range(1), nrows=2)
    df = pd.DataFrame(data)
    pm2week = df.values.tolist()
    # print(pm2week)
    del df

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:L', skiprows=range(4), nrows=2)
    df = pd.DataFrame(data)
    pmmonth = df.values.tolist()
    # pmmonth = df.values.flatten().tolist()
    # print(pmmonth)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:F', skiprows=range(7), nrows=2)
    df = pd.DataFrame(data)
    pm2month = df.values.tolist()
    # print(pm2month)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:D', skiprows=range(10), nrows=2)
    df = pd.DataFrame(data)
    pmquart = df.values.tolist()

    # ***** Tab Data *****
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:K', skiprows=range(15))
    df = pd.DataFrame(data)

    df = df.fillna('')

    # df[4] = df[4].astype(int).apply('{:,}'.format)
    df = df.sort_values(by='Date', ascending=True)
    df = df.apply(lambda s: s.fillna({i: [] for i in df.index}))
    df['Date'] = df['Date'].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))

    pmlist = df.values.tolist()
    # print(df)

    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    # df = pd.DataFrame(data)
    # df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    # udate = df.values.flatten().tolist()

    return (pmlist, pm2week, pmmonth, pm2month, pmquart)

# ********* PREVENTIVE MAINTENANCE Planning ****************
def get_data_pmp(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:F', skiprows=range(2))
    df = pd.DataFrame(data)
    # df['Date of shipment'] = pd.to_datetime(df['Date of shipment']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')
    pmp46list = df.values.tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df

    return (pmp46list, udate)


# ********* Material (Repair)  ****************
def get_data_repair(sh_name, file_name, path='./data/rst_files_repo/'):

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df = df.dropna()
    # print(df)
    # # words = df.values.tolist()
    # # listkpi =df.values.flatten().tolist()
    start_word1 = next(iter(df[df['V'] == 'CUSTOMER SPARE'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1 = df.loc[start_word1 + 1:end_word1 - 1, :]
    lbl_cs = df1["V"].tolist()
    count_cs = df1["W"].tolist()
    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'
    # print(count_cs)

    start_word2 = next(iter(df[df['V'] == 'NCR'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    lbl_ncr = df2["V"].tolist()
    count_ncr = df2["W"].tolist()
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(lbl_ncr)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='D:K', skiprows=range(0))
    df = pd.DataFrame(data)
    df['Date of shipment'] = pd.to_datetime(df['Date of shipment']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')
    rma = df.values.tolist()

    lenlist = len(rma)
    # print(rma)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0]=df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df

    return (lbl_cs, count_cs, lbl_ncr, count_ncr, rma, lenlist, udate)


# ********* Reliability  ****************
def get_data_reliability(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df = df.dropna()
    # print(df)
    # # words = df.values.tolist()
    # # listkpi =df.values.flatten().tolist()
    start_word1 = next(iter(df[df['V'] == 'TOTAL IOS ON FLEET'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1 = df.loc[start_word1 + 1:end_word1 - 1, :]
    lbl_all = df1["V"].tolist()
    total_ios = df1["W"].tolist()
    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'

    start_word2 = next(iter(df[df['V'] == 'UNIQUE IOS ON FLEET'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    # lblres = df2["V"].tolist()
    unique_ios = df2["W"].tolist()
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(unique_ios)

    start_word3 = next(iter(df[df['V'] == 'IOS IMPACTING AVAILABILITY'].index), 'no match')
    end_word3 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df3 = df.loc[start_word3 + 1:end_word3 - 1, :]
    # lblsub = df3["V"].tolist()
    impact_ios= df3["W"].tolist()
    df.at[end_word3:end_word3, 'V'] = 'Grand TotalXxx'
    # print(df)

    # IOS Tracker
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='E', skiprows=range(3), nrows=10)
    # df = pd.DataFrame(data)
    # tracker_co = df.values.flatten().tolist()
    # # print(tracker_co)
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='F', skiprows=range(3), nrows=10)
    # df = pd.DataFrame(data)
    # tracker_og = df.values.flatten().tolist()
    # # print(tracker_og)
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G', skiprows=range(3), nrows=10)
    # df = pd.DataFrame(data)
    # tracker_ui = df.values.flatten().tolist()
    # # print(tracker_ui)
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='H', skiprows=range(3), nrows=10)
    # df = pd.DataFrame(data)
    # tracker_del = df.values.flatten().tolist()
    # # print(tracker_del)

    # tracker_sum = sum(tracker_co) + sum(tracker_og) + sum(tracker_ui) + sum(tracker_del)
    # print(tracker_sum)

    # ****** Unique IOS History *******
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='I:T', skiprows=range(3))
    df = pd.DataFrame(data)
    df = df.set_axis(['mon', 'brake', 'hvac', 'cvs', 'traction', 'tcms', 'doors', 'papis', 'nw', 'rst', 'slv', 'tbd'], axis=1, inplace=False)
    df = df.dropna()
    his_mon = df["mon"].tolist()
    his_brake = df["brake"].tolist()
    his_hvac = df["hvac"].tolist()
    his_cvs = df["cvs"].tolist()
    his_trac = df["traction"].tolist()
    his_tcms = df["tcms"].tolist()
    his_doors = df["doors"].tolist()
    his_papis = df["papis"].tolist()
    his_nw = df["nw"].tolist()
    his_rst = df["rst"].tolist()
    his_slv = df["slv"].tolist()
    his_tbd = df["tbd"].tolist()

    # his_sum = sum(his_brake) + sum(his_hvac) + sum(his_cvs)+ sum(his_trac)+ sum(his_tcms)+ sum(his_doors) + sum(his_papis)+ sum(his_nw)+ sum(his_rst)+ sum(his_slv)+ sum(his_tbd)

    # ****** IOS Impacting History *******
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='W:AH', skiprows=range(3))
    df = pd.DataFrame(data)
    df = df.set_axis(['mon', 'brake', 'hvac', 'cvs', 'traction', 'tcms', 'doors', 'papis', 'nw', 'rst', 'slv', 'tbd'],
                     axis=1, inplace=False)
    df = df.dropna()
    imp_mon = df["mon"].tolist()
    imp_brake = df["brake"].tolist()
    imp_hvac = df["hvac"].tolist()
    imp_cvs = df["cvs"].tolist()
    imp_trac = df["traction"].tolist()
    imp_tcms = df["tcms"].tolist()
    imp_doors = df["doors"].tolist()
    imp_papis = df["papis"].tolist()
    imp_nw = df["nw"].tolist()
    imp_rst = df["rst"].tolist()
    imp_slv = df["slv"].tolist()
    imp_tbd = df["tbd"].tolist()

    # imp_sum = sum(imp_brake) + sum(imp_hvac) + sum(imp_cvs) + sum(imp_trac) + sum(imp_tcms) + sum(imp_doors) + sum(
    #     imp_papis) + sum(imp_nw) + sum(imp_rst) + sum(imp_slv) + sum(imp_tbd)

    # ****** IOS Per Train *******
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='AJ:AL', skiprows=range(3))
    df = pd.DataFrame(data)
    df = df.set_axis(['train', 'critical', 'ncritical'],axis=1, inplace=False)
    df = df.dropna()
    ios_train = df["train"].tolist()
    ios_crit = df["critical"].tolist()
    ios_ncrit = df["ncritical"].tolist()

    # ****** IOS Details *******
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:F', skiprows=range(46))
    df = pd.DataFrame(data)
    df = df.fillna('')
    # df = df.sort_values(by='Date raised', ascending=False)

    # df['Date raised'] = pd.to_datetime(df['Date raised']).dt.strftime('%d-%b-%Y')
    # df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    # df = df.fillna('')

    ioslist = df.values.tolist()
    # print(ncrlist)

    lenlist = len(ioslist)
    # print (ioslist)


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%b %y'))
    udatemy = df.values.flatten().tolist()

    # print(udate)
    # print(monyear)

    del df

    return (lbl_all, total_ios, unique_ios, impact_ios,
            his_mon, his_brake, his_hvac, his_cvs, his_trac,his_tcms, his_doors, his_papis, his_nw, his_rst, his_slv, his_tbd,
            imp_mon, imp_brake, imp_hvac, imp_cvs, imp_trac, imp_tcms, imp_doors, imp_papis, imp_nw, imp_rst, imp_slv,imp_tbd,
            ios_train, ios_crit, ios_ncrit,
            ioslist, lenlist, udate, udatemy)


# ********* Equipment Reliability  ****************
def get_data_eq_reliability(sh_name, file_name, path='./data/rst_files_repo/'):

    # ****** MKBF *******
    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A:D', skiprows=range(3))
    df = pd.DataFrame(data)
    df = df.set_axis(['equipment', 'l12m', 'l3m', 'lm'],axis=1, inplace=False)
    df = df.fillna(0)
    mkbf_eq = df["equipment"].tolist()
    mkbf_l12m = df["l12m"].astype(int).tolist()
    mkbf_l3m = df["l3m"].astype(int).tolist()
    mkbf_lm = df["lm"].astype(int).tolist()


    # ****** MTBF *******
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G:J', skiprows=range(3))
    # df = pd.DataFrame(data)
    # df = df.set_axis(['equipment', 'l12m', 'l3m', 'lm'],axis=1, inplace=False)
    # df = df.fillna(0)
    # mtbf_eq = df["equipment"].tolist()
    # mtbf_l12m = df["l12m"].astype(int).tolist()
    # mtbf_l3m = df["l3m"].astype(int).tolist()
    # mtbf_lm = df["lm"].astype(int).tolist()


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='G:H', skiprows=range(3))
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='H', skiprows=range(3))
    df = pd.DataFrame(data)
    # df=df.dropna()
    mtbf_eq=df.values.tolist()
    # print (mtbf_eq)
    # mtbf_eq=df.values.flatten().tolist()

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='I', skiprows=range(3))
    df = pd.DataFrame(data)
    # df = df.set_axis(['lm'], axis=1, inplace=False)
    # df = df.fillna(0)

    mtbf_lm = df.values.tolist()
    mtbf_lm2 = df.values.flatten().tolist()

    mtbf_color=[]
    for i in range(len(mtbf_lm2)):
        if int(mtbf_lm2[i]) < 75:
            mtbf_color.append("#dc2f02")
        elif int(mtbf_lm2[i]) > 75 and int(mtbf_lm2[i]) < 99:
            mtbf_color.append("#ffb703")
        else:
            mtbf_color.append("#a7c957")


    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='J', skiprows=range(3))
    # df = pd.DataFrame(data)
    # mtbf_colorx = df.values.flatten().tolist()
    # # print(mtbf_color)

    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    del df

    return (mtbf_color, mkbf_eq, mkbf_l12m, mkbf_l3m, mkbf_lm, mtbf_eq, mtbf_lm, udate)

# ********* Quality  ****************
# ********* NCR  ****************
def get_data_ncr(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:L', skiprows=range(1))
    df = pd.DataFrame(data)

    df = df.sort_values(by='Date raised', ascending=False)

    df['Date raised'] = pd.to_datetime(df['Date raised']).dt.strftime('%d-%b-%Y')
    # df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    ncrlist = df.values.tolist()
    # print(ncrlist)

    lenlist=len(ncrlist)
    del df

    data = pd.read_excel(path + file_name, sheet_name='NCR KPI', usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df=df.dropna()
    # print(df)
    # words = df.values.tolist()
    # listkpi =df.values.flatten().tolist()

    start_word1 = next(iter(df[df['V'] == 'Status'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1=df.loc[start_word1+1:end_word1-1 , :]
    lblstatus= df1["V"].tolist()
    valstatus= df1["W"].tolist()
    # ncr_status = df1.values.flatten().tolist()
    # print(ncr_status)
    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'


    start_word2 = next(iter(df[df['V'] == 'Responsibility'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    lblres= df2["V"].tolist()
    valres= df2["W"].tolist()
    # ncr_res = df2.values.flatten().tolist()
    # print(ncr_res)
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(df)

    start_word3 = next(iter(df[df['V'] == 'Sub-system'].index), 'no match')
    end_word3 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df3 = df.loc[start_word3 + 1:end_word3 - 1, :]
    lblsub= df3["V"].tolist()
    valsub= df3["W"].tolist()
    # ncr_sub = df3.values.tolist()
    # print(ncr_sub)
    df.at[end_word3:end_word3, 'V'] = 'Grand TotalXxx'
    # print(df)


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    return (ncrlist, lenlist, lblstatus, valstatus, lblres, valres, lblsub, valsub, udate)

# ********* REX  ****************
def get_data_rex(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:M', skiprows=range(1))
    df = pd.DataFrame(data)

    df = df.sort_values(by='Date raised', ascending=False)

    df['Date raised'] = pd.to_datetime(df['Date raised']).dt.strftime('%d-%b-%Y')
    df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    rexlist = df.values.tolist()

    lenlist=len(rexlist)
    del df

    data = pd.read_excel(path + file_name, sheet_name='REX KPI', usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df=df.dropna()
    # words = df.values.tolist()
    # listkpi =df.values.flatten().tolist()

    start_word1 = next(iter(df[df['V'] == 'Status'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1=df.loc[start_word1+1:end_word1-1 , :]
    lblstatus= df1["V"].tolist()
    valstatus= df1["W"].tolist()
    # ncr_status = df1.values.flatten().tolist()
    # print(ncr_status)
    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'


    start_word2 = next(iter(df[df['V'] == 'Responsibility'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    lblres= df2["V"].tolist()
    valres= df2["W"].tolist()
    # ncr_res = df2.values.flatten().tolist()
    # print(ncr_res)
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(df)

    start_word3 = next(iter(df[df['V'] == 'Sub-system'].index), 'no match')
    end_word3 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df3 = df.loc[start_word3 + 1:end_word3 - 1, :]
    lblsub= df3["V"].tolist()
    valsub= df3["W"].tolist()
    # ncr_sub = df3.values.tolist()
    # print(ncr_sub)
    df.at[end_word3:end_word3, 'V'] = 'Grand TotalXxx'
    # print(df)


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    return (rexlist, lenlist, lblstatus, valstatus, lblres, valres, lblsub, valsub, udate)

# ********* 8D  ****************
def get_data_eightd(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='A:K', skiprows=range(1))
    df = pd.DataFrame(data)

    df = df.sort_values(by='Date raised', ascending=False)

    df['Date raised'] = pd.to_datetime(df['Date raised']).dt.strftime('%d-%b-%Y')
    df['Target Date'] = pd.to_datetime(df['Target Date']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    dlist = df.values.tolist()
    # print(ncrlist)

    lenlist=len(dlist)
    del df

    data = pd.read_excel(path + file_name, sheet_name='8D KPI', usecols='A:B')
    df = pd.DataFrame(data)
    df = df.set_axis(['V', 'W'], axis=1, inplace=False)
    df=df.dropna()
    # print(df)
    # words = df.values.tolist()
    # listkpi =df.values.flatten().tolist()

    start_word1 = next(iter(df[df['V'] == 'Status'].index), 'no match')
    end_word1 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df1=df.loc[start_word1+1:end_word1-1 , :]
    lblstatus= df1["V"].tolist()
    valstatus= df1["W"].tolist()
    # ncr_status = df1.values.flatten().tolist()

    df.at[end_word1:end_word1, 'V'] = 'Grand TotalXxx'


    start_word2 = next(iter(df[df['V'] == 'Responsibility'].index), 'no match')
    end_word2 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')
    df2 = df.loc[start_word2 + 1:end_word2 - 1, :]
    lblres= df2["V"].tolist()
    valres= df2["W"].tolist()
    # ncr_res = df2.values.flatten().tolist()
    # print(ncr_res)
    df.at[end_word2:end_word2, 'V'] = 'Grand TotalXxx'
    # print(df)

    start_word3 = next(iter(df[df['V'] == 'Sub-system'].index), 'no match')
    end_word3 = next(iter(df[df['V'] == 'Grand Total'].index), 'no match')

    df3 = df.loc[start_word3 + 1:end_word3 - 1, :]
    lblsub= df3["V"].tolist()
    valsub= df3["W"].tolist()
    # ncr_sub = df3.values.tolist()
    # print(ncr_sub)
    df.at[end_word3:end_word3, 'V'] = 'Grand TotalXxx'
    # print(df)


    data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    df = pd.DataFrame(data)
    df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    udate = df.values.flatten().tolist()

    return (dlist, lenlist, lblstatus, valstatus, lblres, valres, lblsub, valsub, udate)



 # ********* RST_Documents  ****************
def get_data_doc(sh_name, file_name, path='./data/rst_files_repo/'):
    data = pd.read_excel(path + file_name, sheet_name=sh_name, usecols='B:I', skiprows=range(2))
    df = pd.DataFrame(data)

    # df = df.sort_values(by='TS', ascending=True)

    df['Commissioning date'] = pd.to_datetime(df['Commissioning date']).dt.strftime('%d-%b-%Y')
    df['Arrival date in KSA'] = pd.to_datetime(df['Arrival date in KSA']).dt.strftime('%d-%b-%Y')
    df = df.fillna('')

    fdlist = df.values.tolist()
    fdlenlist=len(fdlist)
    # print(ncrlist)


    data = pd.read_excel(path + file_name, sheet_name='Design Docs', usecols='B:D', skiprows=range(2))
    df = pd.DataFrame(data)
    ddlist=df.values.tolist()
    ddlenlist = len(ddlist)
    # df=df.dropna()
    # print(df)
    data = pd.read_excel(path + file_name, sheet_name='Validation', usecols='B:D', skiprows=range(2))
    df = pd.DataFrame(data)
    valist=df.values.tolist()
    valenlist = len(valist)

    #
    # data = pd.read_excel(path + file_name, sheet_name=sh_name, header=None, usecols='A', skiprows=range(0), nrows=1)
    # df = pd.DataFrame(data)
    # df[0] = df[0].apply(lambda x: pd.Timestamp(x).strftime('%d-%b-%Y'))
    # udate = df.values.flatten().tolist()

    del df

    return (fdlist, fdlenlist, ddlist, ddlenlist, valist, valenlist)

#
#
# # ******** Reports.html data from Excel file
# def get_download(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path+file_name)
#     sheet = book.sheet_by_index(sheet_index)
#     list = []
#     data= []
#     for row_index in range(sheet.nrows):
#         for col_index in range(sheet.ncols):
#             d =sheet.cell(row_index, col_index).value
#             if sheet.cell(row_index, col_index).ctype == 3:
#                 dt=datetime.datetime(*xlrd.xldate_as_tuple(d,book.datemode))
#                 d=dt.strftime("%d %b %Y")
#             list.append(d)
#         data.append(list)
#         list =[]
#     # print ("data")
#     return(data)
#
# # ********Dashboard data for Test Procedure & Report page
# def get_data_db01(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path+file_name)
#     sheet = book.sheet_by_index(sheet_index)
#
#     start_col, start_row, end_col, end_row = (0, 0, 0, 0)  # (0,2,3,6) A3 to D7
#     data0 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     dataDT=data0[0][0]
#
#     start_col, start_row, end_col, end_row=(0,2,5,7) # (0,2,3,6) A3 to D7
#     data1=[sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in xrange(start_row, end_row + 1)]
#
#     start_col, start_row, end_col, end_row=(0,10,5,15) # (0,2,3,6) A3 to D7
#     data2=[sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in xrange(start_row, end_row + 1)]
#
# #format Date (Last Update)
#
#     dt = datetime.datetime(*xlrd.xldate_as_tuple(dataDT, book.datemode))
#     dataDT = dt.strftime("%d %b %Y")
#
#
# # Test Procedure data
#     proc_plan = int(sum(i[1] for i in data1))
#     proc_actual= int(sum(i[2] for i in data1))
#     proc_codeA = int(sum(i[3] for i in data1))
#     proc_subsys = ([round (i[4]*100)  for i in data1])
#     proc_subsys_codeA = ([round (i[5]*100)  for i in data1])
#     f_data1=[proc_plan, proc_actual, proc_codeA, proc_subsys, proc_subsys_codeA]
#
# # Test Report data
#     rpt_plan = int(sum(i[1] for i in data2))
#     rpt_actual = int(sum(i[2] for i in data2))
#     rpt_codeA= int(sum (i[3] for i in data2))
#     rpt_subsys = ([round (i[4]*100)  for i in data2])
#     rpt_subsys_codeA = ([round (i[5]*100)  for i in data2])
#     f_data2=[rpt_plan, rpt_actual, rpt_codeA, rpt_subsys, rpt_subsys_codeA]
#     # print (f_data2)
#
#     # ********* Test Report Progress OverAll Data ********
#     trMonth = []
#     trMonth_data = []
#     for row_index in range(sheet.nrows):
#         d = sheet.cell(row_index, 0).value
#         d2 = sheet.cell(row_index, 1).value
#         if d == "Test Report Progress":
#             trMonth = []
#             trMonth_data = []
#
#         trMonth.append(d)
#         trMonth_data.append(d2)
#
#     trMonth.pop(0)
#     # l4Month_data.pop(0)
#     while ("" in trMonth_data):
#         trMonth_data.remove("")
#
#
#     return(f_data1,f_data2,data1,data2,dataDT,trMonth,trMonth_data)
#
#
# # ********Dashboard data for Anomalies page
# def get_data_db02(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path + file_name)
#     sheet = book.sheet_by_index(sheet_index)
#     #For Date
#     start_col, start_row, end_col, end_row = (0, 0, 0, 0)  # (0,2,3,6) A3 to D7
#     data0 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     dataDT=data0[0][0]
#
#     # format Date (Last Update)
#
#     dt = datetime.datetime(*xlrd.xldate_as_tuple(dataDT, book.datemode))
#     dataDT = dt.strftime("%d %b %Y")
#
#
#     start_col, start_row, end_col, end_row = (0, 3, 3, 16)  # (0,2,3,6) A3 to D7
#     chart1_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     # print(chart1_data)
#     start_col, start_row, end_col, end_row = (1, 19, 7, 22)  # (0,2,3,6) A3 to D7
#     c_gb_data=[sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     # print(cgb_data[0])
#
#     start_col, start_row, end_col, end_row = (1, 26, 4, 29)  # (0,2,3,6) A3 to D7
#     c_tip_data=[sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     start_col, start_row, end_col, end_row = (1, 33, 4, 36)  # (0,2,3,6) A3 to D7
#     c_ss_data=[sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#
#     return (chart1_data,c_gb_data,c_tip_data,c_ss_data, dataDT)
#
# # *****************
# # ********  Dashboard data for Line-4
# # *****************
#
# def get_data_dbline4(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path + file_name)
#     sheet = book.sheet_by_index(sheet_index)
#     start_col, start_row, end_col, end_row = (0, 7, 10, 7)  # (0,2,3,6) A3 to D7
#     Tdata = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     PTR_data = [round (i * 100) for i in Tdata[0]]
#
#     start_col, start_row, end_col, end_row = (1, 10, 2, 13)  # (0,2,3,6) A3 to D7
#     lev4_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     PTR_lev4 = []
#     for j in range(len(lev4_data)):
#         PTR_lev4.append (round(sum(lev4_data[j] * 100) / len(lev4_data[j])))
#
#     start_col, start_row, end_col, end_row = (0, 8, 0, 8)  # (0,2,3,6) A3 to D7
#     Tdata = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     PTR_OA = [round(i * 100) for i in Tdata[0]]
#
#     # print(PTR_OA)
#
#     # ********* Non PTR data Collection (Line 4) ********
#
#     start_col, start_row, end_col, end_row = (0, 23, 11, 23)  # (0,2,3,6) A3 to D7
#     Tdata2 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     nPTR_data = [round (i * 100) for i in Tdata2[0]]
#
#     start_col, start_row, end_col, end_row = (1, 26, 1, 30)  # (0,2,3,6) A3 to D7
#     lev4_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     nPTR_lev4 = []
#     for j in range(len(lev4_data)):
#         nPTR_lev4.append(round(sum(lev4_data[j] * 100) / len(lev4_data[j])))
#
#
#     start_col, start_row, end_col, end_row = (0, 24, 0, 24)  # (0,2,3,6) A3 to D7
#     Tdata2 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     nPTR_OA = [round (i * 100) for i in Tdata2[0]]
#     # print(nPTR_OA)
#
# # ********* OverAll Data (Line 4) ********
#     l4Month = []
#     l4Month_data= []
#     for row_index in range(sheet.nrows):
#         d  = sheet.cell(row_index,0).value
#         d2 = sheet.cell(row_index,1).value
#         if d=="OverAll Progress":
#             l4Month=[]
#             l4Month_data=[]
#         l4Month.append(d)
#         l4Month_data.append(d2)
#
#     l4Month.pop(0)
#     # l4Month_data.pop(0)
#
#     # l4Month_data = ' '.join(l4Month_data).split()
#     # l4Month_data = [i for i in l4Month_data if i]
#     # l4Month_data = list(filter(None, l4Month_data))
#     while ("" in l4Month_data):
#         l4Month_data.remove("")
#
#     return(PTR_data,PTR_lev4,nPTR_data,nPTR_lev4,PTR_OA,nPTR_OA,l4Month,l4Month_data)
#
#
# # ********Dashboard PTR data for Line-6
#
# def get_data_dbline6(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path + file_name)
#     sheet = book.sheet_by_index(sheet_index)
#     start_col, start_row, end_col, end_row = (0, 8, 5, 8)  # (0,2,3,6) A3 to D7
#     Tdata = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     PTR6_data = [round (i * 100) for i in Tdata[0]]
#
#
#     start_col, start_row, end_col, end_row = (8, 3, 8, 6)  # (0,2,3,6) A3 to D7
#     lev6_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     PTR_lev6 = []
#     for j in range(len(lev6_data)):
#         PTR_lev6.append(round(sum(lev6_data[j] * 100) / len(lev6_data[j])))
#
#
#     start_col, start_row, end_col, end_row = (0, 9, 0, 9)  # (0,2,3,6) A3 to D7
#     PTR6_OA = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     # print (PTR6_OA)
#
#     # ***** Extracting Non PTR Line6 Level data ********
#
#     start_col, start_row, end_col, end_row = (0, 18, 4, 18)  # (0,2,3,6) A3 to D7
#     Tdata2 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     nPTR6_data = [round (i * 100) for i in Tdata2[0]]
#
#     start_col, start_row, end_col, end_row = (8, 13, 8, 16)  # (0,2,3,6) A3 to D7
#     lev6_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     nPTR_lev6 = []
#     for j in range(len(lev6_data)):
#         nPTR_lev6.append(round(sum(lev6_data[j] * 100) / len(lev6_data[j])))
#
#
#     start_col, start_row, end_col, end_row = (0, 19, 0, 19)  # (0,2,3,6) A3 to D7
#     nPTR6_OA = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#
#     # print(nPTR6_OA)
#
#     # ********* OverAll Data (Line 6) ********
#     l6Month = []
#     l6Month_data = []
#     for row_index in range(sheet.nrows):
#         d = sheet.cell(row_index, 0).value
#         d2 = sheet.cell(row_index, 1).value
#         if d == "OverAll Progress":
#             l6Month = []
#             l6Month_data = []
#         l6Month.append(d)
#         l6Month_data.append(d2)
#
#     l6Month.pop(0)
#     # l6Month_data.pop(0)
#
#     while ("" in l6Month_data):
#         l6Month_data.remove("")
#
#
#     return (PTR6_data, PTR_lev6, nPTR6_data, nPTR_lev6, PTR6_OA, nPTR6_OA, l6Month, l6Month_data )
#
#
# # ********Dashboard data for Line-5
# def get_data_dbline5(sheet_index, file_name, path='./data/files_repo/'):
#     book = open_workbook(path + file_name)
#     sheet = book.sheet_by_index(sheet_index)
#
#     start_col, start_row, end_col, end_row = (0, 7, 18, 7)  # (0,2,3,6) A3 to D7
#     Tdata5 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     OA5_data = [round (i * 100) for i in Tdata5[0]]
#     # print(OA5_data)
#
#
#
# # ********* Overall percent (Line 5)(due to excluding station 5A1) ********
#     start_col, start_row, end_col, end_row = (0, 8, 0, 8)  # (0,2,3,6) A3 to D7
#     Tdata5 = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#              xrange(start_row, end_row + 1)]
#     OApercent = [round(i * 100) for i in Tdata5[0]]
#     # print(OApercent)
#
# # ********* Level (Line 5) ********
#     start_col, start_row, end_col, end_row = (23, 3, 23, 6)  # (0,2,3,6) A3 to D7
#     lev5_data = [sheet.row_values(row, start_colx=start_col, end_colx=end_col + 1) for row in
#                  xrange(start_row, end_row + 1)]
#
#
#     OA_lev5 = []
#     for j in range(len(lev5_data)):
#         OA_lev5.append(round(sum(lev5_data[j] * 100) / len(lev5_data[j])))
#
# # ********* OverAll Data (Line 5) ********
#     l5Month = []
#     l5Month_data = []
#     for row_index in range(sheet.nrows):
#         d = sheet.cell(row_index, 0).value
#         d2 = sheet.cell(row_index, 1).value
#         if d == "OverAll Progress":
#             l5Month = []
#             l5Month_data = []
#         l5Month.append(d)
#         l5Month_data.append(d2)
#
#     l5Month.pop(0)
#     # l5Month_data.pop(0)
#
#     while ("" in l5Month_data):
#         l5Month_data.remove("")
#
#
#     return (OA5_data,OApercent,OA_lev5,l5Month,l5Month_data)
#
#
#
#
#
# def load_csv(file='file1.csv', path='./data/'):
#     with open(path+file) as csv_data:
#         row_data = []
#         data = reader(csv_data, delimiter=',')
#         for i,x in enumerate(data):
#             if i is not 0:
#                 row_data.append(x)
#     return (row_data)
#
# def get_csv(file, path='./data/csv/'):
#     #    data = reader(csv_data, delimiter=',')
#     return df
#
#
