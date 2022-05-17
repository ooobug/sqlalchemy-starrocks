"""
:dialect:: starrocks
:name: starrocks
:dbapi: 
:connectstring: starrocks://<username>:<password>@<host>/<dbname>[?<options>]

from sqlalchemy.dialects import registry
registry.register("starrocks", "starrocks_dialect", "StarrocksDialect")
"""


from sqlalchemy import types as sqlalchemy_types
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql


starrocks_type_mappings = {
    'boolean': sqlalchemy_types.Boolean,
    'tinyint': sqlalchemy_types.SmallInteger,
    'smallint': sqlalchemy_types.SmallInteger,
    'int': sqlalchemy_types.Integer,
    'largeint': sqlalchemy_types.BigInteger,
    'bigint': sqlalchemy_types.BigInteger,
    'float': sqlalchemy_types.Float,
    'double': sqlalchemy_types.Float,
    'decimal': sqlalchemy_types.DECIMAL,
    'char': sqlalchemy_types.CHAR,
    'varchar': sqlalchemy_types.VARCHAR,
    'string': sqlalchemy_types.String,
    'date': sqlalchemy_types.Date,
    'datetime': sqlalchemy_types.DateTime
}


def infer_data_type(spec):
    dtype = None
    if isinstance(spec, str):
        spec = spec.split('(')[0].lower()
        dtype = starrocks_type_mappings.get(spec)
    return dtype


class StarrocksDialect(MySQLDialect_pymysql):

    name = "starrocks"
    

    def query(self, connection, query_str, **kwargs):
        return connection.execute(query_str).fetchall()


    def get_schema_names(self, connection, **kwargs):
        # Equivalent to "SHOW DATABASES"
        rows = self.query(connection, 'SHOW DATABASES')
        return list(map(lambda x: x[0], rows))


    def get_table_names(self, connection, schema=None, **kwargs):
        query_str = "SHOW TABLES"
        if schema:
            query_str += " IN `%s`" % schema
        rows = self.query(connection, query_str)
        return list(map(lambda x: x[0], rows))


    def _get_table_columns(self, connection, table_name, schema):
        if schema:
            full_table = '`%s`.`%s`' % (schema, table_name)
        else:
            full_table = '`%s`' % table_name
        query_str = "DESCRIBE %s" % full_table
        return self.query(connection, query_str)


    def has_schema(self, connection, schema_name):
        try:
            return schema_name in self.get_schema_names(connection)
        except:
            pass
        return False


    def has_table(self, connection, table_name, schema=None):
        try:
            if self._get_table_columns(connection, table_name, schema):
                return True
        except:
            pass
        return False


    def get_columns(self, connection, table_name, schema=None, **kwargs):
        columns = []
        rows = self._get_table_columns(connection, table_name, schema)
        for row in rows:
            labels = ('name', 'type', 'nullable', 'default', 'extra')
            curr_col = dict(zip(labels, map(lambda x: x or '', row)))
            curr_col['type'] = infer_data_type(curr_col['type'])
            columns.append(curr_col)
        return columns