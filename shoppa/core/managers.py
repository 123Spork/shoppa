import logging
from shoppa.core.db import sql_db
from shoppa.core.exceptions import ObjectNotFound

log = logging.getLogger(__name__)

class CoreSQLDBModelManager(object):
    Model = object

    def get_multi(self, **kwargs):
        return sql_db.find(self.Model, **kwargs)

    def get(self, **kwargs):
        results = sql_db.find(self.Model, **kwargs)
        if len(results) > 0:
            return results[0]
        raise ObjectNotFound

    def save_multi(self, rows):
        sql_db.add(rows)

    def delete_multi(self, rows):
        sql_db.delete(rows)

    def drop_table(self):
        sql_db.drop_table(self.Model)

