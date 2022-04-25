import argparse  # args <- command string
import getpass  # args <- keyboard
from eis_jira import Jira
import eis_presentation

# Constants
# '22.3 Policy P&C Backend'  # '21.6 Policy P&C UI'
PPTX_TEMPLATE_FILE = "Genesis Sprint Review template.pptx"
PPTX_LOCAL_DIR = "presentation"
PPTX_REPLACE_SUBSTR = "template"


def parse_args():
    parser = argparse.ArgumentParser(description='Export sprint JIRA tickets to a sprint presentation')
    parser.add_argument('sprint', type=str, help='Sprint name (for example, "20.1 Policy P&C Backend")')
    parser.add_argument('login', type=str, help='JIRA login')
    parser.add_argument('password', type=str, help='JIRA password')

    args = parser.parse_args()
    return args.sprint, args.login, args.password


def request_args():
    print("Default JIRA sprint: " + SPRINT)
    sprint_new = input("Enter new JIRA Sprint (enter - leave default): ").strip()
    sprint = sprint_new if sprint_new else SPRINT
    login = input("JIRA User Login: ")
    password = getpass.getpass("JIRA User Password: ")
    return sprint, login, password


def main():
    jira = Jira()
    # jira, pptx = Jira(), PPTX()

    sprint, login, password = parse_args()
    jira.connect_to_jira(login, password)
    issues = jira.get_sprint_info(sprint)
    jira.print_sprint_info(issues)
    jira.print_sprint_info_by_rmap(issues)
    # pptx.export_sprint_issues(sprint, issues)


main()
