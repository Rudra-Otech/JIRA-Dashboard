from Config import *

class SQLProcessor:
    '''
        Handles all the SQL Processing, Includes I/O,
        filtering, updating, etc.
    '''

    def __init__(self, user, password, database, tableName, host):
        '''
            Initialization of class, Initialize sql connector,
            Initialize sql cursor, create table if not exist
            return None
        '''
        self.connector = mysql.connect(
            user = user, 
            password = password, 
            host = host,
            database = database
        )

        self.tableName = tableName

        self.cursor = self.connector.cursor(buffered=True)

        self.createTableIfNotExist()

    def createTableIfNotExist(self):
        '''
            Create table if it does not exist. 
            return None
        '''
        self.cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
                    Type VARCHAR(255), 
                    IssueKey VARCHAR(255) PRIMARY KEY, 
                    Summary VARCHAR(255), 
                    Assignee VARCHAR(255), 
                    Reporter VARCHAR(255), 
                    Priority VARCHAR(255), 
                    Status VARCHAR(255), 
                    Resolution VARCHAR(255), 
                    Created VARCHAR(255), 
                    Updated VARCHAR(255), 
                    Due_Date VARCHAR(255)
                )
            '''
        )

    def _listToStr(self, inpList):
        '''
            Represent all elements of the list in str format
            return String
        '''
        return reduce(lambda x, y: f"{x}, {y}" if x != "" else y, inpList)
    
    def _getPrimaryKey(self):
        '''
            Get the primary key column of the sql table
            return list (of primary keys)
        '''
        query = f'SELECT IssueKey FROM {self.tableName}'
        self.cursor.execute(query)
        return list(map(lambda x : x[0], self.cursor.fetchall()))
    
    def _compareSQLandJIRAEntryByKey(self, key, df, sqlTable):
        '''
            Compare entry between df and sql table
            return Boolean (Equality)
        '''
        return df.loc[df['IssueKey'] == key] != sqlTable.loc[sqlTable['IssueKey'] == key]
    
    def _removeCondition(self, key, df, sqlTable):
        '''
            Remove condition, remove entry if true
            return Boolean 
        '''
        return key not in df['IssueKey'] or self._compareSQLandJIRAEntryByKey(key, df, sqlTable)
    
    def _getRemoveEntryKeys(self, df):
        '''
            Get keys of entries to remove from sql table
            return list (of keys to remove)
        '''
        return [key for key in self._getPrimaryKey() if self._removeCondition(key, df, self.getTable())] 

    def _getNewEntries(self, df):
        '''
            Get new entires from df to add to the sql table
            return list (of entries to add)
        '''
        return df[df['IssueKey'].apply(lambda x : x not in self._getPrimaryKey())]
    
    def _removeSQLEntriesNotInDF(self, df):
        '''
            Remove entries in sql not in df
            return None
        '''
        query = f'DELETE FROM {self.tableName} WHERE IssueKey IN {tuple(self._getRemoveEntryKeys(df))}'
        self.cursor.execute(query)


    def _getInsertQueryMany(self):
        '''
            Get the query to insert many items in one line
            return String (SQL Query)
        '''
        return f'INSERT INTO {self.tableName} ({self._listToStr(DATABASE_COLUMNS)}) VALUES ({('%s, '*11)[:-2]})'

    def updateSQLTableUsingDF(self, df):
        '''
            Update the sql table using df as reference
            Remove entries in sql table but not in df 
            Add entries in df but not in sql table
            Remove and add entries not equal with df
            entry taking priority
            return None
        '''
        self._removeSQLEntriesNotInDF(df)
        
        self.cursor.executemany(self._getInsertQueryMany(), self._getNewEntries(df).values.tolist())

    def updateSQLTableUsingJIRA(self):
        '''
            Update sql table using df from jira
            return None
        '''
        self.updateSQLTableUsingDF(self.getTable())
    
    def getTable(self):
        '''
            Get sql table, return in df form
            return df (sql table)
        '''
        query = f'SELECT * FROM {self.tableName}'
        return pd.read_sql(query, self.connector)