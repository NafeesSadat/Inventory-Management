# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from app.models import Inventory, Inbound, Outbound, User, Role
# from app.utils import role_required
# from app import db
# from sqlalchemy import func
# from sqlalchemy.orm.session import object_session

# routes = Blueprint('routes', __name__)

# @routes.route('/')
# @login_required
# def index():
#     return render_template('index.html')

# @routes.route('/inventory', methods=['GET', 'POST'])
# @login_required
# @role_required('manager')
# def inventory():
#     if request.method == 'POST':
#         search_term = request.form['search']
#         items = Inventory.query.filter(Inventory.name.contains(search_term) | Inventory.sku.contains(search_term)).all()
#     else:
#         items = Inventory.query.all()
#     return render_template('inventory.html', items=items)

# @routes.route('/inventory/add', methods=['GET', 'POST'])
# @login_required
# @role_required('manager')
# def add_inventory():
#     if request.method == 'POST':
#         category = request.form['category']
#         sku = request.form['sku']
#         name = request.form['name']
#         location = request.form['location']
#         quantity = request.form['quantity']
#         supplier = request.form['supplier']
#         new_item = Inventory(category=category, sku=sku, name=name, location=location, quantity=quantity, supplier=supplier)
#         db.session.add(new_item)
#         db.session.commit()
#         flash('Inventory item added successfully!', 'success')
#         return redirect(url_for('routes.inventory'))
#     return render_template('add_inventory.html')

# @routes.route('/inventory/update/<int:id>', methods=['GET', 'POST'])
# @login_required
# @role_required('manager')
# def update_inventory(id):
#     item = Inventory.query.get_or_404(id)  # Fetch the item from the current session
#     if request.method == 'POST':
#         try:
#             # Debugging: Log the session state before updating
#             print("Session State Before Update:")
#             print("Session is dirty:", db.session.dirty)
#             print("Session is new:", db.session.new)
#             print("Session is in a failed state:", not db.session.is_active)

#             # Update attributes
#             item.category = request.form['category']
#             item.sku = request.form['sku']
#             item.name = request.form['name']
#             item.location = request.form['location']
#             item.quantity = int(request.form['quantity'])  # Ensure correct type
#             item.supplier = request.form['supplier']

#             # Debugging: Check the item attributes before committing
#             print("Updated Item Before Merge:", item.__dict__)

#             # Merge the object into the current session to avoid conflicts
#             item = db.session.merge(item)  # Ensure the object is in the current session

#             # Debugging: Log the session state after merge
#             print("Session State After Merge:")
#             print("Session is dirty:", db.session.dirty)
#             print("Session is new:", db.session.new)

#             db.session.commit()  # Persist changes

#             # Debugging: Verify the update in the database
#             updated_item = Inventory.query.get(id)
#             print("Verified Updated Item After Commit:", updated_item.__dict__)

#             flash('Inventory item updated successfully!', 'success')
#         except Exception as e:
#             db.session.rollback()  # Reset session on error
#             flash(f'Error updating inventory item: {str(e)}', 'danger')
#             print(f'Error: {str(e)}')  # Log error for debugging
#         return redirect(url_for('routes.inventory'))
#     return render_template('update_inventory.html', item=item)



# @routes.route('/inbound')
# @login_required
# def inbound():
#     items = Inbound.query.all()
#     return render_template('inbound.html', items=items)

# @routes.route('/inbound/add', methods=['GET', 'POST'])
# @login_required
# @role_required('operator')
# def add_inbound():
#     if request.method == 'POST':
#         reference = request.form['reference']
#         date_received = request.form['date_received']
#         product_sku = request.form['product_sku']
#         quantity = request.form['quantity']
#         location = request.form['location']
#         remarks = request.form['remarks']
        
#         try:
#             quantity = int(quantity)  # Ensure quantity is an integer
#         except ValueError:
#             flash("Quantity must be a valid number.", "danger")
#             return redirect(url_for("routes.add_inbound"))

#         new_inbound = Inbound(reference=reference, date_received=date_received, product_sku=product_sku, quantity=quantity, location=location, remarks=remarks)
#         db.session.add(new_inbound)
#         db.session.commit()

