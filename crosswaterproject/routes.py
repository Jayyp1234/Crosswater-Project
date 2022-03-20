from flask import render_template, url_for, flash, redirect, request
from crosswaterproject import app,db
from werkzeug.utils import secure_filename
import array, os, json


#Landing Page for Desktop View
@app.route("/") 
def home():
    return render_template('landing/index.html')
  

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/error.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html', title='Internal Server Error'), 500
