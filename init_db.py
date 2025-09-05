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
        
        # Create sample products if none exist
        if Product.query.count() == 0:
            sample_products = [
                Product(name='Arroz 5kg', category='Grãos', price=25.90, stock_quantity=50, min_stock=10),
                Product(name='Feijão Preto 1kg', category='Grãos', price=8.50, stock_quantity=30, min_stock=5),
                Product(name='Açúcar Cristal 1kg', category='Açúcar', price=4.20, stock_quantity=40, min_stock=8),
                Product(name='Óleo de Soja 900ml', category='Óleos', price=5.80, stock_quantity=25, min_stock=5),
                Product(name='Macarrão Espaguete 500g', category='Massas', price=3.90, stock_quantity=60, min_stock=15),
                Product(name='Leite Integral 1L', category='Laticínios', price=4.50, stock_quantity=35, min_stock=10),
                Product(name='Pão Francês kg', category='Padaria', price=8.90, stock_quantity=20, min_stock=5),
                Product(name='Detergente 500ml', category='Limpeza', price=2.30, stock_quantity=45, min_stock=10),
                Product(name='Sabão em Pó 1kg', category='Limpeza', price=12.90, stock_quantity=15, min_stock=3),
                Product(name='Refrigerante Cola 2L', category='Bebidas', price=7.50, stock_quantity=28, min_stock=6),
            ]
            
            for product in sample_products:
                db.session.add(product)
        
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_database()
