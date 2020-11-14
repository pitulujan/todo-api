class Repository:
  def __init__(self, adapter=None):
    self.client = adapter()

  def find_all(self, selector,collection_name):
    return self.client.find_all(selector,collection_name)
 
  def find_one(self, selector,collection_name):
    return self.client.find_one(selector,collection_name)
 
  def create(self, task,collection_name):
    return self.client.create(task,collection_name)
  
  def update_one(self, selector, task,collection_name):
    return self.client.update_one(selector, task,collection_name)
  
  def delete(self, selector,collection_name):
    return self.client.delete(selector,collection_name)