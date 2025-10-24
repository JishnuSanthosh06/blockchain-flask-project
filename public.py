from flask import *

from database import *

public =Blueprint('public', __name__)

@public.route('/')
def home():
    return render_template("home.html")

@public.route('/login',methods=['post','get'])
def login():
    if 'submit' in request.form:
        
        u_name=request.form['username']
        pwd=request.form['password']
        
        print(u_name,pwd)

        z="select * from login where username='%s' and password='%s'"%(u_name,pwd)
        res=select(z)
        session['log']=res[0]['login_id']

    
        if res:
            if res[0]['usertype']=='admin':
                return redirect(url_for('admin.admin_home'))
            
            
            if res[0]['usertype']=='hospital':
                qry="select * from hospital where login_id='%s'"%(session['log'])
                res=select(qry)
                session['hospital']=res[0]['hospital_id']

                return redirect(url_for('hospital.hospital_home'))
            
            if res[0]['usertype']=='user':
                qry="select * from users where login_id='%s'"%(session['log'])
                res=select(qry)
                session['user']=res[0]['user_id']

                return redirect(url_for('users.users_home'))
            
            if res[0]['usertype']=='donor':
                qry="select * from donor where login_id='%s'"%(session['log'])
                res=select(qry)
                session['donor']=res[0]['login_id']

                return redirect(url_for('donor.donor_home'))
            
            if res[0]['usertype']=='police':
                q="select * from police where login_id='%s'"%(session['log'])
                r=select(q)
                if r:
                    session['policeid']=r[0]['police_id']
                return redirect(url_for('police.police_home'))
        
        else:
            return """<script>alert("invalid user");window.location='/'</script>"""


    
    return render_template('login.html')


@public.route('/register',methods=['post','get'])
def register():
    if 'submit' in request.form:
       
        h_name=request.form['hospital_name']
        pl=request.form['place']
        e=request.form['email']
        ph=request.form['phone']
        u_name=request.form['u_name']
        pw=request.form['pwd']

        x="insert into login values(null,'%s','%s','pending')"%(u_name,pw)
        y=insert(x)
        a="insert into hospital values(null,'%s','%s','%s','%s','%s')"%(y,h_name,pl,e,ph)
        b=insert(a)
        if b:
            return'''<script>alert("Registered Successfully.Waiting for approval");window.location='/'</script>'''

        print(h_name,pl,e,ph,u_name,pw)

    return render_template('register.html')


@public.route('/users_register',methods=['post','get'])
def users_register():

    
    if 'reg' in request.form:
        fname=request.form['f_name']
        lname=request.form['l_name']
        e=request.form['email']
        ph=request.form['phone']
        pl=request.form['place']
        u_name=request.form['u_name']
        pw=request.form['pwd']

        x="insert into login values(null,'%s','%s','user')"%(u_name,pw)
        y=insert(x)
        a="insert into users values(null,'%s','%s','%s','%s','%s','%s')"%(y,fname,lname,e,ph,pl)
        b=insert(a)
        if b:
            return'''<script>alert("Registered Successfully.Waiting for approval");window.location='/'</script>'''

        
    return render_template('users_register.html')

@public.route('/donor_register',methods=['post','get'])
def donor_register():

    if 'reg' in request.form:
        fname=request.form['f_name']
        lname=request.form['l_name']
        e=request.form['email']
        ph=request.form['phone']
        pl=request.form['place']
        u_name=request.form['u_name']
        pw=request.form['pwd']

        x="insert into login values(null,'%s','%s','donor')"%(u_name,pw)
        y=insert(x)
        a="insert into donor values(null,'%s','%s','%s','%s','%s','%s')"%(y,fname,lname,e,ph,pl)
        b=insert(a)
        if b:
            return'''<script>alert("Registered Successfully.");window.location='/'</script>'''
  
    return render_template('donor_register.html')

@public.route('/police_register',methods=['post','get'])
def police_register():

    if 'reg' in request.form:
        stname=request.form['st_name']
        e=request.form['email']
        ph=request.form['phone']
        pl=request.form['place']
        u_name=request.form['u_name']
        pw=request.form['pwd']

        x="insert into login values(null,'%s','%s','police')"%(u_name,pw)
        y=insert(x)
        a="insert into police values(null,'%s','%s','%s','%s','%s')"%(y,stname,e,ph,pl)
        b=insert(a)
        if b:
            return'''<script>alert("Registered Successfully");window.location='/'</script>'''
        
    return render_template('police_register.html')
