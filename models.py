from email.policy import default
from peewee import *
from peewee_migrate import Router
import datetime
import orm_sqlite 


db = SqliteDatabase('database.db')

class Tasks(Model):
    task_id = AutoField()
    title = CharField()
    start_date = DateTimeField(default=None,null=True)
    due_date = DateTimeField(default=None,null=True)
    status = CharField()
    priority = CharField()
    description = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database=db
        db_table='Tasks'


models = [Tasks]
# db.drop_tables(models)
db.create_tables(models,safe=True)