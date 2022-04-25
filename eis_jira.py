# Python JIRA library
# https://jira.readthedocs.io/en/master/
import urllib.parse
from eis_string import *
from jira.client import JIRA

JIRA_SERVER = "https://jira.exigeninsurance.com"
JIRA_SERVER_BROWSE = "https://jira.exigeninsurance.com/browse/"


class Jira:
    jira_connection: JIRA
    sprint_issues: object

    # -----------------------------------------------------------------------------------------
    def connect_to_jira_(self, jira_server, jira_user, jira_password):
        try:
            print("Connection to JIRA...")
            jira_options = {'server': jira_server}
            self.jira_connection = JIRA(options=jira_options, basic_auth=(jira_user, jira_password))
        except Exception as e:
            print("Failed to connect to JIRA: %s" % e.text)
            self.jira_connection = None
            exit(-1)


    # -----------------------------------------------------------------------------------------
    def connect_to_jira(self, jira_user, jira_password):
        self.connect_to_jira_(JIRA_SERVER, jira_user, jira_password)


    # -----------------------------------------------------------------------------------------
    def get_sprint_issues(self, sprint_name):
        jql = 'Sprint = "' + sprint_name + '" AND summary !~ req AND type in ("New Feature", Improvement, Spike, Task) ORDER BY rank'
        try:
            issues = self.jira_connection.search_issues(jql)
        except Exception as e:
            print("Failed to retrieve the issues: %s" % e.text)
            exit(-1)
        return issues

    # -----------------------------------------------------------------------------------------
    def get_issue_rmap(self, issue):
        for issue_link in issue.fields.issuelinks:
            if issue_link.type.name == "Uber Epic Link":
                return issue_link

    # -----------------------------------------------------------------------------------------
    def get_standart_issue_fields(self, issue):
        issue_attr_str = {
            'Issue': 'key'
        }
        issue_fields_attr_str = {
            'Issue Summary': 'summary',
            'Status': 'status',
            'Scope Summary': 'customfield_20342',
            'Wiki Ticket Summary Link': 'customfield_27540',
            'EISDEVTS Issue ID': 'customfield_28344',
            'DGIG Gating': 'customfield_30041',
            'User Story': 'description',
            'Epic Issue': 'customfield_11843'
        }
        issue_fields_attr_num = {
            'Story Points': 'customfield_10391'
        }

        fields = {}
        for attr in issue_attr_str:
            fields[attr] = str(getattr(issue, issue_attr_str[attr], '') or '')\
                            .replace('\n', ' ').replace('\r', ' ')
        for attr in issue_fields_attr_str:
            fields[attr] = str(getattr(issue.fields, issue_fields_attr_str[attr], '') or '')\
                            .replace('\n', ' ').replace('\r', ' ')
        for attr in issue_fields_attr_num:
            fields[attr] = getattr(issue.fields, issue_fields_attr_num[attr], 0) or 0
        return fields

    # -----------------------------------------------------------------------------------------
    def get_issue_fields(self, issue):
        fields = self.get_standart_issue_fields(issue)
        #
        fields["Issue Link"] = urllib.parse.urljoin(JIRA_SERVER_BROWSE, fields["Issue"])
        fields["EISDEVTS Issue Link"] = urllib.parse.urljoin(JIRA_SERVER_BROWSE, fields["EISDEVTS Issue ID"])
        #
        x = fields["Story Points"]
        fields["Story Points"] = str(x if x % 1 != 0 else int(x))
        #
        fields["User Story"] = \
            trim_hidden_symbols(
                get_text_between(
                    fields["User Story"],
                    "h2. User Story",
                    "h2. Scope"))
        #
        if fields['Epic Issue'] not in (None, ''):
            fields["Epic Link"] = {}
            fields["Epic Link"]["Issue"] = getattr(issue.fields, 'customfield_11843', '') or ''
            fields["Epic Link"]["Issue Link"] = urllib.parse.urljoin(JIRA_SERVER_BROWSE, fields["Epic Link"]["Issue"])
            #
            epic_issue = self.jira_connection.issue(fields["Epic Link"]["Issue"])
            fields["Epic Link"]["Issue Summary"] = getattr(epic_issue.fields, 'summary', '') or ''
            #
            rmap_issue = self.get_issue_rmap(issue)
            if rmap_issue is None:
                rmap_issue = self.get_issue_rmap(epic_issue)
            if rmap_issue is not None:
                fields["RMAP Link"] = {}
                fields["RMAP Link"]["Issue"] = getattr(rmap_issue.inwardIssue, 'key', '') or ''
                fields["RMAP Link"]["Issue Link"] = urllib.parse.urljoin(JIRA_SERVER_BROWSE, fields["RMAP Link"]["Issue"])
                fields["RMAP Link"]["Issue Summary"] = getattr(rmap_issue.inwardIssue.fields, 'summary', '') or ''

        return fields

    # -----------------------------------------------------------------------------------------
    def get_sprint_info(self, sprint):
        self.sprint_issues = []
        for issue_key in self.get_sprint_issues(sprint):
            issue = self.jira_connection.issue(issue_key)
            fields = self.get_issue_fields(issue)
            self.sprint_issues.append(fields)
        return self.sprint_issues

    # -----------------------------------------------------------------------------------------
    @classmethod
    def print_issue_fields(self, issue, indent=''):
        #sfor field in issue:
        for field in ['Issue', 'Issue Link', 'Issue Summary', 'Scope Summary', 'Status', 'Epic Link', 'RMAP Link']:
            if field in issue:
                print(indent + field + ": " + str(issue[field]))


    # -----------------------------------------------------------------------------------------
    @classmethod
    def print_sprint_info(self, issue_list):
        for fields in issue_list:
            print("--------------------------------------------------------")
            for field in fields:
                print(field + ": " + str(fields[field]))

    # -----------------------------------------------------------------------------------------
    @classmethod
    def print_sprint_info_by_rmap(self, issue_list):
        # group issues by: rmap, epic
        rmap_issue_list = {}
        for issue in issue_list:
            rmap_issue = issue["RMAP Link"]["Issue"] if "RMAP Link" in issue else '-'
            epic_issue = issue["Epic Link"]["Issue"] if "Epic Link" in issue else '-'
            if rmap_issue not in rmap_issue_list:
                rmap_issue_list[rmap_issue] = {}
            if epic_issue not in rmap_issue_list[rmap_issue]:
                rmap_issue_list[rmap_issue][epic_issue] = []
            rmap_issue_list[rmap_issue][epic_issue].append(issue)

        # # print grouped values
        # print('\n'*3)
        # for rmap_issue in rmap_issue_list:
        #     print('=== RMAP: %s ================================================================='%(rmap_issue))
        #     for epic_issue in rmap_issue_list[rmap_issue]:
        #         print(' ' * 2 + '=== EPIC: %s ================================================================='%(epic_issue))
        #         for issue in rmap_issue_list[rmap_issue][epic_issue]:
        #             print(' ' * 4 + '=== Issue: %s =================================================================' % (issue['Issue']))
        #             self.print_issue_fields(issue, ' ' * 6)

        # print grouped values
        print('\n'*3)
        for rmap_issue in rmap_issue_list:
            print('=== RMAP: %s ================================================================='%(rmap_issue))
            for epic_issue in rmap_issue_list[rmap_issue]:
                print(' ' * 2 + '=== EPIC: %s ================================================================='%(epic_issue))
                for issue in rmap_issue_list[rmap_issue][epic_issue]:
                    print(' ' * 4 + '=== Issue: %s =================================================================' % (issue['Issue']))
                    self.print_issue_fields(issue, ' ' * 6)