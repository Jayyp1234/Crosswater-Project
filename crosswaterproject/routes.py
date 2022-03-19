
from flask import render_template, url_for, flash, redirect, request ,send_from_directory,make_response
from shopnstuff import app, s3_resource,db,bcrypt
from .forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm, BrandRegistrationForm
from .models import Images, Transactions, User,Category,SubCategory,Item,Images,Orders,Brand
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import array, os, json

BUCKET_NAME = 'shopnstuffs'

#Landing Page for Desktop View
@app.route("/") 
@app.route("/home")
def home():
    category = {
    }
    for i in Category.query.order_by(Category.title).all(): 
        data = SubCategory.query.join(Category, SubCategory.category_id == Category.id).filter(Category.id == i.id).order_by(SubCategory.title).all()
        category[i.title] = data
    ##my_bucket = s3_resource.Bucket(BUCKET_NAME)
    ##summaries = my_bucket.objects.filter(Prefix="carousel/")
    my_bucket = []
    summaries = []
    return render_template('landing/index.html',my_bucket=my_bucket, files=summaries,category = category,title='Online Shopping for Groceries, Appliances &amp; More!')
        
#Landing Page for Mobile View
@app.route("/mobile_home")
def mobile_home():
   ##my_bucket = s3_resource.Bucket(BUCKET_NAME)
    ##summaries = my_bucket.objects.filter(Prefix="carousel/")
    my_bucket = []
    summaries = []
    return render_template('landing/index_mobile.html',my_bucket=my_bucket, files=summaries)
   
@app.route("/search")
def search():
    ##my_bucket = s3_resource.Bucket(BUCKET_NAME)
    ##summaries = my_bucket.objects.filter(Prefix="carousel/")
    my_bucket = []
    summaries = []
    return render_template('search/search.html',my_bucket=my_bucket, files=summaries)
   
@app.route("/categories")
def category():
    #Object to be Created.
    category = {
    }
    #Querying and Creating a new Object with Category and Sub Categories Embedded in it
    for i in Category.query.order_by(Category.title).all(): 
        data = SubCategory.query.join(Category, SubCategory.category_id == Category.id).filter(Category.id == i.id).order_by(SubCategory.title).all()
        category[i.title] = data
    return render_template('categories/category.html',category=category)

@app.route("/sub_category/<name>")
def sub_category_data(name=''):
    category = Item.query.join(Category, SubCategory.category_id == Category.id).filter(SubCategory.title).order_by(SubCategory.title).all()
    return render_template('categories/sub_category.html')

@app.route("/sub_category")
def sub_category():
    category = SubCategory.query.join(Category, SubCategory.category_id == Category.id).order_by(SubCategory.title).all()
    return render_template('categories/sub_category.html')
   
@app.route("/display_item")
def display():
    return render_template('display/index.html')
   






#ADMIN DASHBOARD 
@app.route("/admin")
def admin():
    if current_user.is_authenticated and current_user.role != "admin":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        orders = len(Orders.query.all())
        item = len(Item.query.all())
        sales = 0
        for i in Transactions.query.all():
            sales = sales + int(i.price)

        return render_template('admin/dashboard.html', item = item, orders = orders, sales = sales)

#ADMIN CRUD 
@app.route("/admin/categories")
@app.route("/delete-subcategory/<id>")
@app.route("/delete-category/<name>")
@app.route("/update-subcategory", methods=['POST','GET'])
@app.route("/update-category", methods=['POST','GET'])
@app.route("/create-subcategory", methods=['POST','GET'])
@app.route("/create-category", methods=['POST','GET'])
def editCategory(id='',name=''):
    category = {
    }
    for i in Category.query.order_by(Category.title).all(): 
        data = SubCategory.query.join(Category, SubCategory.category_id == Category.id).filter(Category.id == i.id).order_by(SubCategory.title).all()
        category[i.title] = data

    if request.method == "POST":
        form = request.form
        if 'title_update' in form:
            id = request.form['id_update']
            title = request.form['title_update']
            data = SubCategory.query.filter_by(id=id).first()
            print(data)
            data.title = title
            db.session.commit()
            return redirect(url_for('editCategory'))
        elif 'title_create' in form:
            id = request.form['category_id']
            title = request.form['title_create']
            data = Category.query.filter_by(title=id).first()
            subcategory = SubCategory(
                title= title,
                category_id = data.id
            )
            db.session.add(subcategory)
            db.session.commit()
            return redirect(url_for('editCategory'))
        elif 'title_create_category' in form:
            title = request.form['title_create_category']
            category = Category(
                title= title
            )
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('editCategory'))
        else:
            id = request.form['id1_update']
            title = request.form['title1_update']
            data = Category.query.filter_by(title=id).first()
            data.title = title
            db.session.commit()
            return redirect(url_for('editCategory'))
    if id:
        data = SubCategory.query.filter_by(id = id).first()
        print(data)
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('editCategory'))
    elif name:
        data = Category.query.filter_by(title = name).first()
        for i in SubCategory.query.filter_by(category_id = data.id).all():
            db.session.delete(i)
            db.session.commit()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('editCategory'))
    return render_template('admin/page-categories.html',title='Edit - Categories',category=category)

