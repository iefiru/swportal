import click
from workflowscript.meetupGenerator import ParsingModel

SESH_TOKEN=""
USER_ID=""
@click.command()
@click.option('-t', '--token', help='SESH Token')
@click.option('-u', '--user', help='SESH UserID')
def meetup_handle(token, user):
    SESH_TOKEN = token
    USER_ID = user
    print(f'SESH_TOKEN, {SESH_TOKEN}!')
    print(f'USER_ID, {USER_ID}!')
    
    
    # get the template file path
    fsm_template_path = './workflowscript/meetup.template'

    # test on rst file
    parsingModel = ParsingModel(fsm_template_path)
    parsingModel()


if __name__ == '__main__':
    meetup_handle()
