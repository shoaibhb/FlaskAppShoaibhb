from flask import Blueprint, render_template, request, send_from_directory, current_app, json, redirect
from flask_login import login_required, current_user



from .dataget import get_data_configl4, get_data_configl5, get_data_configl6, get_data_pm, get_data_ncr,\
                    get_data_rex, get_data_eightd, get_data_repair, get_data_reliability, get_data_doc, get_data_cmts, \
                    get_data_availability, get_data_tir, get_data_pmtest, get_data_swh, get_data_retrofit, get_data_pmp, \
                    get_data_avakpi, get_data_eq_reliability, get_data_user

from . import db, create_app
import os

from .models import Tbl_pm

main = Blueprint('main', __name__)

#@main.route('/create_db')
#def createdb():
#    db.create_all(app=create_app())  # pass the create_app result so Flask-SQLAlchemy gets the configuration.
#    return render_template("index.html")


# ***** checking UserAdmin PM



@main.route('/delete/<string:getid>', methods = ['POST','GET'])
def delete_pm(getid):
    # pmid = Tbl_pm.pm_id
    # print(getid)
    Tbl_pm.query.filter(Tbl_pm.pm_id == getid).delete()
    # db.session.delete(getid)
    db.session.commit()
    return redirect('/pmentryadmin')
    # return render_template('pages/useradmin.html')

@main.route('/pmadd', methods=['GET', 'POST'])
def insert_pm():
    pdate = request.form['txtdate']
    train = request.form['txttrain']
    doc = request.form['txtdoc']
    mileage = request.form['txtmileage']
    w2= request.form['w2']
    m1 = request.form['m1']
    m2 = request.form['m2']
    m3 = request.form['m3']
    m6 = request.form['m6']
    m9 = request.form['m9']
    y1 = request.form['y1']
    # new_pm = Tbl_pm(pm_date=pdate, pm_train=train, pm_doc=doc, pm_mileage=mileage, pm_2w=w2, pm_1m=m1, pm_2m=m2)


    new_pm = Tbl_pm(pm_date=pdate, pm_train=train, pm_doc=doc.upper(), pm_mileage=mileage, pm_2w=w2, pm_1m=m1, pm_2m=m2, pm_3m=m3, pm_6m=m6, pm_9m=m9, pm_1y=y1)


    # add the new user to the database
    db.session.add(new_pm)
    db.session.commit()
    return redirect('/pmentryflow')
    # return redirect('/')

@main.route('/pmentryflow')
@login_required
def query_recordsflow():
    nam= current_user.name
    if nam.lower()=="RAO KAMRAN".lower() or "Ramachandran KARTHICK".lower() or "Imran Rasheed".lower() or "Zouhair AZZABI".lower():
        # pm = Tbl_pm.query.all()
        pm = reversed(db.session.query(Tbl_pm).order_by(Tbl_pm.pm_id.asc()).limit(70).all())
        # pm = Tbl_pm.query.filter_by(pm_train='602').all()
        return render_template('pages/pmentryflow.html', pm=pm,nam=nam)
    else:
        return render_template('pages/401.html')



@main.route('/pmentryadmin')
# def insert_pm():
#     new_pm = Tbl_pm(pm_date="31-Feb-2022", pm_train="817", pm_doc="PM3333", pm_mileage="22000")
#
#     # add the new user to the database
#     db.session.add(new_pm)
#     db.session.commit()
#     return("45")

def query_records():
    # ses=db.session()
    # cur=ses.execute("select * from tbl_pm").cursor
    # employee= cur.fetchall()
    # print (type(employee))
    up = get_data_user(sh_name='user-access', file_name='rst_report01.xlsx')
    # nam= current_user.name
    # if nam.lower()=="RAO KAMRAN".lower() or "Taha MUSSA".lower():
    if up[2] == "yes":
        pm = Tbl_pm.query.all()
        # pm = reversed(db.session.query(Tbl_pm).order_by(Tbl_pm.pm_id.desc()).limit(100).all())
        # pm = Tbl_pm.query.filter_by(pm_train='602').all()
        return render_template('pages/pmentryadmin.html', pm=pm)
    else:
        return render_template('pages/401.html')

    # pm = Tbl_pm.query.filter(Tbl_pm.pm_date.between('1-Jan-22', '31-Jan-22'))



# ***** End checking UserAdmin PM

