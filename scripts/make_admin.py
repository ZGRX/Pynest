from app.db.database import SessionLocal
from app.db.models import User

db  = SessionLocal()
user = db.query(User).filter(User.email == "pg_test_20261021@example.com").first()
if user is None:
    print("Not found user")
else:     
    user.is_admin = True
    db.commit()
    print(user.is_admin)
db.close()
# {
#   "username": "pg_test",
#   "email": "pg_test_20261021@example.com",
#   "password": "test123456"
# }