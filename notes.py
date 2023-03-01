# Use this file for notes and running examples...
# As expected, run it with `python3 -m notes`

# "Establishing Connectivity - the Engine"
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
print(engine)

# "Working with Transactions and the DBAPI"
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

# "Committing Changes"

# "commit as you go"
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    # raise RuntimeError("oh no!")
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# "begin once"
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

# fetching rows
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    #tuple assignment -- > assign variables to each row positionally as they are received
    # for x,y in result:
    #     print(f"x: {x}  y: {y}")

    # integer index -- > regular integer access
    # for row in result:
    #     x = row[0]
    #      ...

    # Attribute Name -->  tuples have dynamic attribute names matching the names of each column
    # for row in result:
    #     y = row.y

    #     # illustrate use with Python f-strings
    #     print(f"Row: {row.x} {y}")

    # mapping access --> receive rows as Python mapping objects, which is essentially a read-only version of Python’s interface to the common dict object, the Result may be transformed into a MappingResult object using the Result.mappings() modifier; this is a result object that yields dictionary-like RowMapping objects rather than Row objects:
    # for dict_row in result.mappings():
    #     x = dict_row["x"]
    #     y = dict_row["y"]

    # original ex
    for row in result:
         print(f"x: {row.x}  y: {row.y}")

# Sending Parameters
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 4})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

# Sending Multiple Parameters
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()

# Executing with an ORM Session¶
from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}]
    )
    session.commit()

# copied code too see print of new table
stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

# Working with Database Metadata
