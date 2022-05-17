# sqlalchemy-starrocks
Starrocks (formerly known as DorisDB) SQLAlchemy Dialect



## Installation

Option A: clone or download this project, and run following cli commands:

```shell
cd sqlalchemy-starrocks && python setup.py install
```



Option B: download the latest release from github and install:

```python
python -m pip install git+https://github.com/ooobug/sqlalchemy-starrocks.git
```



## Usage

To connect to `Starrocks`, use the following format:
```html
starrocks://<username>:<password>@<host>:<port>/<dbname>[?<options>]
```



- Python

```python
import sqlalchemy as sa
engine = sa.create_engine('starrocks://test:1234@localhost:9030/test?charset=utf8')
conn = engine.connect()
```



- Superset

  <div align="left"><img src="superset.png"></image></div>
  
  
  



## Testing

Test cases are under directory named `tests` . 

Unit testing is straightforward, just hit

```shell
python tests/test_starrocks.py
```



Furthermore, you can run overall compatibility tests as follows

- DDL
```shell
python tests/test_ddl.py
```



- DML
```shell
python tests/test_dml.py
```



- Query
```shell
python tests/test_simple_query.py
```