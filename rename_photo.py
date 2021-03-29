#! /usr/bin/python3

import os
import os.path
import shutil
import argparse
import pathlib

class ChangePhotoNames(object):
    '''Class for processing every directory at topdir and potentially renaming all the
    files in the subdirectory to be subdirName_fileName.fileExt
    It will prompt at each subdirectory to see if those files should be renamed.

    This is built for the case where the subdirectory is a useful name for the context of
    the photos inside (like "2020-07 Fourth of July in California") and the filenames in
    the subdirector are not helpful (like "005.jpg", "006.jpg", etc.).  Running this
    will give the opportunity to rename the files "2020-07 Fourth of July in California_005.jpg".
    '''

    def __init__(self):
        '''Initialize'''
        self.topdir = None
        self.recursive = False
        self.noprompt = True
        self.testrun = False

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Rename Photo files to include containing directory name')
        parser.add_argument('topdir', type=pathlib.Path, help='top directory to begin processing')
        parser.add_argument('-r', '--recursive', action='store_true', help='process subdirectories recursively')
        parser.add_argument('-t', '--testrun', action='store_true', help='print out a testrun without taking action')
        parser.add_argument('-y', '--noprompt', action='store_true', default=False, help="Don't prompt for confirmation for each directory/subdirectory")
        args = parser.parse_args()
        self.topdir = vars(args)['topdir']
        self.recursive = vars(args)['recursive']
        self.noprompt = vars(args)['noprompt']
        self.testrun = vars(args)['testrun']

    def prompt_user(self, question, options=['yes', 'no']):
        '''Prompt for an answer on the terminal'''
        answerdict = {num+1: answer for num, answer in enumerate(options)}
        answers = ', '.join([f'{num+1}: {answer}' for num, answer in enumerate(options)])
        answers = answers + ", q: Quit"
        valid_response = False
        while not valid_response:
            try:
                response = input(f'--> {question}: [{answers}]: ')
                if response in ['q', 'Q']:
                    return 'q'
                if int(response) in answerdict:
                    valid_response =  True
            except Exception:
                pass
        return answerdict[int(response)]

    def start_interactive(self):
        for root, dirs, files in os.walk(self.topdir, 
                                        topdown=True, 
                                        onerror=None, 
                                        followlinks=False):
            if len(files) > 0:
                answer = 'yes'
                if not self.noprompt:
                    print(f'\nDirectory {root}\nSample filnemae: {files[0]}')
                    answer = self.prompt_user(f'Would you like to rename files in this directory?')
                    if answer == 'q':
                        return
                if answer == 'yes':
                    for file in files:
                        new_name = f'{os.path.basename(root)}_{file}'
                        if self.testrun:
                            print(f'Renames {os.path.join(os.path.basename(root), file)} to {os.path.join(os.path.basename(root), new_name)}')
                        else:
                            print(f'{os.path.join(os.path.basename(root), file)} --> {os.path.join(os.path.basename(root), new_name)}')
                            os.rename(os.path.join(root, file), os.path.join(root, new_name))
            if not self.recursive:
                return

if __name__ == '__main__':
    cpn = ChangePhotoNames()
    cpn.parse_arguments()
    #print(vars(cpn))
    cpn.start_interactive()

