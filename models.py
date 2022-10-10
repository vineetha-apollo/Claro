from email.policy import default
from peewee import *
from peewee_migrate import Router
import datetime
import orm_sqlite 
# from playhouse.migrate import *


db = SqliteDatabase('database.db')
# migrator = SqliteMigrator(db)
# router = Router(db)

# # Create migration
# router.create('migration_name')

# # Run migration/migrations
# router.run('migration_name')

# # Run all unapplied migrations
# router.run()

# Run all unapplied migrations
# router.run()

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

class Group(Model):
    group_id = AutoField()
    title = CharField()
    start_date = DateField(default=None,null=True)
    end_date = DateField(default=None,null=True)
    status = CharField()
    priority = CharField()
    description = CharField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    user_ids = CharField(null=True)
    # start_at = DateTimeField(default=datetime.datetime.now)
    # end_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database=db
        db_table='Group'

class Users(Model):
    user_id = AutoField()
    username = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    status = CharField()
    class Meta:
        database=db
        db_table='Users'


models = [Tasks,Group,Users]
# db.drop_tables(models)
db.create_tables(models,safe=True)


