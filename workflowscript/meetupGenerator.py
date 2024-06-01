import textfsm
import json
import os
from datetime import datetime, timedelta

class ParsingModel:
    ''' This parser will read and parse the previous meetup information. Then, it
        will automatically generate the information of the next meetup events.
        Input : 
            fsm_template_path : Path to the TextFSM template
            rst_path : Path to the previous meetup rst file. If you don't specify 
                       the meetup rst file, it will automatically find the current
                       meetup rst file.
        Output : 
            After the __call__ process is finished, it will generate the json file 
            include the next meetup information. 
        Example : 
            fsm_template_path = './path/to/fsm_template_path'
            parsingModel = ParsingModel(fsm_template_path)
            parsingModel()
    '''
    def __init__(self, fsm_template_path, rst_path=''):
        self.fsm_template_path = fsm_template_path
        self.rst_path = rst_path
        self.result_fsm_header = None
        self.result_fsm_text = None
        self.result_json = {}
        self.meetup_file_path = './content/pages/meetup'
        self.saved_json_path = './workflowscript/meetup_information.json'
        self.startup_time = datetime.now()

    def __call__(self):
        print('-'*50)
        print('startup time : ', self.startup_time)
        self.check_rst_path()
        self.read_and_parse()
        self.two_list_to_json()
        self.update_meetup_json()
        self.save_json()
        return 

    # self-defined function
    def check_rst_path(self):
        print('The rst file is:', self.rst_path)
        if self.rst_path == '':
            print('rst file not found! Start to find rst file automatically!')
            self.get_meetup_rst_path()
        return
    
    def get_meetup_rst_path(self):
        ''' This function only get the meetup rst path file.
        '''
        days_until_previous_wednesday = (self.startup_time.weekday() - 2) % 7
        previous_wednesday = self.startup_time - timedelta(days=days_until_previous_wednesday)
        previous_wednesday_str = previous_wednesday.strftime("%m%d")
        year = str(previous_wednesday.year)

        self.meetup_file_path = os.path.join(self.meetup_file_path, year)
        try:
            files = os.listdir(self.meetup_file_path)
        except:
            print("Error! python can't find the meetup folder!")

        filtered_files = [file for file in files if file == previous_wednesday_str + "-nycu.rst"]

        # Meetup event may be paused, so we need to find the day of the previous previous_wednesday
        # and search again.
        count = 0
        while not filtered_files and count < 10:
            count += 1
            previous_wednesday -= timedelta(days=7)
            previous_wednesday_str = previous_wednesday.strftime("%m%d")
            filtered_files = [file for file in files if file == previous_wednesday_str + "-nycu.rst"]

        if len(filtered_files) != 1:
            # We didn't find the correct previous meetup rst file.
            raise Exception("Error! Can't find the previous meetup file.")
        else:
            self.rst_path = os.path.join(self.meetup_file_path, filtered_files[0])
            print(f"Found rst file: {self.rst_path}")
        return

    def read_and_parse(self):
        with open(self.rst_path, 'r', encoding='utf-8') as rst_file:
            rst_file_content = rst_file.read()
            self.parsing_file(rst_file_content)

            rst_file.close()
        return

    def parsing_file(self, rst_file_content):
        with open(self.fsm_template_path) as template_file:
            fsm = textfsm.TextFSM(template_file)
            self.result_fsm_header = fsm.header
            self.result_fsm_text = fsm.ParseText(rst_file_content)

            # We should only get one result from parser
            if len(self.result_fsm_text) > 1:
                raise Exception('!!! MULTIPLY RESULT !!!')
            else:
                # extract the only one list in the self.result_fsm_text
                self.result_fsm_text = self.result_fsm_text[0]

            self.print_parsed_result()

            template_file.close()
        return

    def print_parsed_result(self):
        print("The parsed information : ")
        for key, val in zip(self.result_fsm_header, self.result_fsm_text):
            print("{:<20}".format(key), val)
        return
    
    def two_list_to_json(self):
        ''' Give the two list, self.result_fsm_header and self.result_text, we 
            support that self.result_text only contain one list. We will 
            return the dict that the key is result_fsm_header and the val is
            resutl_text
        '''
        for key, val in zip(self.result_fsm_header, self.result_fsm_text):
            self.result_json[key] = val
        return 
    
    def update_meetup_json(self):
        ''' This function only update the information of meetup event. After we got
            the old meetup rst file information and saved to result_json, we need to 
            update the new meetup information.
        '''
        # get the information of next Wednesday
        days_to_next_wednesday = (9 - self.startup_time.weekday()) % 7
        if days_to_next_wednesday == 0:
            days_to_next_wednesday = 7
        next_wednesday = self.startup_time + timedelta(days=days_to_next_wednesday)

        # update json information
        self.result_json["EVENT_YEAR"] = str(next_wednesday.year)
        self.result_json["EVENT_MONTH"] = next_wednesday.strftime("%B")
        day = next_wednesday.strftime("%d").lstrip("0").replace(" 0", " ")
        self.result_json["EVENT_DATE"] = day + self.get_day_suffix(int(day))
        self.result_json["FILE_CREATE_DATE"] = next_wednesday.strftime("%Y-%m-%d %H:%M")
        self.result_json["FILE_URL"] = 'meetup/' + self.result_json["EVENT_YEAR"] + '/' + next_wednesday.strftime("%m%d") + '-nycu'
        self.result_json["FILE_SAVE_AS"] = self.result_json["FILE_URL"] + '.html'
        return
    
    def get_day_suffix(self, day):
        return {1:'st',2:'nd',3:'rd'}.get(day % 20, 'th')

    def save_json(self):
        json_data = json.dumps(self.result_json, indent=4, ensure_ascii=False)
        print("The saved json file : ")
        print(json_data)
        
        with open(self.saved_json_path, 'w', encoding='utf-8') as json_file: 
            json_file.write(json_data)
            json_file.close()
        return
# END class ParsingModel
