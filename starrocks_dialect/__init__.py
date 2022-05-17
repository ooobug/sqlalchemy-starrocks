from sqlalchemy.dialects import registry

__version__ = '0.1.0'
registry.register('starrocks', 'starrocks_dialect.starrocks', 'StarrocksDialect')