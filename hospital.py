import uuid
from flask import *
from database import *
from blk import *


hospital=Blueprint('hospital', __name__)



@hospital.route('/hospital_home')
def hospital_home():
    return render_template('hospital_home.html')


@hospital.route('/hospital_view_hospital_profile')
def hospital_view_hospital_profile():
    data={}
    a="select * from hospital where hospital_id='%s'"%(session['hospital'])
    res=select(a)
    print(res,"//////////")
    data['hos']=res
    return render_template('hospital_view_hospital_profile.html',data=data)


@hospital.route('/hospital_post_request',methods=['post','get'])
def hospital_post_request():
    if 'submit' in request.form:
        t=request.form['title']
        ogname=request.form['organ_name']
        des=request.form['desc']
        re=request.files['repo']
        date=request.form['date']
        print(t,des,re,date)


        path = 'static/report/'+str(uuid.uuid4())+re.filename
        re.save(path)

        x="insert into post values(null,'%s',null,'%s','%s','%s','%s',curdate(),'pending','%s','hospital')"%(session['hospital'],t,ogname,des,date,path)
        y=insert(x)


    data={}
    a="select * from post where sender_id='%s'"%(session['hospital'])
    res=select(a)
    print(res,"///////")
    data['ho']=res
    return render_template('hospital_post_request.html',data=data)


@hospital.route('/hospital_donation_request')
def hospital_donation_request():
    data={}
    a="select * from donation inner join donor on donation.user_id = donor.login_id"
    res=select(a)
    print(res,"///////")
    data['don']=res

    if 'action' in request.args:
        act=request.args['action']
        ids=request.args['id']
        user_id=request.args['user_id']
        title=request.args['title']
        organ_name=request.args['organ_name']
        date=request.args['date']
        status=request.args['status']
        if act == 'approve':
            a="update donation set status='Approved' where donation_id='%s'" %(ids)
            b=update(a)

            with open(compiled_contract_path) as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            contract = web3.eth.contract(address=deployed_contract_address,abi=contract_abi)
            id=web3.eth.get_block_number()
            message = contract.functions.addDonation(int(ids),int(user_id),str(title),str(organ_name),str(date),str(status)).transact()
            print(message)
            return'''<script>alert("Approved");window.location='/hospital_donation_request'</script>'''

            

            
    return render_template('hospital_donation_request.html',data=data)



@hospital.route ('/hospital_requested_users')
def hospital_requested_users():
    data={}
    a="select * from post "
    res=select(a)
    print(res,"///////")
    data['ru']=res



    if 'action' in request.args:
        act=request.args['action']
        id=request.args['id']
        if act == 'accept':
            a="update post set status='approved' where post_id='%s'" %(id)
            b=update(a)
            if b:
                return'''<script>alert("Approved");window.location='/hospital_requested_users'</script>'''

        if act == 'reject':
            c="update post set status='rejecetd' where post_id='%s'" %(id)
            d=update(c)
            if d:
                return'''<script>alert("Rejected");window.location='/hospital_requested_users'</script>'''
    return render_template('hospital_requested_users.html',data=data)


@hospital.route ('/hospital_check_user_details')
def hospital_check_user_details():
    data={}
    a="SELECT * FROM `post` INNER JOIN `users` ON user_id=post.receiver_id WHERE receiver_id=1 "
    res=select(a)
    print(res,"//////")
    data['check']=res        
    return render_template('hospital_check_user_details.html',data=data)

@hospital.route('/hospital_donor_message',methods=['POST','GET'])
def hospital_donor_message():
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
        a="insert into chat values(null,'%s','%s','%s','donor','hospital',curdate(),curtime())"%(session['log'],session['id'],chat)
        insert(a)
        return redirect(url_for('hospital.hospital_donor_message'))
    return render_template("hospital_donor_message.html",data=data,name=name)

@hospital.route('/hospital_user_message',methods=['POST','GET'])
def hospital_user_message():
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
        a="insert into chat values(null,'%s','%s','%s','user','hospital',curdate(),curtime())"%(session['log'],session['id'],chat)
        insert(a)
        return redirect(url_for('hospital.hospital_user_message'))
    return render_template("hospital_user_message.html",data=data,name=name)