@main.route('/email')
def indexx():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    filename="recipients.txt"
    filename2 = "recipientsCC.txt"

    username = "rst_riyadh@hotmail.com"
    password = "Riyadh@123"
    mail_from = "rst_riyadh@hotmail.com"
    # mail_to = "kamran.rao@alstomgroup.com"
    mail_to = open(filename, 'r').read()
    mail_cc = open(filename2, 'r').read()
    mail_subject = "Automated Email From RST(Riyadh) Server"
    mail_body = "TRAIN AVAILABILITY STATUS"
    mail_attachment = "test.pdf"
    mail_attachment_name = "Fleet Availability.pdf"

    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    # mimemsg['Cc'] = mail_cc
    mimemsg['Bcc'] = mail_cc
    mimemsg['Subject'] = mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))

    with open(mail_attachment, "rb") as attachment:
        mimefile = MIMEBase('application', 'octet-stream')
        mimefile.set_payload((attachment).read())
        encoders.encode_base64(mimefile)
        mimefile.add_header('Content-Disposition', "attachment; filename= %s" % mail_attachment_name)
        mimemsg.attach(mimefile)
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login(username, password)
        connection.send_message(mimemsg)
        connection.quit()

    return ("Email is Successfully Sent")


@main.route('/')
def index():
    return render_template('login.html')

@main.route('/culist')
# @login_required
def culist():
    return send_from_directory('','loginhistory.xlsx')



@main.route('/proj')
@login_required
def proj():

    return render_template('pages/rst_projects.html')


