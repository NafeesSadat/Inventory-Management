# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

# db = SQLAlchemy()

# class Role(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     description = db.Column(db.String(200), nullable=True)

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
#     role = db.relationship('Role', backref=db.backref('users', lazy=True))

# class Inventory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(50), nullable=False)
#     sku = db.Column(db.String(50), unique=True, nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     supplier = db.Column(db.String(100), nullable=False)

# class Inbound(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     reference = db.Column(db.String(50), nullable=False)
#     date_received = db.Column(db.Date, nullable=False)
#     product_sku = db.Column(db.String(50), db.ForeignKey('inventory.sku'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     remarks = db.Column(db.String(200), nullable=True)

# class Outbound(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     reference = db.Column(db.String(50), nullable=False)
#     date_shipped = db.Column(db.Date, nullable=False)
#     product_sku = db.Column(db.String(50), db.ForeignKey('inventory.sku'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     destination = db.Column(db.String(100), nullable=False)
#     remarks = db.Column(db.String(200), nullable=True)
    

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize SQLAlchemy for ORM support
db = SQLAlchemy()

# Model to represent user roles in the system
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the role
    name = db.Column(db.String(50), unique=True, nullable=False)  # Role name, must be unique
    description = db.Column(db.String(200), nullable=True)  # Optional description of the role

# Model to represent users, including their roles
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(150), unique=True, nullable=False)  # Username, must be unique
    password = db.Column(db.String(150), nullable=False)  # Password, stored securely (hashed in production)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)  # Foreign key to Role
    role = db.relationship('Role', backref=db.backref('users', lazy=True))  # Establish a relationship with Role

# Model to represent inventory items in the warehouse
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the inventory item
    category = db.Column(db.String(50), nullable=False)  # Category of the inventory item
    sku = db.Column(db.String(50), unique=True, nullable=False)  # Stock keeping unit, must be unique
    name = db.Column(db.String(100), nullable=False)  # Name or description of the item
    location = db.Column(db.String(100), nullable=False)  # Storage location in the warehouse
    quantity = db.Column(db.Integer, nullable=False)  # Current quantity available
    supplier = db.Column(db.String(100), nullable=False)  # Supplier or vendor name

# Model to record inbound shipments to the warehouse
class Inbound(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the inbound record
    reference = db.Column(db.String(50), nullable=False)  # Reference identifier for the shipment
    date_received = db.Column(db.Date, nullable=False)  # Date when the shipment was received
    product_sku = db.Column(db.String(50), db.ForeignKey('inventory.sku'), nullable=False)  # SKU of the product
    quantity = db.Column(db.Integer, nullable=False)  # Quantity received
    location = db.Column(db.String(100), nullable=False)  # Location where the items were stored
    remarks = db.Column(db.String(200), nullable=True)  # Optional remarks or notes about the shipment

# Model to record outbound shipments from the warehouse
class Outbound(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the outbound record
    reference = db.Column(db.String(50), nullable=False)  # Reference identifier for the shipment
    date_shipped = db.Column(db.Date, nullable=False)  # Date when the shipment was sent out
    product_sku = db.Column(db.String(50), db.ForeignKey('inventory.sku'), nullable=False)  # SKU of the product
    quantity = db.Column(db.Integer, nullable=False)  # Quantity shipped
    destination = db.Column(db.String(100), nullable=False)  # Destination of the shipment
    remarks = db.Column(db.String(200), nullable=True)  # Optional remarks or notes about the shipment
