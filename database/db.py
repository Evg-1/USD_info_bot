import os

import peewee

db_abs_path = os.path.abspath(os.path.join(__file__, os.pardir, 'db.sqlite'))

database = peewee.SqliteDatabase(db_abs_path)


class BaseTable(peewee.Model):
    class Meta:
        database = database


class User(BaseTable):
    telegram_id = peewee.IntegerField(primary_key=True)
    first_name = peewee.CharField(null=True)
    last_name = peewee.CharField(null=True)
    last_activity = peewee.DateTimeField(null=True)


database.create_tables([User])
