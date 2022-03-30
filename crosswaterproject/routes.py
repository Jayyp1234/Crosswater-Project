from flask import render_template, url_for, flash, redirect, request,send_from_directory
from crosswaterproject import app,db,mail
from crosswaterproject.forms import ContactForm,ReportForm,FeedbackForm,RequestForm
from werkzeug.utils import secure_filename
import array, os, json
from flask_mail import Message

reciever = "okekejohnpaul12@gmail.com"
#Landing Page for Desktop View
@app.route("/") 
def home():
    return render_template('landing/index.html')
  
@app.route("/about") 
def about():
    return render_template('landing/about.html')

@app.route("/agro-product") 
def agro_product():
    return render_template('landing/agric-product.html')

@app.route("/mineral-product") 
def mineral_product():
    return render_template('landing/mineral-product.html')

@app.route("/contact", methods=['GET', 'POST']) 
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("Contact Message from {}".format(form.firstname.data), sender="livepusher8@gmail.com", recipients=[reciever])
        msg.html = '<b> Name: </b>'+form.firstname.data+' '+form.lastname.data+'<br><b> Phone Number: </b>'+form.phone_number.data+'<br>''<b> Email: </b>'+form.email.data+'<br> <b> Message: </b>'+form.message.data
        mail.send(msg)
        flash('Message Sent', 'success')
    return render_template('landing/contact.html', form = form)

@app.route("/request", methods=['GET', 'POST']) 
def request():
    form = RequestForm()
    if form.validate_on_submit():
        msg = Message("Request Message from {}".format(form.firstname.data), sender="livepusher8@gmail.com", recipients=[reciever])
        msg.html = '<b> Name: </b>'+form.firstname.data+' '+form.lastname.data+'<br><b> Phone Number: </b>'+form.phone_number.data+'<br>''<b> Email: </b>'+form.email.data+'<br> <b> Message: </b>'+form.message.data
        mail.send(msg)
        flash('Message Sent', 'success')
    return render_template('landing/request.html', form = form)
    
@app.route("/report", methods=['GET', 'POST']) 
def report():
    form = ReportForm()
    if form.validate_on_submit():
        msg = Message("Report Message from {}".format(form.firstname.data), sender="livepusher8@gmail.com", recipients=[reciever])
        msg.html = '<b> Name: </b>'+form.firstname.data+' '+form.lastname.data+'<br><b> Phone Number: </b>'+form.phone_number.data+'<br>''<b> Email: </b>'+form.email.data+'<br> <b> Report: </b>'+form.message.data
        mail.send(msg)
        flash('Message Sent', 'success')
    return render_template('landing/report.html', form = form)

@app.route("/feedback", methods=['GET', 'POST']) 
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        msg = Message("Feedback Message from Anonymous", sender="livepusher8@gmail.com", recipients=[reciever])
        msg.html = '<b> Title: </b>'+form.title.data+'<br><b> Details: </b>'+form.message.data
        mail.send(msg)
        flash('Message Sent', 'success')
    return render_template('landing/feedback.html', form = form)

@app.route("/product/seasame") 
def product_sesame():
    return render_template('product/sesame.html')

@app.route("/product/shea") 
def product_shea():
    return render_template('product/shea.html')

@app.route("/product/blackstone") 
def product_blackstone():
    return render_template('product/blackstone.html')

@app.route("/product/cashew") 
def product_cashew():
    return render_template('product/cashew.html')

@app.route("/product/cocoa") 
def product_cocoa():
    return render_template('product/cocoa.html')

@app.route("/product/ginger") 
def product_ginger():
    return render_template('product/ginger.html')

@app.route("/product/hibiscus") 
def product_hibiscus():
    return render_template('product/hibiscus.html')

@app.route("/product/peanuts") 
def product_peanuts():
    return render_template('product/peanuts.html')

@app.route("/product/tigernut") 
def product_tigernut():
    return render_template('product/tigernut.html')


@app.route("/product/lithium") 
def product_lithium():
    return render_template('product/lithium.html')

@app.route("/product/mica") 
def product_mica():
    return render_template('product/mica.html')

@app.route("/product/lead") 
def product_lead():
    return render_template('product/lead.html')

@app.route("/product/copper") 
def product_copper():
    return render_template('product/copper.html')

@app.route("/product/zinc") 
def product_zinc():
    return render_template('product/zinc.html')

@app.route("/product/manganese") 
def product_manganese():
    return render_template('product/manganese.html')

@app.route("/product/gemstones") 
def product_gemstones():
    return render_template('product/gemstones.html')





@app.route("/privacy") 
def privacy():
    return render_template('landing/privacy.html')

@app.route("/search") 
def search():
    return render_template('search.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/error.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html', title='Internal Server Error'), 500
