'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
'''

# External imports
import json, os

# Internal imports
from src.ImageHandler.image_handler import open_image
from src.Clients.user import client
from src.Logger.log import write_log, write_error
from src.CSV import reader

def check_directories(*directories ) -> bool:
    ''' 
    Make sure that CSV and images directories exist.
    Then ensure that there are files contained within.
    '''
    # For all directories passed into funciton 
    # Check if they exist
    for arg in directories:
        if not(os.path.exists(arg)):
            write_error(FileNotFoundError(f'FILE: File or directory MISSING: {arg}'))
            return False
        else:
            write_log(f'File: "{arg}" found.')
    
    # If all directories exist return true
    return True

# Main function
def main():
    ''' Main function for controlling application flow'''



    # Initalise settings for the program
    try:
        # Open json file for settings
        settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
    
    except:
        print("Error reading settings file! Please ensure file exists and is valid!")
        return
    
    # Check that files and directories exist
    if not(check_directories(
        settings['working_path'], 
        settings['csv_filename'],
        settings['images_path']
        )):
        print('Program cannot continue due to fatal error processing files')
        return

    write_log("File: Checks Complete. Starting Client Generation")


    # Create CSV reader
    file_reader: reader.Reader = reader.csv_reader(settings['csv_filename'])
    list_of_clients = file_reader.get_clients()

    for student in list_of_clients:
        write_log(f'Current Student: {student}')

        # confirm user's image exists in directory
        img = open_image(
            settings['working_path'],
            settings['images_path'],
            student['image_filename']
        )
        if img == None:
            write_error(FileNotFoundError(f'FILE: {student["image_filename"]} cannot be found'))
            write_log(f'USER: user, {student["client_id"]} Skipped as no image could be found')
            continue
        else:
            # Create user object

            user: client = client(
                student['client_id'], 
                img
                )

        print(user)
        '''
        TODO: Find a way to create the user object so that MAIN does not need to be aware of clients. 
        This may need a controller or something along those lines. 
        '''
        '''
        TODO: Main is too busy. This needs to be a more single responsiblity function. rewrite this so
        that main is only responsible for working with the controlers. This may mean creating 
        some controllers. 
        '''


        #Step 0: Get canvas user ID via SIS ID

        # Step 1: Start upload file to user's file storage

        # Step 2: Upload Data

        # Step 3: Confirm Upload

        # Step 4: Make API call to set avatar image
    pass

if __name__ == '__main__':
    # If module is run by itself then run main
    main()