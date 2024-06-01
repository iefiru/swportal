import click
from workflowscript.meetupGenerator import ParsingModel

SESH_TOKEN=""
@click.command()
@click.option('-t', '--token', 'SESH token', help='SESH Token')
def meetup_handle(token):
    SESH_TOKEN = token
    print(f'SESH_TOKEN, { SESH_TOKEN or "stranger"}!')
    
    
    # get the template file path
    fsm_template_path = './workflowscript/meetup.template'

    # test on rst file
    parsingModel = ParsingModel(fsm_template_path)
    parsingModel()


if __name__ == '__main__':
    meetup_handle()
