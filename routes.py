from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Product, Purchase, Sale
from datetime import datetime, timedelta
from sqlalchemy import func, and_
import qrcode
import os
import uuid
from io import BytesIO

def generate_qr_code(sku, product_name):
    """Generate QR code for a product and save it to static/qrcodes/"""
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code (SKU)
    qr.add_data(sku)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image
    filename = f"{sku}.png"
    filepath = os.path.join('static', 'qrcodes', filename)
    img.save(filepath)
    
    return f"qrcodes/{filename}"

def generate_sku():
    """Generate a unique SKU for a product"""
    return f"PRD{str(uuid.uuid4())[:8].upper()}"

@app.before_request
def require_login():
    allowed_routes = ['login', 'static', 'search_product_by_sku']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Get key metrics
    total_products = Product.query.count()
    total_sales_today = db.session.query(func.sum(Sale.total_price)).filter(
        func.date(Sale.created_at) == datetime.utcnow().date()
    ).scalar() or 0
    
    total_sales_month = db.session.query(func.sum(Sale.total_price)).filter(
        func.extract('month', Sale.created_at) == datetime.utcnow().month,
        func.extract('year', Sale.created_at) == datetime.utcnow().year
    ).scalar() or 0
    
    low_stock_products = Product.query.filter(Product.stock_quantity <= Product.min_stock).all()
    
    # Recent sales
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         total_sales_today=total_sales_today,
                         total_sales_month=total_sales_month,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales)

@app.route('/products')
def products():
    search = request.args.get('search', '')
    if search:
        products = Product.query.filter(
            Product.name.ilike(f'%{search}%') | 
            Product.category.ilike(f'%{search}%')
        ).all()
    else:
        products = Product.query.all()
    
    return render_template('products.html', products=products, search=search)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        stock_quantity = int(request.form['stock_quantity'])
        min_stock = int(request.form['min_stock'])
        
        product = Product(
            name=name,
            category=category,
            price=price,
            stock_quantity=stock_quantity,
            min_stock=min_stock
        )
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = float(request.form['price'])
        product.stock_quantity = int(request.form['stock_quantity'])
        product.min_stock = int(request.form['min_stock'])
        product.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

@app.route('/inventory')
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@app.route('/purchases')
def purchases():
    purchases = Purchase.query.order_by(Purchase.created_at.desc()).all()
    return render_template('purchases.html', purchases=purchases)

@app.route('/purchases/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        unit_cost = float(request.form['unit_cost'])
        supplier = request.form['supplier']
        notes = request.form['notes']
        
        total_cost = quantity * unit_cost
        
        purchase = Purchase(
            product_id=product_id,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            supplier=supplier,
            notes=notes
        )
        
        # Update product stock
        product = Product.query.get(product_id)
        product.stock_quantity += quantity
        product.updated_at = datetime.utcnow()
        
        db.session.add(purchase)
        db.session.commit()
        flash('Purchase recorded successfully!', 'success')
        return redirect(url_for('purchases'))
    
    products = Product.query.all()
    return render_template('add_purchase.html', products=products)

@app.route('/sales')
def sales():
    sales = Sale.query.order_by(Sale.created_at.desc()).all()
    return render_template('sales.html', sales=sales)

@app.route('/sales/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        unit_price = float(request.form['unit_price'])
        customer_name = request.form['customer_name']
        notes = request.form['notes']
        
        product = Product.query.get(product_id)
        
        # Check if we have enough stock
        if product.stock_quantity < quantity:
            flash(f'Not enough stock! Available: {product.stock_quantity}', 'error')
            products = Product.query.filter(Product.stock_quantity > 0).all()
            return render_template('add_sale.html', products=products)
        
        total_price = quantity * unit_price
        
        sale = Sale(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            customer_name=customer_name,
            notes=notes
        )
        
        # Update product stock
        product.stock_quantity -= quantity
        product.updated_at = datetime.utcnow()
        
        db.session.add(sale)
        db.session.commit()
        flash('Sale recorded successfully!', 'success')
        return redirect(url_for('sales'))
    
    products = Product.query.filter(Product.stock_quantity > 0).all()
    return render_template('add_sale.html', products=products)

@app.route('/reports')
def reports():
    # Daily sales
    today = datetime.utcnow().date()
    daily_sales = db.session.query(
        func.sum(Sale.total_price),
        func.count(Sale.id)
    ).filter(func.date(Sale.created_at) == today).first()
    
    # Monthly sales
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    monthly_sales = db.session.query(
        func.sum(Sale.total_price),
        func.count(Sale.id)
    ).filter(
        func.extract('month', Sale.created_at) == current_month,
        func.extract('year', Sale.created_at) == current_year
    ).first()
    
    # Top selling products this month
    top_products = db.session.query(
        Product.name,
        func.sum(Sale.quantity).label('total_sold'),
        func.sum(Sale.total_price).label('total_revenue')
    ).join(Sale).filter(
        func.extract('month', Sale.created_at) == current_month,
        func.extract('year', Sale.created_at) == current_year
    ).group_by(Product.id, Product.name).order_by(
        func.sum(Sale.quantity).desc()
    ).limit(10).all()
    
    # Recent transactions
    recent_purchases = Purchase.query.order_by(Purchase.created_at.desc()).limit(10).all()
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(10).all()
    
    return render_template('reports.html',
                         daily_sales=daily_sales,
                         monthly_sales=monthly_sales,
                         top_products=top_products,
                         recent_purchases=recent_purchases,
                         recent_sales=recent_sales)
