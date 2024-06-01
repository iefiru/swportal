from workflowscript.meetupGenerator import ParsingModel

if __name__ == '__main__':
    # get the template file path
    fsm_template_path = './workflowscript/meetup.template'

    # test on rst file
    parsingModel = ParsingModel(fsm_template_path)
    parsingModel()