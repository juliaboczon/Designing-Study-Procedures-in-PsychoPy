from psychopy import visual, core, monitors, gui
from psychopy.hardware import keyboard

import os
import time

import logging

logging.basicConfig(level=logging.INFO)

script_path = os.path.abspath(os.path.dirname(__file__))

results_path = script_path + '/Results/'

os.makedirs(results_path, exist_ok=True)

# GUI functions

def save_gui_data(gui_data: dict):
    
    #for key in gui_data:
    #    ...
    
    string_gui_data = ''
    
    for key, value in gui_data.items():
        string_gui_data += f'{key}: {value}\n'
    
    participant_id = gui_data['Participant ID']
    
    experiment_timestamp = time.strftime('%Y-%m-%d_%H-%M', time.gmtime())
    
    #with open('C:/Users/student/Documents/gui_data.txt', 'w', encoding='utf-8') as file:
    with open(results_path + f'gui_data_{participant_id}_{experiment_timestamp}.txt', 'w', encoding='utf-8') as file:
        file.write(string_gui_data)

def collect_gui_data():
    
    gui_dict = {'Participant ID': '',
                'Participant age': '',
                'Participant gender': ['Male', 'Female', 'Other'],
                'Handedness': ['Left', 'Right', 'Ambidextrous'],
                'Number of trials': 10,
                'Response type': ['Keyboard', 'Microphone']}
    
    gui_window = gui.DlgFromDict(gui_dict, title = 'Test title', sortKeys = False, show = False)
    
    while True:
    
        gui_data = gui_window.show()
        
        control_condition_id = len(gui_data['Participant ID']) > 0 and 'id' in gui_data['Participant ID']
        
        age_lower_limit = 18
        age_upper_limit = 80
        
        try:
            control_condition_age = int(gui_data['Participant age']) > age_lower_limit and int(gui_data['Participant age']) < age_upper_limit
            
            if gui_window.OK:
                if control_condition_id:
                    if control_condition_age:
                        logging.info(f'Collected gui data: {gui_data}')
                        save_gui_data(gui_data)
                        return
                    else:
                        warning_window = gui.Dlg(title='Age warning!')
                        warning_message = f'Participant age must be within a range of: {age_lower_limit} - {age_upper_limit}'
                        warning_window.addText(warning_message)
                        warning_data = warning_window.show()
                else:
                    warning_window = gui.Dlg(title='ID warning!')
                    warning_message = 'Participant ID missing!'
                    warning_window.addText(warning_message)
                    warning_data = warning_window.show()
            else:
                core.quit()
                
        except ValueError:
            warning_window = gui.Dlg(title='Age warning!')
            warning_message = 'Age must be a number!'
            warning_window.addText(warning_message)
            warning_data = warning_window.show()

# Instructions trial

def instruction_trial(win, kb, instruction_text):
    
    while True:
        instruction_text.draw()
        win.flip()
        
        response = kb.getKeys(keyList = ['space', 'q'])
        
        if len(response) > 0:
            if response[0].name in ['q']:
                core.quit()
            return

# Experiment trials

# Main experiment function

def experiment():
    #create a window
    
    for monitor in monitors.getAllMonitors():
        logging.info(monitor)
        
    logging.info(monitors.Monitor('testMonitor').getSizePix())
    
    collect_gui_data()
        
    win_width = monitors.Monitor('testMonitor').getSizePix()[0]
    win_height = monitors.Monitor('testMonitor').getSizePix()[1]
    
    mywin = visual.Window([win_width,win_height],fullscr = True, monitor="testMonitor", color = 'green', units="deg")
     
    #create some stimuli
    grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[-4,0], sf=3)
    fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)

    #create a keyboard component
    kb = keyboard.Keyboard()
    
    # TextStim manual: https://psychopy.org/api/visual/textstim.html#psychopy.visual.TextStim
    fixation = visual.TextStim(mywin, text = "*")
    greetings_trial = visual.TextStim(mywin, text = "Hello!")
    
    # First instruction
    instruction_trial(mywin, kb, fixation)
    instruction_trial(mywin, kb, greetings_trial)

    #draw the stimuli and update the window
    grating.draw()
    #fixation.draw()
    mywin.update()

    #pause, so you get a chance to see it!
    core.wait(2.0)

if __name__ == "__main__":
    experiment()