@app.route("/admin/products")
@app.route("/delete-products/<id>")
def admin_products(id=''):
    if current_user.is_authenticated and current_user.role != "admin":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        items = Item.query.join(Images, Item.id == Images.item_id).all()
        category = Category.query.order_by(Category.title).all()
        if id:
            data = Item.query.filter_by(id = id).first()
            for i in data.image:
                pin = Images.query.filter_by(id = i.id).first()
                print(pin)
                db.session.delete(pin)
                db.session.commit()
            db.session.delete(data)
            db.session.commit()

            return redirect(url_for('admin_products'))
        return render_template('admin/page-products-grid-2.html', items = items, bucket = BUCKET_NAME, category = category)

@app.route("/admin/add-products", methods=['POST','GET'])
def admin_add_products(id=''):
    if current_user.is_authenticated and current_user.role != "admin":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        category = Category.query.order_by(Category.title).all()
        subcategory = SubCategory.query.order_by(SubCategory.title).all()
        if request.method == "POST":
            form = request.form
            title = request.form['title']
            sub_category = request.form['subcategory_id']
            initial_price = request.form['initial_price']
            final_price = request.form['final_price']
            quantity = request.form['quantity']
            details = request.form['quick_details']
            tags = request.form['tags']
            color = request.form['color']
            specification = request.form['specification']
            warranty = request.form['warranty']
            data = Item(title = title, brand_id = 1,warranty = warranty, specification = specification, subcategory_id = sub_category, initial_price = initial_price, final_price = final_price, quantity = quantity, detail = details, color = color, tags = tags)
            db.session.add(data)
            db.session.commit()

            file = request.files["image"]
            if file.filename == "":
                return "Please select a file"
            if file:
                picture_file = save_picture(file)
                image_url = url_for('static', filename='uploads/' + picture_file)
                file = secure_filename(file.filename)
                s3_resource.upload_file(
                    Filename = f'{os.getcwd()}/shopnstuff{image_url}',
                    Bucket=BUCKET_NAME,
                    Key = file,
                    ExtraArgs={
                        "ACL": "public-read"
                    }
                )
                id = Item.query.order_by(Item.id.desc()).first().id
                print(id)
                data1 = Images(item_id = id, address = picture_file)
                print(data1)
                db.session.add(data1)
                db.session.commit()
                os.remove(f'{os.getcwd()}/shopnstuff{image_url}')
        
        return render_template('admin/page-form-product-1.html', title='Items',category=category, subcategory=subcategory)

def save_picture(picture_file):
    picture = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/uploads', picture)
    picture_file.save(picture_path)
    return picture


@app.route("/admin/ads")
def ads():
    orders = Orders.query.all()
    return render_template('admin/page-ads.html', title='Create Ads')

@app.route("/admin/orders")
def orders():
    orders = Orders.query.all()
    return render_template('admin/page-orders-1.html', title='Orders', orders = orders)

@app.route("/admin/orders-details/<id>")
def orders_details(id=''):
    return render_template('admin/page-orders-detail.html', title='Orders - Details')

@app.route("/admin/transactions")
def transaction():
    trans = Transactions.query.all()
    return render_template('admin/page-transactions-B.html', title='Transactions',trans= trans)

@app.route("/admin/reviews")
def reviews():
    return render_template('admin/page-reviews.html', title='Reviews')