#         # Update inventory
#         inventory_item = Inventory.query.filter_by(sku=product_sku).first()
#         if inventory_item:
#             try:
#                 print("Before Inventory Update:", inventory_item.__dict__)

#                 # Merge to ensure session consistency
#                 inventory_item.quantity += quantity
#                 inventory_item = db.session.merge(inventory_item)

#                 print("After Inventory Update:", inventory_item.__dict__)
#                 db.session.commit()
#                 print("Inventory updated successfully.")
#                 flash('Inbound record added and inventory updated!', 'success')
#             except Exception as e:
#                 db.session.rollback()
#                 print(f"Error during inventory update: {e}")
#                 flash("Failed to update inventory.", "danger")
#         else:
#             print("Inventory item not found for SKU:", product_sku)
#             flash("Inventory item not found. Please check the SKU.", "danger")

#         return redirect(url_for('routes.inbound'))
#     return render_template('add_inbound.html')



# @routes.route('/outbound')
# @login_required
# def outbound():
#     items = Outbound.query.all()
#     return render_template('outbound.html', items=items)

# @routes.route('/outbound/add', methods=['GET', 'POST'])
# @login_required
# @role_required('operator')
# def add_outbound():
#     if request.method == 'POST':
#         reference = request.form['reference']
#         date_shipped = request.form['date_shipped']
#         product_sku = request.form['product_sku']
#         quantity = request.form['quantity']
#         destination = request.form['destination']
#         remarks = request.form['remarks']
        
#         try:
#             quantity = int(quantity)  # Ensure the quantity is an integer
#             if quantity <= 0:
#                 flash('Quantity must be a positive number.', 'danger')
#                 return redirect(url_for('routes.add_outbound'))
#         except ValueError:
#             flash('Invalid quantity. Please enter a valid number.', 'danger')
#             return redirect(url_for('routes.add_outbound'))
        
#         new_outbound = Outbound(reference=reference, date_shipped=date_shipped, product_sku=product_sku, quantity=quantity, destination=destination, remarks=remarks)
#         db.session.add(new_outbound)
#         db.session.commit()
        
#         # Update inventory
#         inventory_item = Inventory.query.filter_by(sku=product_sku).first()
#         if inventory_item:
#             if inventory_item.quantity >= quantity:
#                 try:
#                     print("Before Inventory Update:", inventory_item.__dict__)

#                     # Merge to ensure session consistency
#                     inventory_item.quantity -= quantity
#                     inventory_item = db.session.merge(inventory_item)

#                     print("After Inventory Update:", inventory_item.__dict__)
#                     db.session.commit()
#                     flash('Outbound record added and inventory updated successfully!', 'success')
#                 except Exception as e:
#                     db.session.rollback()
#                     print(f"Error during inventory update: {e}")
#                     flash("Failed to update inventory.", "danger")
#             else:
#                 flash('Not enough inventory to fulfill the outbound request.', 'danger')
#         else:
#             flash('Inventory item not found for the given SKU.', 'danger')
        
#         return redirect(url_for('routes.outbound'))
    
#     return render_template('add_outbound.html')



# @routes.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username'].strip().lower()  # Normalize the username
#         password = request.form['password']
#         user = User.query.filter(func.lower(User.username) == username).first()

#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect(url_for('routes.index'))
#         else:
#             flash('Login failed. Check your username and/or password', 'danger')
#     return render_template('login.html')

# @routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username'].strip().lower()  # Normalize the username
#         password = request.form['password']
#         role_name = request.form['role']
        
#         # Fetch role and hash password
#         role = Role.query.filter_by(name=role_name).first()
#         hashed_password = generate_password_hash(password, method='sha256')

#         # Check if the user already exists in the database (case insensitive)
#         existing_user = User.query.filter(func.lower(User.username) == username).first()

#         if existing_user is None:
#             new_user = User(username=username, password=hashed_password, role=role)
#             try:
#                 # If the user or role is already attached to a session, remove it before adding
#                 user_session = object_session(new_user)
#                 role_session = object_session(role)

