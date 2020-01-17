# pandas strinio sqlite tempfile
# Use http://www.ch-werner.de/sqliteodbc/ both 32 and 64 standard installs and then define it as an 
# ODBC 32-bit connection in adminstrator tools for use in Excel (and other apps)
import sqlite3
import pandas as pd
import io

thing = "logistic-science-pack"
table_name = "Planning"

# https://kirkmcdonald.github.io/calc.html#items=lab:r:1 
scsv = """
item,item rate,factory,count,modules,beacon module,beacon count,power
logistic-science-pack,1,assembling-machine-1,0.2,,,,17000
inserter,1,assembling-machine-1,0.1,,,,3708.4
electronic-circuit,1,assembling-machine-1,0.1,,,,3708.4
copper-cable,3,assembling-machine-1,0.1,,,,4312.5
copper-plate,1.5,stone-furnace,0.1,,,,7200
copper-ore,1.5,electric-mining-drill,0.1,//,,,7350
transport-belt,1,assembling-machine-1,0.1,,,,3104.2
iron-gear-wheel,1.5,assembling-machine-1,0.1,,,,4312.5
iron-plate,5.5,stone-furnace,0.3,,,,26400
iron-ore,5.5,electric-mining-drill,0.2,//,,,18950
coal,0.504,electric-mining-drill,0.1,//,,,4461.6

"""

Previously_Using_TemporaryFile = """
import tempfile
fp = tempfile.TemporaryFile() 
b = bytes(scsv,'utf-8' )
fp.write(b)
fp.seek(0)
# ... stuff ...
fp.close()
"""

# https://docs.python.org/3/library/io.html?highlight=stringio#io.StringIO
sio = io.StringIO(scsv)

# https://stackoverflow.com/questions/41900593/csv-into-sqlite-table-python
# load data
df = pd.read_csv(sio)
df['Thing'] = thing

pd.sql


from pathlib import Path
filename = Path("factorio.db")

conn = sqlite3.connect(filename.absolute())

conn.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                '("item"	TEXT,'
                '"item rate"	INTEGER,'
                '"factory"	TEXT,'
                '"count"	REAL,'
                '"modules"	TEXT,'
                '"beacon module"	REAL,'
                '"beacon count"	REAL,'
                '"power"	REAL,'
                '"Thing"	TEXT,'
                'PRIMARY KEY(item,Thing))')

# https://sqlitebrowser.org/dl/

df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

conn.close()
