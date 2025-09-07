from app import app, db
from models import User, Product
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', is_admin=True)
            admin_user.set_password('admin123')
            db.session.add(admin_user)
        
        # Import functions from routes
        from routes import generate_sku, generate_qr_code
        
        # Create sample products if none exist
        try:
            product_count = Product.query.count()
        except:
            # Table might not exist yet, so create it first
            db.create_all()
            product_count = 0
            
        if product_count == 0:
            sample_products_data = [
                {'name': 'Arroz 5kg', 'category': 'Grãos', 'price': 25.90, 'stock_quantity': 50, 'min_stock': 10},
                {'name': 'Feijão Preto 1kg', 'category': 'Grãos', 'price': 8.50, 'stock_quantity': 30, 'min_stock': 5},
                {'name': 'Açúcar Cristal 1kg', 'category': 'Açúcar', 'price': 4.20, 'stock_quantity': 40, 'min_stock': 8},
                {'name': 'Óleo de Soja 900ml', 'category': 'Óleos', 'price': 5.80, 'stock_quantity': 25, 'min_stock': 5},
                {'name': 'Macarrão Espaguete 500g', 'category': 'Massas', 'price': 3.90, 'stock_quantity': 60, 'min_stock': 15},
                {'name': 'Leite Integral 1L', 'category': 'Laticínios', 'price': 4.50, 'stock_quantity': 35, 'min_stock': 10},
                {'name': 'Pão Francês kg', 'category': 'Padaria', 'price': 8.90, 'stock_quantity': 20, 'min_stock': 5},
                {'name': 'Detergente 500ml', 'category': 'Limpeza', 'price': 2.30, 'stock_quantity': 45, 'min_stock': 10},
                {'name': 'Sabão em Pó 1kg', 'category': 'Limpeza', 'price': 12.90, 'stock_quantity': 15, 'min_stock': 3},
                {'name': 'Refrigerante Cola 2L', 'category': 'Bebidas', 'price': 7.50, 'stock_quantity': 28, 'min_stock': 6},
            ]
            
            for product_data in sample_products_data:
                sku = generate_sku()
                qr_code_path = generate_qr_code(sku, product_data['name'])
                
                product = Product(
                    name=product_data['name'],
                    sku=sku,
                    category=product_data['category'],
                    price=product_data['price'],
                    stock_quantity=product_data['stock_quantity'],
                    min_stock=product_data['min_stock'],
                    qr_code_path=qr_code_path
                )
                db.session.add(product)
        
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_database()
