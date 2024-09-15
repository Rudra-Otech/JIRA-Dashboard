from Config import *
from DataProcessors import *
from PageComponents import *

def main():
    '''
        The entire webpage
        return None
    '''

    st.set_page_config(
        page_title="JIRA Dashboard",
        page_icon="./App/logo.jpg",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    alt.themes.enable("dark")

    jira = JIRAProcessor('rudrar@otech.com', JIRA_API_TOKEN)

    sql = SQLProcessor(
        user = SQL_USER,
        password = SQL_PASSWORD,
        host = SQL_HOST,
        database = SQL_DATABASE,
        tableName = SQL_TABLE_NAME
    )

    df = sql.getTable().sort_values('Created', ascending = False).reset_index().drop(columns='index')

    #df = pd.read_excel('./App/ExampleTable.xlsx').sort_values('Created', ascending = False).reset_index().drop(columns='index')
    
    sidebar = Sidebar(df)
    sidebar.createSidebar(sql, jira)

    dataset = DatasetDisplay(df)
    df = dataset.selectDF(sidebar)

    columns = Columns(df)
    columns.createColumns()

    dataset.createDatasetRow()

if __name__ == "__main__":
    main()