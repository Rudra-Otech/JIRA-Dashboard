from Config import *

class JIRAProcessor:
    '''
        Handles all the JIRA Processing, Includes I/O,
        filtering, updating, etc.
    '''

    def __init__(self, email, apiTokenKey):
        '''
            Initialization, connect to JIRA and authenticate,
            set class df obj to store data
            return None
        '''
        self.jira = JIRA(
            server=JIRA_SERVER_ADDRESS,
            basic_auth = (email, apiTokenKey)
        )

        self.df = pd.DataFrame(columns = DATABASE_COLUMNS)

    def _getAllIssueFields(self, issue):
        '''
            Get the tuple of all the issue fields
            return tuple (all fields)
        '''
        return(
            issue.fields.issuetype, 
            issue, 
            issue.fields.summary, 
            issue.fields.assignee, 
            issue.fields.reporter, 
            issue.fields.priority, 
            issue.fields.status, 
            issue.fields.resolution, 
            str(
                dt.datetime.strptime(
                    issue.fields.created.split('T')[0], '%Y-%m-%d'
                )
            ).split(' ')[0], 
            str(
                dt.datetime.strptime(
                    issue.fields.statuscategorychangedate.split('T')[0], '%Y-%m-%d'
                )
            ).split(' ')[0],
            issue.fields.duedate
        )

    def _processIssueIntoDF(self, issue):
        '''
            Create a df from all the issue fields in the issue
            return df (of all issues)
        '''
        return pd.DataFrame(
            {
                column : str(issueField)
                for column, issueField in zip(
                    DATABASE_COLUMNS,
                    self._getAllIssueFields(issue)
                )
            }, 
            index = [0]
        )

    def _updateDFWithNewIssue(self, issue):
        '''
            Update current df with new issue.
            Concatenate new df with old df, drop dupes
            return df (updated df)
        '''
        self.df = pd.concat(
            (
                self.df, 
                self._processIssueIntoDF(issue)
            ), 
            ignore_index=True
        )

        self.df.drop_duplicates(inplace=True)
    
    def _processAllIssuesAndUpdateDF(self, issues):
        '''
            Update current df with all issues.
            return None
        '''
        for issue in issues:
                self._updateDFWithNewIssue(issue)
    
    def updateFromJIRA(self):
        '''
            Update current df with all issues from JIRA
            return df (updated df)
        '''
        size = 100
        initial = 0
        while True:
            start= initial * size
            issues = self.jira.search_issues(f'project={JIRA_PROJECT_NAME}', start, size)
            if len(issues) == 0:
                break
            initial += 1
            self._processAllIssuesAndUpdateDF(issues)
        
        return self.df