@main.route('/availability')
@login_required
def availability():
    availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6,tslistnok4, \
    tslistnok5, tslistnok6, mtustatus, mtustatus2=get_data_availability(sh_name='availability', file_name='rst_report01.xlsx')

    # if current_user.name!="RAO KAMRAN":
    return render_template('pages/rst_availability.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6,  mtustatus=mtustatus, mtustatus2=mtustatus2)


@main.route('/availabilityPDF')
# @login_required
def availabilityPDF():
    availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6, tslistnok4, \
    tslistnok5, tslistnok6, mtustatus, mtustatus2 = get_data_availability(sh_name='availability',
                                                                          file_name='rst_report01.xlsx')

    # if current_user.name!="RAO KAMRAN":
    return render_template('pages/rst_availabilityPDF.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6, mtustatus=mtustatus, mtustatus2=mtustatus2)


@main.route('/availabilityl46')
@login_required
def availabilityl46():

    up = get_data_user(sh_name='user-access', file_name='rst_report01.xlsx')
    print(up)
    if up[6] == "yes":
        availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6,tslistnok4, \
        tslistnok5, tslistnok6, mtustatus, mtustatus2=get_data_availability(sh_name='availability', file_name='rst_report01.xlsx')

        # if current_user.name!="RAO KAMRAN":
        return render_template('pages/rst_availability_l46.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6,  mtustatus=mtustatus, mtustatus2=mtustatus2)
    else:
        return render_template('pages/401.html')


@main.route('/availabilityPDFl46')
# @login_required
def availabilityPDFl46():
    availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6, tslistnok4, \
    tslistnok5, tslistnok6, mtustatus, mtustatus2 = get_data_availability(sh_name='availability',
                                                                          file_name='rst_report01.xlsx')

    # if current_user.name!="RAO KAMRAN":
    return render_template('pages/rst_availabilityPDF_l46.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6, mtustatus=mtustatus, mtustatus2=mtustatus2)

@main.route('/availabilityl5')
@login_required
def availabilityl5():

    up = get_data_user(sh_name='user-access', file_name='rst_report01.xlsx')

    if up[7] == "yes":
        availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6,tslistnok4, \
        tslistnok5, tslistnok6, mtustatus, mtustatus2=get_data_availability(sh_name='availability', file_name='rst_report01.xlsx')

        # if current_user.name!="RAO KAMRAN":
        return render_template('pages/rst_availability_l5.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6,  mtustatus=mtustatus, mtustatus2=mtustatus2)

    else:
        return render_template('pages/401.html')



@main.route('/availabilityPDFl5')
# @login_required
def availabilityPDFl5():
    availtsl, availts, udate, tslistok4, tslistok5, tslistok6, tslistpok4, tslistpok5, tslistpok6, tslistnok4, \
    tslistnok5, tslistnok6, mtustatus, mtustatus2 = get_data_availability(sh_name='availability',
                                                                          file_name='rst_report01.xlsx')

    # if current_user.name!="RAO KAMRAN":
    return render_template('pages/rst_availabilityPDF_l5.html', availtsl=availtsl, availts=availts, udate=udate,
                           tslistok4=tslistok4, tslistok5=tslistok5, tslistok6=tslistok6, tslistpok4=tslistpok4,
                           tslistpok5=tslistpok5, tslistpok6=tslistpok6, tslistnok4=tslistnok4, tslistnok5=tslistnok5,
                           tslistnok6=tslistnok6, mtustatus=mtustatus, mtustatus2=mtustatus2)


@main.route('/availabilitykpil46')
@login_required
def availabilitykpil46():
    kpil4date, l4ava, l4target, l4total, l6ava, l6target, l6total, l5ava, l5target, l5total, udate = \
        get_data_avakpi(sh_name='avakpi',file_name='rst_report01.xlsx')

    return render_template('pages/rst_availability_kpil46.html', kpil4date=kpil4date, l4ava=l4ava, l4target=l4target, l4total=l4total,
                           l6ava=l6ava, l6target=l6target, l6total=l6total, l5ava=l5ava, l5target=l5target, l5total=l5total, udate=udate)

@main.route('/availabilitykpil5')
@login_required
def availabilitykpil5():
    kpil4date, l4ava, l4target, l4total, l6ava, l6target, l6total, l5ava, l5target, l5total, udate = \
        get_data_avakpi(sh_name='avakpi',file_name='rst_report01.xlsx')

    return render_template('pages/rst_availability_kpil5.html', kpil4date=kpil4date, l5ava=l5ava, l5target=l5target, l5total=l5total, udate=udate)


@main.route('/reliability')
@login_required
def reliability():

    lbl_all, total_ios, unique_ios, impact_ios, his_mon,\
    his_brake, his_hvac, his_cvs, his_trac, his_tcms, his_doors, his_papis, his_nw, his_rst, his_slv, his_tbd, \
    imp_mon, imp_brake, imp_hvac, imp_cvs, imp_trac, imp_tcms, imp_doors, imp_papis, imp_nw, imp_rst, imp_slv,imp_tbd,\
    ios_train, ios_crit, ios_ncrit, ioslist, lenlist, udate, udatemy\
        =get_data_reliability(sh_name='reliability', file_name='rst_report01.xlsx')

    return render_template('pages/rst_reliability.html', lbl_all=lbl_all, total_ios=total_ios, unique_ios=unique_ios,
                           impact_ios=impact_ios, his_mon=his_mon, his_brake=his_brake,
                           his_hvac=his_hvac, his_cvs=his_cvs, his_trac=his_trac, his_tcms=his_tcms, his_doors=his_doors,
                           his_papis=his_papis, his_nw=his_nw, his_rst=his_rst, his_slv=his_slv, his_tbd=his_tbd,
                           imp_mon=imp_mon, imp_brake=imp_brake, imp_hvac=imp_hvac, imp_cvs=imp_cvs, imp_trac=imp_trac,
                           imp_tcms=imp_tcms, imp_doors=imp_doors, imp_papis=imp_papis, imp_nw=imp_nw, imp_rst=imp_rst,
                           imp_slv=imp_slv, imp_tbd=imp_tbd, ios_train=ios_train, ios_crit=ios_crit, ios_ncrit=ios_ncrit,
                           ioslist=ioslist, lenlist=lenlist, udate=udate, udatemy=udatemy)

@main.route('/EquipmentReliability')
@login_required
def eqreliability():
    mtbf_color, mkbf_eq, mkbf_l12m, mkbf_l3m, mkbf_lm, mtbf_eq, mtbf_lm, udate = \
        get_data_eq_reliability(sh_name='eq-reliability', file_name='rst_report01.xlsx')

    return render_template('pages/rst_eq_reliability.html', mtbf_color=mtbf_color, mkbf_eq=mkbf_eq, mkbf_l12m=mkbf_l12m, mkbf_l3m=mkbf_l3m,
                           mkbf_lm=mkbf_lm, mtbf_eq=mtbf_eq, mtbf_lm=mtbf_lm, udate=udate)


@main.route('/TIR_L5')
@login_required
def tir_l5():
    tirlist, lbltir, valtir, lblorigin, valorigin, lblpic, valpic, lblclosure, valclosure, lblpicx, valpicx, udate=\
        get_data_tir(sh_name='TIR SUMMARY', file_name='RUH-TSY-RST-TIR-SUMMARY_L5.xlsm')
    return render_template('pages/rst_tir_l5.html', tirlist=tirlist, lbltir=lbltir, valtir=valtir, lblorigin=lblorigin,
                           valorigin=valorigin, lblpic=lblpic, valpic=valpic, lblclosure=lblclosure,
                           valclosure=valclosure, lblpicx=lblpicx, valpicx=valpicx, udate=udate)


@main.route('/TIR_L46')
@login_required
def tir_l46():
    tirlist, lbltir, valtir, lblorigin, valorigin, lblpic, valpic, lblclosure, valclosure, lblpicx, valpicx, udate=\
        get_data_tir(sh_name='TIR SUMMARY', file_name='RUH-TSY-RST-TIR-SUMMARY_L46.xlsm')
    return render_template('pages/rst_tir_l46.html', tirlist=tirlist, lbltir=lbltir, valtir=valtir, lblorigin=lblorigin,
                           valorigin=valorigin, lblpic=lblpic, valpic=valpic, lblclosure=lblclosure,
                           valclosure=valclosure, lblpicx=lblpicx, valpicx=valpicx, udate=udate)



@main.route('/TIR')
@login_required
def tir():
    tirlist, lbltir, valtir, lblorigin, valorigin, lblpic, valpic, lblclosure, valclosure, lblpicx, valpicx, udate=\
        get_data_tir(sh_name='TIR SUMMARY', file_name='TIR SUMMARY.xlsm')
    return render_template('pages/rst_tir.html', tirlist=tirlist, lbltir=lbltir, valtir=valtir, lblorigin=lblorigin,
                           valorigin=valorigin, lblpic=lblpic, valpic=valpic, lblclosure=lblclosure,
                           valclosure=valclosure, lblpicx=lblpicx, valpicx=valpicx, udate=udate)



@main.route('/configuration_line4')
@login_required

def configuration_line4():

    tml4,pol4,tsl4pok,tsl4ok,tsl4nok,swl4,swsl4,statusl4,bll4,udate, tmid=get_data_configl4(sh_name='configl4', file_name='rst_report01.xlsx')

    return render_template('pages/rst_line4_config.html',name=current_user.name, email=current_user.email,
                           tml4=tml4,pol4=pol4, tsl4pok=tsl4pok, tsl4ok=tsl4ok, tsl4nok=tsl4nok, swl4=swl4, swsl4=swsl4,
                           statusl4=statusl4, bll4=bll4, udate=udate, tmid=tmid)



@main.route('/configuration_line5')
@login_required
def configuration_line5():

    up = get_data_user(sh_name='user-access', file_name='rst_report01.xlsx')
    # print(up[1])
    # print(up)
    if up[7] == "yes":
        tml5, pol5, tsl5pok, tsl5ok, tsl5nok, swl5, swsl5, statusl5, bll5, udate, tmid = get_data_configl5(sh_name='configl5',
                                                                                    file_name='rst_report01.xlsx')

        return render_template('pages/rst_line5_config.html', name=current_user.name, email=current_user.email,
                               tml5=tml5, pol5=pol5, tsl5pok=tsl5pok, tsl5ok=tsl5ok, tsl5nok=tsl5nok, swl5=swl5, swsl5=swsl5,
                               statusl5=statusl5, bll5=bll5, udate=udate, tmid=tmid)
    else:
        return render_template('pages/401.html')


@main.route('/configuration_line6')
@login_required
def configuration_line6():

    up = get_data_user(sh_name='user-access',file_name='rst_report01.xlsx')
    # print(up[6])
    if up[6]=="yes":
        tml6, pol6, tsl6pok, tsl6ok, tsl6nok, swl6, swsl6, statusl6, bll6, udate, tmid = get_data_configl6(sh_name='configl6',
                                                                                file_name='rst_report01.xlsx')
        return render_template('pages/rst_line6_config.html', name=current_user.name, email=current_user.email,
                           tml6=tml6, pol6=pol6, tsl6pok=tsl6pok, tsl6ok=tsl6ok, tsl6nok=tsl6nok, swl6=swl6, swsl6=swsl6,
                           statusl6=statusl6, bll6=bll6,udate=udate,tmid=tmid)
    else:
        return render_template('pages/401.html')



@main.route('/software_history46')
@login_required
def swhistory46():
    swh, udate = get_data_swh(sh_name='sw_history', file_name='rst_report01.xlsx')
    return render_template('pages/rst_swhistory46.html',swh=swh, udate=udate)

@main.route('/software_history5')
@login_required
def swhistory5():
    swh, udate = get_data_swh(sh_name='sw_history', file_name='rst_report01.xlsx')
    return render_template('pages/rst_swhistory5.html',swh=swh, udate=udate)



@main.route('/NCR')
@login_required
def ncr():
    ncrlist, lenlist,lblstatus, valstatus, lblres, valres, lblsub, valsub, udate = get_data_ncr(sh_name='NCR',file_name='RST Quality Report.xlsx')
    return render_template('pages/rst_ncr.html', ncrlist=ncrlist, lenlist=lenlist, lblstatus=lblstatus,
                           valstatus=valstatus, lblres=lblres, valres=valres, lblsub=lblsub, valsub=valsub, udate=udate)


@main.route('/REX46')
@login_required
def rex46():
    rexlist, lenlist,lblstatus, valstatus, lblres, valres, lblsub, valsub, udate = get_data_rex(sh_name='REX',file_name='RST Quality Report.xlsx')
    return render_template('pages/rst_rex46.html', rexlist=rexlist, lenlist=lenlist, lblstatus=lblstatus,
                           valstatus=valstatus, lblres=lblres, valres=valres, lblsub=lblsub, valsub=valsub, udate=udate)

@main.route('/REX5')
@login_required
def rex5():
    rexlist, lenlist,lblstatus, valstatus, lblres, valres, lblsub, valsub, udate = get_data_rex(sh_name='REX',file_name='RST Quality Report.xlsx')
    return render_template('pages/rst_rex5.html', rexlist=rexlist, lenlist=lenlist, lblstatus=lblstatus,
                           valstatus=valstatus, lblres=lblres, valres=valres, lblsub=lblsub, valsub=valsub, udate=udate)


@main.route('/8D5')
@login_required
def eightd5():
    dlist, lenlist,lblstatus, valstatus, lblres, valres, lblsub, valsub, udate = get_data_eightd(sh_name='8D',file_name='RST Quality Report.xlsx')
    return render_template('pages/rst_8d5.html', dlist=dlist, lenlist=lenlist, lblstatus=lblstatus,
                           valstatus=valstatus, lblres=lblres, valres=valres, lblsub=lblsub, valsub=valsub, udate=udate)

@main.route('/8D46')
@login_required
def eightd46():
    dlist, lenlist,lblstatus, valstatus, lblres, valres, lblsub, valsub, udate = get_data_eightd(sh_name='8D',file_name='RST Quality Report.xlsx')
    return render_template('pages/rst_8d46.html', dlist=dlist, lenlist=lenlist, lblstatus=lblstatus,
                           valstatus=valstatus, lblres=lblres, valres=valres, lblsub=lblsub, valsub=valsub, udate=udate)

@main.route('/corrective_maintenance')
@login_required
def cmts():
    cmtslist, lenlist, btstatus, udate= get_data_cmts(sh_name='Train status',file_name='Train status.xlsx')
    return render_template('pages/rst_cmts.html', cmtslist=cmtslist, lenlist=lenlist, btstatus=btstatus, udate=udate)


@main.route('/train_status_line46')
@login_required
def cmtsl46():
    cmtslist, lenlist, btstatus, udate= get_data_cmts(sh_name='Train status',file_name='Train status_L46.xlsx')
    return render_template('pages/rst_ts_l46.html', cmtslist=cmtslist, lenlist=lenlist, btstatus=btstatus, udate=udate)


@main.route('/train_status_line5')
@login_required
def cmtsl5():
    cmtslist, lenlist, btstatus, udate= get_data_cmts(sh_name='Train status',file_name='Train status_L5.xlsx')
    return render_template('pages/rst_ts_l5.html', cmtslist=cmtslist, lenlist=lenlist, btstatus=btstatus, udate=udate)


@main.route('/documents46')
@login_required
def doc46():
    fdlist, fdlenlist, ddlist, ddlenlist, valist, valenlist = get_data_doc(sh_name='FLEET DETAILS',file_name='Details of the documents.xlsx')

    return render_template('pages/rst_doc46.html', fdlist=fdlist, fdlenlist=fdlenlist, ddlist=ddlist, ddlenlist=ddlenlist,
                           valist=valist, valenlist=valenlist)

@main.route('/documents5')
@login_required
def doc5():
    fdlist, fdlenlist, ddlist, ddlenlist, valist, valenlist = get_data_doc(sh_name='FLEET DETAILS',file_name='Details of the documents.xlsx')

    return render_template('pages/rst_doc5.html', fdlist=fdlist, fdlenlist=fdlenlist, ddlist=ddlist, ddlenlist=ddlenlist,
                           valist=valist, valenlist=valenlist)


@main.route('/preventive_maintenanceOLD')
@login_required
def preventive_maintenance():
    udate, pm2week, pmmonth, pm2month, pmquart, pm401, pm402, pm403, pm404, pm405, pm406, pm407, pm408, pm409, pm410, pm411, \
    pm412, pm413, pm414, pm415, pm416, pm417, pm418, pm419, pm420, pm421, pm422, pm423, pm424, \
    pm501, pm502, pm503, pm504, pm505, pm506, pm507, pm508, pm509, pm510, pm511,pm512, pm513, pm514, pm515, pm516, \
    pm517, pm518, pm519, pm601, pm602, pm603, pm604, pm605, pm606, pm607, pm608, pm609, pm610, pm611, pm612, pm613, \
    pm614, pm615, pm616, pm617, pm618, pm619, pm620, pm621, pm622, pm623, pm624, pm625, pm626 \
        = get_data_pm(sh_name='pm', file_name='rst_report01.xlsx')

    return render_template('pages/rst_pm.html',udate=udate, pm2week=pm2week, pmmonth=pmmonth, pm2month=pm2month, pmquart=pmquart,
                           pm401=pm401, pm402=pm402, pm403=pm403, pm404=pm404, pm405=pm405, pm406=pm406, pm407=pm407,
                           pm408=pm408, pm409=pm409, pm410=pm410, pm411=pm411, pm412=pm412, pm413=pm413, pm414=pm414,
                           pm415=pm415, pm416=pm416, pm417=pm417, pm418=pm418, pm419=pm419, pm420=pm420, pm421=pm421,
                           pm422=pm422, pm423=pm423, pm424=pm424, 
                           pm501=pm501, pm502=pm502, pm503=pm503, pm504=pm504, pm505=pm505, pm506=pm506, pm507=pm507,
                           pm508=pm508, pm509=pm509, pm510=pm510, pm511=pm511, pm512=pm512, pm513=pm513, pm514=pm514,
                           pm515=pm515, pm516=pm516, pm517=pm517, pm518=pm518, pm519=pm519,
                           pm601=pm601, pm602=pm602, pm603=pm603, pm604=pm604, pm605=pm605, pm606=pm606, pm607=pm607,
                           pm608=pm608, pm609=pm609, pm610=pm610, pm611=pm611, pm612=pm612, pm613=pm613, pm614=pm614,
                           pm615=pm615, pm616=pm616, pm617=pm617, pm618=pm618, pm619=pm619, pm620=pm620, pm621=pm621,
                           pm622=pm622, pm623=pm623, pm624=pm624, pm625=pm625, pm626=pm626)

@main.route('/preventive_maintenance_L46')
@login_required
def testpm():
    # pm = Tbl_pm.query.order_by(Tbl_pm.pm_id.desc()).limit(1800).all()

    # pm= db.session.query(Tbl_pm).filter(Tbl_pm.pm_train.like('5%')).all()
    pm= db.session.query(Tbl_pm).filter(Tbl_pm.pm_train.like('4%') | Tbl_pm.pm_train.like('6%')).all()

    udate=db.session.query(Tbl_pm).order_by(Tbl_pm.pm_id.desc()).first()
    udate=[udate.pm_date]

    # pmlist, pm2week, pmmonth, pm2month, pmquart=get_data_pmtest(sh_name='pm', file_name='rst_report01.xlsx')
    # return render_template('pages/rst_pm.html', pm=pm, pm2week=pm2week, pmmonth=pmmonth, pm2month=pm2month,
    #                        pmquart=pmquart, udate=udate)
    return render_template('pages/rst_pml46.html', pm=pm, udate=udate)


@main.route('/preventive_maintenance_L5')
@login_required
def testpm5():

    pm= db.session.query(Tbl_pm).filter(Tbl_pm.pm_train.like('5%')).all()

    udate=db.session.query(Tbl_pm).order_by(Tbl_pm.pm_id.desc()).first()
    udate=[udate.pm_date]

    return render_template('pages/rst_pml5.html', pm=pm, udate=udate)


@main.route('/pm_planning')
@login_required
def pmp():
    pmp46list, udate=get_data_pmp(sh_name='Sheet1', file_name='Planning Forecast 2022-Depot46.xlsx')
    return render_template('pages/rst_pmp.html', pmp46list=pmp46list,udate=udate)


@main.route('/retrofit')
@login_required
def retrofit():
    r_sum_list,udate = get_data_retrofit(sh_name='retrofit_summary', file_name='rst_report01.xlsx')
    return render_template('pages/rst_retrofit.html',r_sum_list=r_sum_list, udate=udate)
    # return render_template('dashboard02.html',name=current_user.name, email=current_user.email,
    #                        chart1_data=chart1_data, c_gb_data=c_gb_data, c_tip_data=c_tip_data,
    #                        c_ss_data=c_ss_data, dataDT=dataDT)



@main.route('/repair46')
@login_required
def repair46():
    lbl_cs, count_cs, lbl_ncr, count_ncr, rma, lenlist, udate = get_data_repair(sh_name='repair', file_name='rst_report01.xlsx')
    return render_template('pages/rst_repair46.html',lbl_cs=lbl_cs, count_cs=count_cs, lbl_ncr=lbl_ncr,
                           count_ncr=count_ncr, rma=rma, lenlist=lenlist, udate=udate)

@main.route('/repair5')
@login_required
def repair5():
    lbl_cs, count_cs, lbl_ncr, count_ncr, rma, lenlist, udate = get_data_repair(sh_name='repair', file_name='rst_report01.xlsx')
    return render_template('pages/rst_repair5.html',lbl_cs=lbl_cs, count_cs=count_cs, lbl_ncr=lbl_ncr,
                           count_ncr=count_ncr, rma=rma, lenlist=lenlist, udate=udate)

# @main.route('/dashboardLines')
# @login_required
# def dashboard_Lines():
#     PTR_data,PTR_lev4,nPTR_data,nPTR_lev4,PTR_OA,nPTR_OA,l4Month,l4Month_data\
#         =get_data_dbline4(sheet_index=3, file_name='Reports_Template.xlsx')
#
#     PTR6_data, PTR_lev6, nPTR6_data, nPTR_lev6,PTR6_OA, nPTR6_OA, l6Month, l6Month_data\
#         = get_data_dbline6(sheet_index=4, file_name='Reports_Template.xlsx')
#
#     OA5_data, OApercent, OA_lev5, l5Month, l5Month_data \
#         = get_data_dbline5(sheet_index=5,file_name='Reports_Template.xlsx')
#
#     return render_template('dashboardpsl.html', name=current_user.name, email=current_user.email,
#                            l4Month=l4Month, l4Month_data=l4Month_data,l6Month_data=l6Month_data,
#                             l5Month=l5Month,l5Month_data=l5Month_data)

#
# @main.route('/dashboardLine4')
# @login_required
# def dashboard_Line4():
#     PTR_data,PTR_lev4,nPTR_data,nPTR_lev4,PTR_OA,nPTR_OA,l4Month,l4Month_data\
#         =get_data_dbline4(sheet_index=3, file_name='Reports_Template.xlsx')
#     return render_template('dashboardpsl4.html', name=current_user.name, email=current_user.email,
#                            PTR_data=PTR_data,PTR_lev4=PTR_lev4,
#                            nPTR_data=nPTR_data,nPTR_lev4=nPTR_lev4,
#                            PTR_OA=PTR_OA,nPTR_OA=nPTR_OA,
#                            l4Month=l4Month, l4Month_data=l4Month_data)



# @main.route('/dashboardLine6')
# @login_required
# def dashboard_Line6():
#     PTR6_data, PTR_lev6, nPTR6_data, nPTR_lev6,PTR6_OA, nPTR6_OA, l6Month, l6Month_data\
#         = get_data_dbline6(sheet_index=4, file_name='Reports_Template.xlsx')
#     return render_template('dashboardpsl6.html', name=current_user.name, email=current_user.email,
#                            PTR6_data=PTR6_data, nPTR6_data=nPTR6_data,
#                            PTR_lev6=PTR_lev6, nPTR_lev6=nPTR_lev6,
#                            PTR6_OA=PTR6_OA, nPTR6_OA=nPTR6_OA,
#                            l6Month=l6Month, l6Month_data=l6Month_data)


# @main.route('/dashboardLine5')
# @login_required
# def dashboard_Line5():
#     OA5_data,OApercent, OA_lev5,l5Month,l5Month_data=get_data_dbline5(sheet_index=5, file_name='Reports_Template.xlsx')
#     return render_template('dashboardpsl5.html', name=current_user.name, email=current_user.email,
#                            OA5_data=OA5_data, OApercent=OApercent,
#                            OA_lev5=OA_lev5, l5Month=l5Month, l5Month_data=l5Month_data)


# @main.route('/profile')
# @login_required
# def profile():
#    dict = get_download_db01(sheet_index=1, file_name='Reports_Template.xlsx')
#    print(dict)
#    return render_template('index.html', name=current_user.name, email=current_user.email)


@main.route('/page1')
@login_required
def page1():
     return render_template('index.html', name=current_user.name, email=current_user.email, cmp=60, kuku=[20, 40])

@main.route('/page2')
@login_required
def page2():
    #loaddata()
    return render_template('page2.html', name=current_user.name, email=current_user.email)





# @main.route('/reports')
# @login_required
# def reports():
#     dict= get_download(sheet_index=0, file_name='Reports_Template.xlsx')
# #   print(dict)
#     data= [i[1]+'.'+i[2] for i in dict]
#     data2 = [i[3]  for i in dict]
# #    print(data2)
#     return render_template('reports.html', name=current_user.name, email=current_user.email,data=data, data2=data2 )

@main.route('/getfile/<filename>')
@login_required
def getfile(filename):
    if filename[0:3] == 'NCR': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ncr\\")
    if filename[0:3] == 'SAP': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ncr\\")
    if filename[0:2] == '18': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ncr\\")
    if filename[0:2] == '19': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ncr\\")
    if filename[0:2] == '20': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ncr\\")

    if filename[0:3] == 'REX': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\rex\\")
    if filename[0:2] == '8D': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\8d\\")
    if filename[0:2] == 'PM': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\pm\\")
    if filename[0:2] == 'IR': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\ir\\")

    if filename[4:8] == 'Conf': uploads = os.path.join(current_app.root_path, "data\\rst_files_repo\\configuration\\")

    try:
        return send_from_directory(uploads, filename)
    except:
        return render_template("pages/404.html")


@main.route('/getfatfile/<filename>')
@login_required
def getfatfile(filename):
    # upload = os.path.join(current_app.root_path, "data\\rst_files_repo\\documents\\FAT\\")
    if (filename[-14:])== 'FAT Report.pdf': upload = os.path.join(current_app.root_path, "data\\rst_files_repo\\documents\\FAT\\")
    if (filename[-17:]) == 'Authorization.pdf': upload = os.path.join(current_app.root_path,
                                                                   "data\\rst_files_repo\\documents\\Shipment authorization letter\\")

    if (filename[-18:]) == 'transportation.pdf': upload = os.path.join(current_app.root_path,
                                                                   "data\\rst_files_repo\\documents\\NRTAS Reports\\")
    print(filename[-18:])
    try:
        return send_from_directory(upload, filename)

    except:
        return render_template("pages/404.html")



@main.route('/gettirfile/<filename>')
@login_required
def gettirfile(filename):

    path = "https://alstomgroup.sharepoint.com/:x:/r/sites/TrRmThreeTsy_Project/SUBSYSTEMS/RST/Shared%20Documents/RIYADH-M3-FAST-TSY-RST/14%20Corrective%20Maintenance/L4%26L6/TIR%20Train%20Incident%20Report%20Portal%20(L4%26L6)/"

    return render("https://alstomgroup.sharepoint.com/:x:/r/sites/TrRmThreeTsy_Project/SUBSYSTEMS/RST/Shared%20Documents/RIYADH-M3-FAST-TSY-RST/14%20Corrective%20Maintenance/L4%26L6/TIR%20Train%20Incident%20Report%20Portal%20(L4%26L6)/")
    # return render_template(file)
    # print (filename)
    # try:
    #     return send_from_directory(file, filename)
    # except:
    #     return render_template("pages/404.html")




def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@main.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'