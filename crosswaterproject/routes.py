from flask import render_template, url_for, flash, redirect, request
from crosswaterproject import app,db
from werkzeug.utils import secure_filename
import array, os, json


#Landing Page for Desktop View
@app.route("/") 
def home():
    return render_template('landing/index.html')
  
@app.route("/about") 
def about():
    return render_template('landing/about.html')


@app.route("/product") 
def product():
    return render_template('landing/product.html')

@app.route("/contact") 
def contact():
    return render_template('landing/contact.html')

@app.route("/request") 
def request():
    return render_template('landing/request.html')
    
@app.route("/report") 
def report():
    return render_template('landing/report.html')

@app.route("/feedback") 
def feedback():
    return render_template('landing/feedback.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/error.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html', title='Internal Server Error'), 500
