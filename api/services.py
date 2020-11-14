from repos import Repository
from repos.mongo import MongoRepository
from api.schemas import TaskSchema,UserSchema
from bson.objectid import ObjectId
from api.errors.api_errors import InvalidId

class Service:
  def __init__(self, repo_client=Repository(adapter=MongoRepository)):
    self.repo_client = repo_client

  def find_user(self,username = None, _id = None):
    if username is not None:
      user = self.repo_client.find_one({"username": username},'users')
      if user is not None:
          user = UserSchema().load(user)
    else:
          user = db.users.find_one({"_id": ObjectId(_id)},'users')
          if user is not None:
              user = UserSchema().load(user)
    return user

  def find_task(self,_id=None):
    if _id is not None:
        try:
          tasks_mongo = self.repo_client.find_one({"_id": ObjectId(_id)},'tasks_bucket')       
        except:
            raise InvalidId("Not supported Id type")

        if tasks_mongo is not None:
            tasks = [TaskSchema().dump(tasks_mongo)]
        else:
            tasks = []

    else:

      tasks_mongo = self.repo_client.find_all({},'tasks_bucket')
      tasks = TaskSchema(many=True).dump(tasks_mongo)

    return tasks

  def create_task(self, title, description, done):
    
      new_task = {
          "title": title,
          "description": description,
          "done": done,
      }
      new_task['_id'] = self.repo_client.create(new_task,'tasks_bucket').inserted_id
      return TaskSchema().dump(new_task)

  def update_task(self, task,task_to_update):
      _id = str(task['_id'])
      records_affected = self.repo_client.update_one({"_id": ObjectId(_id)},{"$set": task_to_update},'tasks_bucket')
      task.update(task_to_update)
      return task

  def delete_task(self, _id):
      records_affected = self.repo_client.delete({"_id": ObjectId(_id)},'tasks_bucket')
      return records_affected > 0
