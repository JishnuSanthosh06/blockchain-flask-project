from flask import *
from database import *

police=Blueprint('police', __name__)

@police.route('/police_home')
def police_home():
    return render_template('police_home.html')

@police.route('/police_profile_management')
def police_profile_management():
    data={}
    a="select * from police where police_id='%s'"%(session['policeid'])
    res=select(a)
    print(res,"//////////")
    data['pol']=res
    return render_template('police_profile_management.html',data=data)

@police.route('/police_edit_profile', methods=['post','get'])
def police_edit_profile():
    data={}
    a="select * from police where police_id='%s'"%(session['policeid'])
    res=select(a)
    print(res,"//////////")
    data['pol']=res
    
    if 'edit' in request.form:
        st=request.form['station_Name']
        e=request.form['email']
        ph=request.form['phone']
        pl=request.form['place']
        print(st,e,ph,pl)

        x="update police set station_Name='%s',email='%s',phone='%s',place='%s' where police_id='%s' "%(st,e,ph,pl,session['policeid'])
        y=update(x)
        if y:
            return """<script>alert("edited successfully");window.location='/police_edit_profile'</script>"""
        
    return render_template("police_edit_profile.html",data=data)


@police.route('/police_verify_oragan_cases')
def police_verify_oragan_cases():
    data={}
    a="select * from post order by date desc"
    res=select(a)
    print(res,"///////")
    data['ru']=res



    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
        if act == 'Verify':
            a="update post set status='Verified' where post_id='%s'" %(id)
            b=update(a)
            if b:
                return'''<script>alert("Verified");window.location='/police_verify_oragan_cases'</script>'''

        if act == 'Reject':
            c="update post set status='Rejected' where post_id='%s'" %(id)
            d=update(c)
            if d:
                return'''<script>alert("Rejected");window.location='/police_verify_oragan_cases'</script>'''

    return render_template('police_verify_oragan_cases.html',data=data)

@police.route('/police_view_hospital_requests')
def police_view_hospital_requests():
    data={}
    a="select * from post where type='hospital'"
    res=select(a)
    print(res,"///////")
    data['ho']=res
    
    return render_template('police_view_hospital_requests.html',data=data)


