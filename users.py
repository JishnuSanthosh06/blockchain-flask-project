import uuid
from flask import *
from database import *

users=Blueprint('users', __name__)

@users.route('/users_home')
def users_home():
    return render_template('users_home.html')

@users.route('/users_view_hospitals')
def users_View_hospital():
    data={}
    a="select * from hospital "
    res=select(a)
    print(res,"//////////")
    data['hosp']=res
    return render_template('users_view_hospitals.html',data=data)

@users.route('/users_post_request',methods=['post','get'])
def users_post_request():

    if 'submit' in request.form:
        t=request.form['title']
        ogname=request.form['organ_name']
        des=request.form['desc']
        re=request.files['repo']
        date=request.form['date']
        print(t,des,re,date)


        path = 'static/report/'+str(uuid.uuid4())+re.filename
        re.save(path)

        x="insert into post values(null,'%s',null,'%s','%s','%s','%s',curdate(),'pending','%s','user')"%(session['user'],t,ogname,des,date,path)
        y=insert(x)

    data={}
    a="select * from post where sender_id='%s'"%(session['user'])
    res=select(a)
    print(res,"///////")
    data['ho']=res
    return render_template('users_post_request.html',data=data)

@users.route('/users_view_others_posted_request')
def users_view_others_posted_request():
    data={}
    a="select * from post where sender_id!='%s'"%(session['user'])
    res=select(a)
    print(res,"///////")
    data['ho']=res

    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
        if act == 'accept':
            a="update post set status='approved' where post_id='%s'" %(id)
            b=update(a)
            if b:
                return'''<script>alert("Approved");window.location='/users_view_others_posted_request'</script>'''

        if act == 'reject':
            c="update post set status='rejecetd' where post_id='%s'" %(id)
            d=update(c)
            if d:
                return'''<script>alert("Rejected");window.location='/users_view_others_posted_request'</script>'''
    return render_template('users_view_others_posted_request.html',data=data)

@users.route('/users_send_donation_request',methods=['post','get'])
def users_send_donation_request():
    if 'submit' in request.form:
        t=request.form['title']
        organ=request.form['og']
        print(t,organ)
        
        qry="insert into  donation values(null,'%s','%s','%s',curdate(),'pending')"%(session['user'],t,organ)
        insert(qry)

    data={}
    a="select * from donation where user_id='%s'"%(session['user'])
    res=select(a)
    print(res,"///////")
    data['do']=res

    return render_template('users_send_donation_request.html',data=data)


@users.route('/users_view_others_donation_request')
def users_view_others_donation_request():
    data={}
    a="select * from donation where user_id!='%s'"%(session['user'])
    res=select(a)
    print(res,"///////")
    data['do']=res

    return render_template('users_view_others_donation_request.html',data=data)

@users.route('/users_send_complaints',methods=['post','get'])
def users_send_complaints():
    if 'submit' in request.form:
        com=request.form['complaint']
        print(com)
        a="insert into complaints values(null,'%s','%s','pending',curdate())"%(session['user'],com)
        insert(a)

    data={}
    a="select * from complaints where user_id='%s'"%(session['user'])
    res=select(a)
    print(res,"//////////")
    data['comp']=res

    return render_template('users_send_complaints.html',data=data)


@users.route('/user_view_message',methods=['POST','GET'])
def user_view_message():
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
        a="insert into chat values(null,'%s','%s','%s','hospital','user',curdate(),curtime())"%(session['log'],session['id'],chat)
        insert(a)
        return redirect(url_for('users.user_view_message'))
    return render_template("user_view_message.html",data=data,name=name)