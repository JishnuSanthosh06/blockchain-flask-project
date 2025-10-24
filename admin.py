from flask import *
from database import *

admin=Blueprint('admin', __name__)


@admin.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')


@admin.route('/admin_View_hospital')
def admin_View_hospital():
    data={}
    a="select * from hospital inner join login using(login_id)"
    res=select(a)
    print(res,"//////////")
    data['hosp']=res

    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
        if act == 'approve':
            a="update login set usertype='hospital' where login_id='%s'" %(id)
            b=update(a)
            if b:
                return'''<script>alert("Approved");window.location='/admin_View_hospital'</script>'''

        if act == 'reject':
            c="update login set usertype='rejected' where login_id='%s'" %(id)
            d=update(c)
            if d:
                return'''<script>alert("Rejected");window.location='/admin_View_hospital'</script>'''

    
    return render_template('admin_View_hospital.html',data=data)


@admin.route('/admin_View_post_and_status')
def admin_View_post_and_status():
    data={}
    a="select * from post"
    res=select(a)
    print(res,"//////////")
    data['vps']=res
    return render_template('admin_View_post_and_status.html',data=data)


@admin.route('/admin_View_donors')
def admin_View_donors():
    data={}
    a="select * from donor"
    res=select(a)
    print(res,"//////////")
    data['don']=res
    return render_template('admin_View_donors.html',data=data)



@admin.route('/admin_View_users')
def admin_View_users():
    data={}
    a="select * from users"
    res=select(a)
    print(res,"//////////")
    data['user']=res
    return render_template('admin_View_users.html',data=data)



@admin.route('/admin_View_complaints')
def admin_View_complaints():
    data={}
    a="select * from complaints"
    res=select(a)
    print(res,"//////////")
    data['com']=res

    return render_template('admin_View_complaints.html',data=data)


@admin.route('/admin_send_reply', methods=['post','get'])
def admin_send_reply():
    com_id=request.args['complaint_id']
    if 'submit' in request.form:
        r=request.form['reply']
        print(r,"////////////")

        qry="update complaints set reply='%s' where complaint_id='%s'"%(r,com_id)
        res=update(qry)
        return'''<script>alert("Complaint sent");window.location='/admin_View_complaints'</script>'''
    return render_template('admin_send_reply.html')