#                 if user_session:
#                     user_session.expunge(new_user)  # Detach the user object from the current session

#                 if role_session:
#                     role_session.expunge(role)  # Detach the role object from the current session

#                 db.session.add(new_user)
#                 db.session.commit()
#                 flash('User registered successfully!', 'success')
#                 return redirect(url_for('routes.login')) # Redirect to the login page
#             except Exception as e:
#                 db.session.rollback()
#                 flash(f'An error occurred while registering the user: {str(e)}', 'danger')
#         else:
#             flash('User is already registered.', 'danger')

#     roles = Role.query.all()
#     return render_template('register.html', roles=roles)


# @routes.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('routes.login'))


from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Inventory, Inbound, Outbound, User, Role
from app.utils import role_required
from app import db
from sqlalchemy import func
from sqlalchemy.orm.session import object_session

# Define the blueprint for routing
routes = Blueprint('routes', __name__)

# Route for the home page, requires the user to be logged in
@routes.route('/')
@login_required
def index():
    return render_template('index.html')

# Route to view inventory, only accessible by users with 'manager' role
@routes.route('/inventory', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def inventory():
    if request.method == 'POST':
        search_term = request.form['search']  # Get search term from form
        items = Inventory.query.filter(Inventory.name.contains(search_term) | Inventory.sku.contains(search_term)).all()  # Filter inventory by name or SKU
    else:
        items = Inventory.query.all()  # Fetch all inventory items if no search term
    return render_template('inventory.html', items=items)

# Route to add a new inventory item, accessible by 'manager' role
@routes.route('/inventory/add', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def add_inventory():
    if request.method == 'POST':
        # Get form data and create a new inventory item
        category = request.form['category']
        sku = request.form['sku']
        name = request.form['name']
        location = request.form['location']
        quantity = request.form['quantity']
        supplier = request.form['supplier']
        new_item = Inventory(category=category, sku=sku, name=name, location=location, quantity=quantity, supplier=supplier)
        db.session.add(new_item)  # Add new item to the session
        db.session.commit()  # Commit changes to the database
        flash('Inventory item added successfully!', 'success')  # Show success message
        return redirect(url_for('routes.inventory'))  # Redirect to inventory page
    return render_template('add_inventory.html')

# Route to update an existing inventory item, accessible by 'manager' role
@routes.route('/inventory/update/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def update_inventory(id):
    item = Inventory.query.get_or_404(id)  # Fetch the inventory item or show a 404 if not found
    if request.method == 'POST':
        try:
            # Update inventory item fields based on the form input
            item.category = request.form['category']
            item.sku = request.form['sku']
            item.name = request.form['name']
            item.location = request.form['location']
            item.quantity = int(request.form['quantity'])  # Ensure quantity is an integer
            item.supplier = request.form['supplier']
            
            # Merge item to ensure it's updated correctly in the session
            item = db.session.merge(item)
            db.session.commit()  # Save changes to the database
            flash('Inventory item updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback session if error occurs
            flash(f'Error updating inventory item: {str(e)}', 'danger')
        return redirect(url_for('routes.inventory'))
    return render_template('update_inventory.html', item=item)

# Route to view inbound records, accessible by logged-in users
@routes.route('/inbound')
@login_required
def inbound():
    items = Inbound.query.all()  # Fetch all inbound records
    return render_template('inbound.html', items=items)

# Route to add a new inbound record, accessible by 'operator' role
@routes.route('/inbound/add', methods=['GET', 'POST'])
@login_required
@role_required('operator')
def add_inbound():
    if request.method == 'POST':
        reference = request.form['reference']
        date_received = request.form['date_received']
        product_sku = request.form['product_sku']
        quantity = request.form['quantity']
        location = request.form['location']
        remarks = request.form['remarks']

        # Ensure quantity is a valid integer
        try:
            quantity = int(quantity)
        except ValueError:
            flash("Quantity must be a valid number.", "danger")
            return redirect(url_for("routes.add_inbound"))

        # Create new inbound record
        new_inbound = Inbound(reference=reference, date_received=date_received, product_sku=product_sku, quantity=quantity, location=location, remarks=remarks)
        db.session.add(new_inbound)
        db.session.commit()

        # Update inventory quantity after inbound entry
        inventory_item = Inventory.query.filter_by(sku=product_sku).first()
        if inventory_item:
            inventory_item.quantity += quantity  # Add quantity to existing inventory
            inventory_item = db.session.merge(inventory_item)  # Ensure session consistency
            db.session.commit()
            flash('Inbound record added and inventory updated!', 'success')
        else:
            flash("Inventory item not found. Please check the SKU.", "danger")

        return redirect(url_for('routes.inbound'))
    return render_template('add_inbound.html')

# Route to view outbound records, accessible by logged-in users
@routes.route('/outbound')
@login_required
def outbound():
    items = Outbound.query.all()  # Fetch all outbound records
    return render_template('outbound.html', items=items)

# Route to add a new outbound record, accessible by 'operator' role
@routes.route('/outbound/add', methods=['GET', 'POST'])
@login_required
@role_required('operator')
def add_outbound():
    if request.method == 'POST':
        reference = request.form['reference']
        date_shipped = request.form['date_shipped']
        product_sku = request.form['product_sku']
        quantity = request.form['quantity']
        destination = request.form['destination']
        remarks = request.form['remarks']

        # Ensure quantity is a valid positive integer
        try:
            quantity = int(quantity)
            if quantity <= 0:
                flash('Quantity must be a positive number.', 'danger')
                return redirect(url_for('routes.add_outbound'))
        except ValueError:
            flash('Invalid quantity. Please enter a valid number.', 'danger')
            return redirect(url_for('routes.add_outbound'))

        # Create new outbound record
        new_outbound = Outbound(reference=reference, date_shipped=date_shipped, product_sku=product_sku, quantity=quantity, destination=destination, remarks=remarks)
        db.session.add(new_outbound)
        db.session.commit()

        # Update inventory quantity after outbound entry
        inventory_item = Inventory.query.filter_by(sku=product_sku).first()
        if inventory_item:
            if inventory_item.quantity >= quantity:
                inventory_item.quantity -= quantity  # Subtract quantity from inventory
                inventory_item = db.session.merge(inventory_item)  # Ensure session consistency
                db.session.commit()
                flash('Outbound record added and inventory updated successfully!', 'success')
            else:
                flash('Not enough inventory to fulfill the outbound request.', 'danger')
        else:
            flash('Inventory item not found for the given SKU.', 'danger')

        return redirect(url_for('routes.outbound'))
    return render_template('add_outbound.html')

# Route for user login
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()  # Normalize username to lowercase
        password = request.form['password']
        user = User.query.filter(func.lower(User.username) == username).first()  # Case insensitive search for username

        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            return redirect(url_for('routes.index'))  # Redirect to the index page
        else:
            flash('Login failed. Check your username and/or password', 'danger')
    return render_template('login.html')

# Route for user registration
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()  # Normalize username
        password = request.form['password']
        role_name = request.form['role']
        
        # Fetch selected role and hash password
        role = Role.query.filter_by(name=role_name).first()
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if user already exists in the database
        existing_user = User.query.filter(func.lower(User.username) == username).first()

        if existing_user is None:
            new_user = User(username=username, password=hashed_password, role=role)
            try:
                # Remove any existing session references to avoid conflicts
                user_session = object_session(new_user)
                role_session = object_session(role)

                if user_session:
                    user_session.expunge(new_user)

                if role_session:
                    role_session.expunge(role)

                db.session.add(new_user)
                db.session.commit()
                flash('User registered successfully!', 'success')
                return redirect(url_for('routes.login'))  # Redirect to login page
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred while registering the user: {str(e)}', 'danger')
        else:
            flash('User is already registered.', 'danger')

    roles = Role.query.all()  # Fetch all available roles for registration
    return render_template('register.html', roles=roles)

# Route for logging out a user
@routes.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('routes.login'))  # Redirect to login page
