from Config import *

class Columns:
    '''
        Holds all the widgets for the columns and formats them as 
        defined in the self.createColumns() func.
    '''
    def __init__(self, df):
        '''
            Initialization Func.
            Setting df to be a class obj.
            Setting session variables for buttons.
            return None
        '''
        self.df = df
        if "clickedType" not in st.session_state:
            st.session_state.clickedType =  False

        if "clickedPriority" not in st.session_state:
            st.session_state.clickedPriority =  False

        if "clickedAssignee" not in st.session_state:
            st.session_state.clickedAssignee =  False

        if "clickedReporter" not in st.session_state:
            st.session_state.clickedReporter =  False

    '''
        Button Click Functions
        return None
    '''
    def clickButtonType(self):
        st.session_state.clickedType = not(st.session_state.clickedType)

    def clickButtonPriority(self):
        st.session_state.clickedPriority = not(st.session_state.clickedPriority)

    def clickButtonAssignee(self):
        st.session_state.clickedAssignee = not(st.session_state.clickedAssignee)

    def clickButtonReporter(self):
        st.session_state.clickedReporter = not(st.session_state.clickedReporter)    

    def typeBarGraph(self):
        '''
            Create Bar Graph for ticket type
            Switchable by Button
            return None
        '''
        st.button('Change to Pie Graph', key = 'Type', on_click = self.clickButtonType)
        fig = px.bar(
            self.df.groupby('Type').count().reset_index(),
            x = 'IssueKey',
            y = 'Type'
        )
        st.plotly_chart(fig)

    def typePieGraph(self):
        '''
            Create Pie Graph for ticket type
            Switchable by Button
            return None
        '''
        st.button('Change to Bar Graph',  key = 'Type', on_click = self.clickButtonType)
        fig = px.pie(
            self.df.groupby('Type').count().reset_index(),
            values = 'IssueKey',
            names = 'Type'
        )

        st.plotly_chart(fig)
    
    def typeGraph(self):
        '''
            Bar and Pie Graph for ticket type
            Switchable by Button
            return None
        '''
        st.write(r"$\textsf{\Large Types:}$")
        if st.session_state.clickedType:
            self.typeBarGraph()
        else:
            self.typePieGraph()

    def priorityBarGraph(self):
        '''
            Create Bar Graph for priority
            Switchable by Button
            return None
        '''
        st.button('Change to Pie Graph', key = 'Priority', on_click = self.clickButtonPriority)
        fig = px.bar(
            self.df.groupby('Priority').count().reset_index(),
            x = 'IssueKey',
            y = 'Priority'
        )
        st.plotly_chart(fig)

    def priorityPieGraph(self):
        '''
            Create Pie Graph for priority
            Switchable by Button
            return None
        '''
        st.button('Change to Bar Graph',  key = 'Priority', on_click = self.clickButtonPriority)
        fig = px.pie(
            self.df.groupby('Priority').count().reset_index(),
            values = 'IssueKey',
            names = 'Priority'
        )

        st.plotly_chart(fig)
    
    def priorityGraph(self):
        '''
            Bar and Pie Graph for priority
            Switchable by Button
            return None
        '''
        st.write(r"$\textsf{\Large Priority:}$")
        if st.session_state.clickedPriority:
            self.priorityBarGraph()
        else:
            self.priorityPieGraph()

    def assigneeBarGraph(self):
        '''
            Create Bar Graph for assignee
            Switchable by Button
            return None
        '''
        st.button('Change to Pie Graph', key = 'Assignee', on_click = self.clickButtonAssignee)
        fig = px.bar(
            self.df.groupby('Assignee').count().reset_index(),
            x = 'IssueKey',
            y = 'Assignee'
        )
        st.plotly_chart(fig)

    def assigneePieGraph(self):
        '''
            Create Pie Graph for assignee
            Switchable by Button
            return None
        '''
        st.button('Change to Bar Graph',  key = 'Assignee', on_click = self.clickButtonAssignee)
        fig = px.pie(
            self.df.groupby('Assignee').count().reset_index(),
            values = 'IssueKey',
            names = 'Assignee'
        )

        st.plotly_chart(fig)
    
    def assigneeGraph(self):
        '''
            Bar and Pie Graph for assignee
            Switchable by Button
            return None
        '''
        st.write(r"$\textsf{\Large Assignee:}$")
        if st.session_state.clickedAssignee:
            self.assigneeBarGraph()
        else:
            self.assigneePieGraph()

    def reporterBarGraph(self):
        '''
            Create Bar Graph for reporter
            Switchable by Button
            return None
        '''
        st.button('Change to Pie Graph', key = 'Reporter', on_click = self.clickButtonReporter)
        fig = px.bar(
            self.df.groupby('Reporter').count().reset_index(),
            x = 'IssueKey',
            y = 'Reporter'
        )
        st.plotly_chart(fig)

    def reporterPieGraph(self):
        '''
            Create Pie Graph for reporter
            Switchable by Button
            return None
        '''
        st.button('Change to Bar Graph',  key = 'Reporter', on_click = self.clickButtonReporter)
        fig = px.pie(
            self.df.groupby('Reporter').count().reset_index(),
            values = 'IssueKey',
            names = 'Reporter'
        )

        st.plotly_chart(fig)
    
    def reporterGraph(self):
        '''
            Bar and Pie Graph for reporter
            Switchable by Button
            return None
        '''
        st.write(r"$\textsf{\Large Reporter:}$")
        if st.session_state.clickedReporter:
            self.reporterBarGraph()
        else:
            self.reporterPieGraph()

    def createdHistogram(self):
        '''
            Create Histogram for Date Created
            return None
        '''
        fig = px.histogram(
            self.df,
            x = 'Created',
            nbins = 10
        )
        st.plotly_chart(fig)
        
    def updatedHistogram(self):
        '''
            Create Histogram for Date Updated
            return None
        '''
        fig = px.histogram(
            self.df,
            x = 'Updated',
            nbins = 10
        )
        st.plotly_chart(fig)

    def createColumns(self):
        '''
            Creates the columns with formatting
            return None
        '''
        column1, column2 = st.columns(2)

        with column1:
            self.typeGraph()

            st.divider()

            self.priorityGraph()

            st.divider()

            self.createdHistogram()

        with column2:
            self.assigneeGraph()

            st.divider()

            self.reporterGraph()

            st.divider()

            self.updatedHistogram()

        st.divider()
            