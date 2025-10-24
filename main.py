from flask import *
from public import public
from admin import admin
from hospital import hospital
from users import users
from donor import donor
from police import police

app=Flask(__name__) 

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(hospital)
app.register_blueprint(users)
app.register_blueprint(donor)
app.register_blueprint(police)

app.secret_key="sdfghjm"

app.run(debug=True)
