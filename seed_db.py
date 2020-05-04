from api import db
from api.models import User, Tasks

# Simple test user for testing purposes
test_user = User(username="pitu")
test_user.set_password("pitu")


# Simple tasks for testing purposes
task_1 = Tasks(description="Test description 1", done=False, title="Got Milk?")
task_2 = Tasks(description="Test description 2", done=False, title="Got Rice?")

db.session.add(test_user)
db.session.add(task_1)
db.session.add(task_2)
db.session.commit()
