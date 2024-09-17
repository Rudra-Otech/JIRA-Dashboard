from Config import *

class DatasetDisplay:
    '''
        Holds all the widgets for the dataset area and formats them as 
        defined in the self.createDatasetRow() func.
    '''
    def __init__(self, df):
        '''
            Initialization Func. 
            Setting the df to be a class obj.
            return None
        '''
        self.df = df
    
    def selectDF(self, sidebar):
        '''
            Selecting a subset of the df according to the conditions
            given in the sidebar. Setting selected df as the new df
            return df (selected subset of df)
        '''
        self.df = self.df[
            self.df['Type'].isin((sidebar.selectedTypeType,) if sidebar.selectedTypeType != 'All' else self.df['Type']) &
            self.df['Assignee'].isin((sidebar.selectedAssignee,) if sidebar.selectedAssignee != 'All' else self.df['Assignee']) &
            self.df['Reporter'].isin((sidebar.selectedReporter,) if sidebar.selectedReporter != 'All' else self.df['Reporter']) &
            self.df['Priority'].isin((sidebar.selectedPriority,) if sidebar.selectedPriority != 'Any' else self.df['Priority']) &
            (self.df['Created'] >= sidebar.selectedCreatedFrom) & (self.df['Created'] <= sidebar.selectedCreatedTo) &
            (self.df['Updated'] >= sidebar.selectedUpdatedFrom) & (self.df['Updated'] <= sidebar.selectedUpdatedTo)
        ].reset_index().drop(columns='index')

        return self.df
    
    def defineDaysSinceAndPLevel(self):
        '''
            Try creating columns for days since created and updated,
            and priority level. Fails if improper data, display
            appropriate message.
            return None
        '''
        try:
            self.df['Created'] = pd.to_datetime(self.df['Created'])
            self.df['Updated'] = pd.to_datetime(self.df['Updated'])

            daysSince = lambda x : (dt.date.today() - x.date()).days
            self.df['Days Since Created'] = self.df['Created'].apply(daysSince)
            self.df['Days Since Update'] = self.df['Updated'].apply(daysSince)

            self.df['Created'] = self.df['Created'].astype(str)
            self.df['Updated'] = self.df['Updated'].astype(str)

            self.df['Priority Level'] = self.df['Priority'].apply(lambda x : {'Lowest' : 0, 'Low' : 1, 'Medium' : 2, 'High' : 3, 'Highest' : 4}[x])
        except :
            st.write("Error: Could not create days since or priority columns, likely due to improper data")

    def writeStatistics(self):
        '''
            Try showing statistics for days since created, days since
            updated and priority level. Fails if insufficient/improper
            data.
            return None
        '''
        try:
            daysSinceCreated = self.df['Days Since Created']
            daysSinceUpdate = self.df['Days Since Update']
            priorityLevel = self.df['Priority Level']
            st.write(f'Days Since Created: Min = {daysSinceCreated.min()}; Max = {daysSinceCreated.max()}; Avg = {round(daysSinceCreated.mean(), 3)}; Median = {daysSinceCreated.median()}; SD = {round(daysSinceCreated.std(), 3)}')
            st.write(f'Days Since Updated: Min = {daysSinceUpdate.min()}; Max = {daysSinceUpdate.max()}; Avg = {round(daysSinceUpdate.mean(), 3)}; Median = {daysSinceUpdate.median()}; SD = {round(daysSinceUpdate.std(), 3)}')
            st.write(f'Priority Level: Min = {priorityLevel.min()}; Max = {priorityLevel.max()}; Avg = {round(priorityLevel.mean(), 3)}; Median = {priorityLevel.median()}; SD = {round(priorityLevel.std(), 3)}')
        except:
            st.write("Error: Statistics Not Available, likely due to insufficient data")

    def showProfilingReport(self):
        '''
            Show the profiling report saved
            return None
        '''
        with open('./PageComponents/Profile Report.html', 'r') as profileReport:
            profileReportHTML = profileReport.read()
        st.components.v1.html(profileReportHTML, scrolling=True, height=700)
        
    def createDatasetRow(self):
        '''
            Creates the dataset row with formatting
            Trying to get statistics if possible
            Showing entire df
            return None
        '''
        
        self.defineDaysSinceAndPLevel()
        
        st.write(r"$\textsf{\LARGE Dataset:}$")
        st.write(f'Total number of Types in the selected dataset : {self.df.shape[0]}')

        self.writeStatistics()

        st.dataframe(self.df.sort_values('Created', ascending=True).reset_index().drop(columns='index'))

        self.showProfilingReport()
