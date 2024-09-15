from Config import *

class Sidebar():
    '''
        Class Sidebar:
        Holds all the widgets for the sidebar and formats them as 
        defined in the self.createSidebar() func.
    '''
    def __init__(self, df):
        '''
            Initialization Func. 
            Setting the df to be a class obj.
            return None
        '''
        self.df = df 

    def refresh(self, sql):
            '''
            Create a new Profile Report and save it,
            Update sql table using jira df
            '''
            ProfileReport(self.df).to_file('./App/Profile Report.html')
            sql.updateSQLTableUsingJIRA()
        
    def refreshData(self, sql):
        '''
            Button to refresh data,
            sql = SQL object, jira = JIRAPocessor object
            return None
        '''

        st.button('Refresh Data', key = 'RefreshData', on_click = lambda : self.refresh(sql))
        
    def typeSelectbox(self):
        '''
            Selector For Type Of Ticket
            return None
        '''
        typeList = sorted(list(self.df['Type'].unique()))
        typeList.insert(0, 'All')
        
        self.selectedTypeType = st.selectbox(
            'Select Type of Type:', 
            typeList
        )
    
    def assigneeSelectbox(self):
        '''
            Selector For Assignee
            return None
        '''
        assigneeList = sorted(list(self.df['Assignee'].unique()))
        assigneeList.insert(0, 'All')
        
        self.selectedAssignee = st.selectbox(
            'Select Assignee:',
            assigneeList
        )
    
    def reporterSelectbox(self):
        '''
            Selector For Reporter
            return None
        '''
        reporterList = sorted(list(self.df['Reporter'].unique()))
        reporterList.insert(0, 'All')
        
        self.selectedReporter = st.selectbox(
            'Select Reporter:',
            reporterList
        )

    def prioritySlider(self):
        '''
            Selector For Priority
            return None
        '''    
        self.selectedPriority = st.select_slider(
            'Select Priority:',
            ['Highest', 'High', 'Medium', 'Low', 'Lowest', 'Any'][::-1]
        )

    def createdDateSlider(self):
        '''
            Selector For Creation Date
            return None
        '''
        st.write('Created:')
        self.selectedCreatedFrom = st.select_slider(
            'From:',
            self.df['Created'].sort_values(ascending = False),
            value = self.df['Created'].iloc[-1],
            key = 'createdFrom'
        )

        self.selectedCreatedTo = st.select_slider(
            'To:',
            self.df['Created'].sort_values(ascending = False),
            key = 'createdTo'
        )
    
    def updatedDateSlider(self):
        '''
            Selector For Update Date
            return None
        '''
        st.write('Updated:')
        self.selectedUpdatedFrom = st.select_slider(
            'From:',
            self.df['Updated'].sort_values(ascending = False),
            value = self.df['Updated'].iloc[-1],
            key = 'updatedFrom'
        )

        self.selectedUpdatedTo = st.select_slider(
            'To:',
            self.df['Updated'].sort_values(ascending = False),
            key = 'updatedTo'
        )

    def title(self):
        columns = st.columns([1, 3])
        with columns[0]:
            st.image('./App/logo.jpg')
        with columns[1]:
            st.title('JIRA Dashboard')

    def createSidebar(self, sql, jira):
        '''
            Creates the sidebar with formatting
            return None
        '''
        with st.sidebar:
            
            self.title()

            st.divider()
            
            self.refreshData(sql)

            st.divider()

            self.typeSelectbox()
            self.assigneeSelectbox()
            self.reporterSelectbox()

            st.divider()

            self.prioritySlider()

            st.divider()

            self.createdDateSlider()
            
            st.write('')
            st.write('')

            self.updatedDateSlider()
