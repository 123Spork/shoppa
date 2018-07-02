import logging
import pymysql


from sqlalchemy import create_engine, exc
from pymysql import err
from sqlalchemy.orm import sessionmaker
from shoppa.core.exceptions import SQLIntegrityError, SQLInvalidRequestError, SQLInternalError, SQLOperationalError
from shoppa.settings import settings

pymysql.install_as_MySQLdb()
log = logging.getLogger(__name__)


class SQLDBManager(object):
    def __init__(self):
        self._connection_engine = None
        self.connection_uri = self.get_connection_uri()

    @property
    def connection_engine(self):
        if not self._connection_engine:
            self._connection_engine = create_engine(self.connection_uri)
        return self._connection_engine

    def get_connection_uri(self):
        return ""

    def _start_session(self):
        Session = sessionmaker(bind=self.connection_engine, expire_on_commit=False)
        session = Session()
        session._model_changes = {}
        from shoppa.core.models import BaseSQLModel
        BaseSQLModel.metadata.create_all(bind=self.connection_engine)
        return session

    def _end_session(self, session):
        session.close()

    def add(self, table_rows):
        session = self._start_session()
        if not isinstance(table_rows, list):
            table_rows = [table_rows]
        session.add_all(table_rows)
        try:
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            self._end_session(session)
            raise SQLIntegrityError

        self._end_session(session)

    def delete(self, table_rows):
        session = self._start_session()
        if not isinstance(table_rows, list):
            table_rows = [table_rows]
        for row in table_rows:
            try:
                session.delete(row)
            except exc.InvalidRequestError as e:
                session.rollback()
                self._end_session(session)
                raise SQLInvalidRequestError(e)
        try:
            session.commit()
        except exc.InvalidRequestError as e:
            session.rollback()
            self._end_session(session)
            raise SQLInvalidRequestError(e)

    def find(self, row_model, **kwargs):
        session = self._start_session()
        results = session.query(row_model).filter_by(**kwargs).all()
        self._end_session(session)
        return results

    def query_db(self, query, in_session=None):
        if not in_session:
            session = self._start_session()
        else:
            session = in_session
        try:
            results = session.execute(query)
        except err.InternalError as g:
            self._end_session(session)
            raise SQLInternalError(g)
        except exc.StatementError as e:
            self._end_session(session)
            raise SQLInvalidRequestError(e)

        self._end_session(session)
        return results

    def drop_table(self, row_model):
        self.drop_tables(row_model.__tablename__)

    def drop_views(self, view_names):
        session = self._start_session()
        if not isinstance(view_names, list):
            view_names = [view_names]

        for view in view_names:
            self.query_db("DROP VIEW IF EXISTS {0};".format(view), in_session=session)
        self._end_session(session)

    def drop_tables(self, table_names):
        if not isinstance(table_names, list):
            table_names = [table_names]

        for table in table_names:
            self.query_db("DROP TABLE IF EXISTS {0};".format(table))

    def get_view(self, view_name):
        return self.query_db("SELECT * FROM {0};".format(view_name))


class MariaDBManager(SQLDBManager):

    def get_connection_uri(self):
        return "mysql://{0}:{1}@{2}/{3}".format(
            settings.SQL_DB_AUTH_SETTINGS['user'],
            settings.SQL_DB_AUTH_SETTINGS['password'],
            settings.SQL_DB_HOST,
            settings.SQL_DB_DATABASE
        )

    def drop_all_tables_views(self):
        session = self._start_session()

        try:
            tables = self.query_db('SHOW TABLES;')
        except exc.OperationalError as e:
            raise SQLOperationalError(e)

        #maria db returns view results with SHOW TABLES request
        for table in tables:
            try:
                self.query_db("DROP TABLE IF EXISTS {0};".format(table[0]))
            except err.InternalError as e:
                self._end_session(session)
                raise SQLInternalError(e)
            except exc.InternalError as f:
                self._end_session(session)
                raise SQLInternalError(f)
            try:
                self.query_db("DROP VIEW IF EXISTS {0};".format(table[0]))
            except err.InternalError as e:
                self._end_session(session)
                raise SQLInternalError(e)
            except exc.InternalError as f:
                self._end_session(session)
                raise SQLInternalError(f)

        self._end_session(session)

    def drop_views(self, view_names):
        session = self._start_session()
        if not isinstance(view_names, list):
            view_names = [view_names]

        try:
            sql = "DROP VIEW IF EXISTS "
            for view in view_names:
                sql += "{0},".format(view)
            self.query_db(sql[:-1], in_session=session)
        except err.InternalError as e:
            self._end_session(session)
            raise SQLInternalError(e)
        except exc.InternalError as f:
            self._end_session(session)
            raise SQLInternalError(f)

        self._end_session(session)


class SQLiteDBManager(SQLDBManager):

    def get_connection_uri(self):
        return "sqlite://"

    def drop_all_tables_views(self):
        session = self._start_session()

        try:
            views = self.query_db('SELECT * FROM sqlite_master WHERE type="view";')
        except exc.OperationalError as e:
            self._end_session(session)
            raise SQLOperationalError(e)

        for view in views:
            try:
                self.query_db("DROP VIEW IF EXISTS {0};".format(view[1]))
            except err.InternalError as e:
                self._end_session(session)
                raise SQLInternalError(e)

        try:
            tables = self.query_db('SELECT * FROM sqlite_master WHERE type="table";')
        except exc.OperationalError as e:
            self._end_session(session)
            raise SQLOperationalError(e)

        for table in tables:
            try:
                self.query_db("DROP TABLE IF EXISTS {0};".format(table[1]))
            except err.InternalError as e:
                self._end_session(session)
                raise SQLInternalError(e)
            except exc.InternalError as f:
                self._end_session(session)
                raise SQLInternalError(f)

        self._end_session(session)

sql_db = None
if settings.SQL_DB_MODE == "test":
    sql_db = SQLiteDBManager()
else:
    sql_db = MariaDBManager()