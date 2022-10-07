from email.policy import default
from peewee import *
from peewee_migrate import Router
import datetime
import orm_sqlite 


db = SqliteDatabase('database.db')

class Tasks(Model):
    task_id = AutoField()
    title = CharField()
    start_date = DateField(default=None,null=True)
    due_date = DateField(default=None,null=True)
    status = CharField()
    priority = CharField()
    description = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    # end_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database=db
        db_table='Tasks'
class Groups(Model):
    group_id = AutoField()
    title = CharField()
    start_date = DateField(default=None,null=True)
    end_date = DateField(default=None,null=True)
    status = CharField()
    priority = CharField()
    description = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    # start_at = DateTimeField(default=datetime.datetime.now)
    # end_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database=db
        db_table='Groups'


models = [Tasks,Groups]
# db.drop_tables(models)
db.create_tables(models,safe=True)


# def initialize():
#     db.connect()
#     db.create_tables(modelss, safe=True)
#     db.close()

# import models

# if __name__ == '__main__':
#     models.initialize()