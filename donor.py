from flask import *
from database import *

donor=Blueprint('donor', __name__)

@donor.route('/donor_home')
def donor_home():
    return render_template('donor_home.html')


@donor.route('/donor_update_preferences')
def donor_update_preferences():

    data={}
    a="select * from post "
    res=select(a)
    print(res,"///////")
    data['ho']=res

    return render_template('donor_update_preferences.html',data=data)


@donor.route('/donor_view_donation_requests')
def donor_view_donation_requests():
    data={}
    a="select * from donation  "
    res=select(a)
    print(res,"///////")
    data['do']=res

    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
        if act == 'accept':
            a="update donation set status='approved' where donation_id='%s'" %(id)
            b=update(a)
            if b:
                return'''<script>alert("Approved");window.location='/donor_view_donation_requests'</script>'''

        if act == 'reject':
            c="update donation set status='rejected' where donation_id='%s'" %(id)
            d=update(c)
            if d:
                return'''<script>alert("Rejected");window.location='/donor_view_donation_requests'</script>'''

    return render_template('donor_view_donation_requests.html',data=data)

@donor.route('/donor_View_hospital')
def donor_View_hospital():
    data={}
    a="select * from hospital "
    res=select(a)
    print(res,"//////////")
    data['hosp']=res

    return render_template('donor_View_hospital.html',data=data)

@donor.route('/donor_send_donation_request',methods=['post','get'])
def donor_send_donation_request():
    if 'submit' in request.form:
        t=request.form['title']
        organ=request.form['og']
        print(t,organ)
        
        qry="insert into  donation values(null,'%s','%s','%s',curdate(),'pending')"%(session['donor'],t,organ)
        insert(qry)

    data={}
    a="select * from donation where user_id='%s'"%(session['donor'])
    res=select(a)
    print(res,"///////")
    data['do']=res

    return render_template('donor_send_donation_request.html',data=data)

@donor.route('/donor_view_message',methods=['POST','GET'])
def donor_view_message():
    data={}
    name=''
    if 'action' in request.args:
        action=request.args['action']
        session['id']=request.args['id']
        name=request.args['name']

    else:
        action=None
    
    f="SELECT * FROM chat WHERE sender_id='%s' AND receiver_id='%s' UNION SELECT * FROM chat WHERE sender_id='%s' AND receiver_id='%s' ORDER BY date , time"%(session['id'],session['log'],session['log'],session['id'])
    rg=select(f)
    print(rg)
    data['rg']=rg

    if 'submit' in request.form:
        chat=request.form['chat']
        print(chat,"000000000000000000000000000000000000000000000000")
        a="insert into chat values(null,'%s','%s','%s','hospital','donor',curdate(),curtime())"%(session['log'],session['id'],chat)
        insert(a)
        return redirect(url_for('donor.donor_view_message'))
    return render_template("donor_view_message.html",data=data,name=name)