@app.route("/admin/settings")
def settings():
    return render_template('admin/page-settings-1.html', title='Settings')

@app.route("/admin/sellers")
def sellers():
    brand = Brand.query.all()
    return render_template('admin/page-sellers-cards.html', title='Sellers', sellers = brand, bucket=BUCKET_NAME )

@app.route("/admin/seller-detail/<int:id>")
def seller_detail(id=''):
    brand = Brand.query.filter_by(id = id).first()
    items = Item.query.filter_by(brand_id = id).join(Images, Item.id == Images.item_id).all()
    return render_template('admin/page-seller-detail.html', title='Seller-Detail', seller = brand, bucket=BUCKET_NAME, items = items )

























#SELLER SECTION

@app.route('/seller-login', methods=['POST','GET'])
def seller_login():
    login = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('seller_dashboard'))
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login.password.data):
            login_user(user, remember=login.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('seller/login.html', title='Seller Login Page', form = login )

@app.route('/seller/register', methods=['POST','GET'])
def register_seller():
    register = BrandRegistrationForm()
    if register.validate_on_submit():
        user_email = register.email.data
        hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        if User.query.filter_by(email=user_email).first() == user_email:
            user = User.query.filter_by(email=user_email).first()
            file = request.files["brand_logo"]
            if file.filename == "":
                return "Please select a file"
            if file:
                picture_file = save_picture(file)
                image_url = url_for('static', filename='uploads/' + picture_file)
                file = secure_filename(file.filename)
                s3_resource.upload_file(
                    Filename = f'{os.getcwd()}/shopnstuff{image_url}',
                    Bucket=BUCKET_NAME,
                    Key = file,
                    ExtraArgs={"ACL": "public-read"}
                )
                user.name = register.name.data.lower()
                user.password = hashed_password
                user.role = 'seller'
                brand = Brand(
                    name = register.name.data.lower(),
                    display_name = register.brand_name.data.lower(),
                    email = register.email.data.lower(),
                    image_ref = picture_file,
                    bank_name = register.account_name.data.lower(),
                    bank_type = register.account_type.data.lower(),
                    account_no = register.account_number.data.lower(),
                    password = hashed_password,
                    payment_status = 'not paid'
                )
            db.session.add(user)
            db.session.add(brand)
            db.session.commit()
            return redirect(url_for('seller_payment', email = register.email.data.lower() ,**request.args))
        else:
            hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
            file = request.files["brand_logo"]
            if file.filename == "":
                return "Please select a file"
            if file:
                picture_file = save_picture(file)
                image_url = url_for('static', filename='uploads/' + picture_file)
                file = secure_filename(file.filename)
                s3_resource.upload_file(
                    Filename = f'{os.getcwd()}/shopnstuff{image_url}',
                    Bucket=BUCKET_NAME,
                    Key = file,
                    ExtraArgs={"ACL": "public-read"}
                )
                user = User(
                    name = register.name.data.lower(),
                    email = register.email.data.lower(),
                    password = hashed_password,
                    role='seller',
                    email_preference = 'yes'
                )
                brand = Brand(
                    name = register.name.data.lower(),
                    display_name = register.brand_name.data.lower(),
                    email = register.email.data.lower(),
                    image_ref = picture_file,
                    bank_name = register.account_name.data.lower(),
                    bank_type = register.account_type.data.lower(),
                    account_no = register.account_number.data.lower(),
                    password = hashed_password,
                    payment_status = 'not paid'
                )
            db.session.add(user)
            db.session.add(brand)
            db.session.commit()
            msg=''
            msgprop = False
        return redirect(url_for('seller_payment', email = register.email.data.lower() ,**request.args))
    return render_template('seller/register.html', title='Seller Register Page', form = register)

@app.route('/seller/register-pay', methods=['POST','GET'])
def seller_payment():
    data = Brand.query.filter_by(email = request.args['email']).first()
    if request.method == "POST":
        data = Brand.query.filter_by(email = request.form['email']).first()
        data1 = User.query.filter_by(email = request.form['email']).first()
        email = request.form['email']
        ref = request.form['transation']
        id = data1.id
        price = 500
        data.status = 'paid'
        trans = Transactions(transation_id = ref,user_id = id,payment_type = 'Seller Registration Fee',price = 500)
        db.session.add(trans)
        db.session.commit()
        login_user(data1)
        return redirect(url_for('seller_dashboard'))
    return render_template('/seller/registrationPayment.html', info = data)

@app.route('/seller/dashboard')
def seller_dashboard():
    if current_user.is_authenticated and current_user.role != "seller":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        active_user = len(User.query.filter_by(role = 'user').all())
        active_seller = len(User.query.filter_by(role = 'seller').all())
        return render_template('seller/dashboard.html', user = active_user, admin=active_seller)

@app.route("/seller/products")
@app.route("/delete-products/<id>")
def seller_products(id=''):
    if current_user.is_authenticated and current_user.role != "seller":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        data = Brand.query.filter_by(email = current_user.email).first()
        items = Item.query.filter_by(brand_id = data.id).join(Images, Item.id == Images.item_id).all()
        category = Category.query.order_by(Category.title).all()
        if id:
            data = Item.query.filter_by(id = id).first()
            for i in data.image:
                pin = Images.query.filter_by(id = i.id).first()
                print(pin)
                db.session.delete(pin)
                db.session.commit()
            db.session.delete(data)
            db.session.commit()

            return redirect(url_for('seller_products'))
        return render_template('seller/page-products-grid-2.html', items = items, bucket = BUCKET_NAME, category = category)

@app.route("/seller/add-products", methods=['POST','GET'])
def seller_add_products(id=''):
    if current_user.is_authenticated and current_user.role != "seller":
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('login'))
    else:
        category = Category.query.order_by(Category.title).all()
        subcategory = SubCategory.query.order_by(SubCategory.title).all()
        if request.method == "POST":
            form = request.form
            title = request.form['title']
            sub_category = request.form['subcategory_id']
            initial_price = request.form['initial_price']
            final_price = request.form['final_price']
            quantity = request.form['quantity']
            details = request.form['quick_details']
            tags = request.form['tags']
            color = request.form['color']
            brand_id = Brand.query.filter_by(email = current_user.email).first()
            specification = request.form['specification']
            warranty = request.form['warranty']
            data = Item(title = title, warranty = warranty, brand_id = brand_id.id,specification = specification, subcategory_id = sub_category, initial_price = initial_price, final_price = final_price, quantity = quantity, detail = details, color = color, tags = tags, region='normal')
            db.session.add(data)
            db.session.commit()

            file = request.files["image"]
            if file.filename == "":
                return "Please select a file"
            if file:
                picture_file = save_picture(file)
                image_url = url_for('static', filename='uploads/' + picture_file)
                file = secure_filename(file.filename)
                s3_resource.upload_file(
                    Filename = f'{os.getcwd()}/shopnstuff{image_url}',
                    Bucket=BUCKET_NAME,
                    Key = file,
                    ExtraArgs={
                        "ACL": "public-read"
                    }
                )
                id = Item.query.order_by(Item.id.desc()).first().id
                print(id)
                data1 = Images(item_id = id, address = picture_file)
                print(data1)
                db.session.add(data1)
                db.session.commit()
                os.remove(f'{os.getcwd()}/shopnstuff{image_url}')
        
        return render_template('seller/page-form-product-1.html', title='Items',category=category, subcategory=subcategory)

def save_picture(picture_file):
    picture = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/uploads', picture)
    picture_file.save(picture_path)
    return picture



















##AUTHENTICATION DETAILS

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = RequestResetForm()
        return render_template('auth/reset_password.html', form = form)

@app.route("/reset_token", methods=['GET', 'POST'])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = ResetPasswordForm()
        return render_template('auth/reset_token.html', form = form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = register.email.data
        users = User.query.all()
        print(register.data)
        if User.query.filter_by(email=user_email).first() == user_email:
            msg='Email Address already Exists'
            msgprop = True
        else:
            hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
            user = User(username=register.username.data.lower(),email=register.email.data.lower(),password=hashed_password)
            db.session.add(user)
            db.session.commit()
            msg=''
            msgprop = False
        for data in register.data:
            data = ''
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = LoginForm()
    register = RegistrationForm()
    msg = ''
    msgprop = False
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login.password.data):
            login_user(user, remember=login.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=login,register=register)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/error.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html', title='Internal Server Error'), 500
