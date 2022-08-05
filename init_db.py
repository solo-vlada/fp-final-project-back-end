from server_app   import db
from server_app.models import tables

# Clear it all out

db.drop_all()

# Set it back up

db.create_all()
