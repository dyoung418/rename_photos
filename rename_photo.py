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

    def __init__(self, topdir=None, recursive=False, noprompt=False, testrun=False, newdir=None):
        '''Initialize'''
        self.topdir = topdir
        self.recursive = recursive
        self.noprompt = noprompt
        self.testrun = testrun
        self.newdir = newdir

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Rename Photo files to include containing directory name')
        parser.add_argument('topdir', type=pathlib.Path, help='top directory to begin processing')
        parser.add_argument('-r', '--recursive', action='store_true', help='process subdirectories recursively')
        parser.add_argument('-t', '--testrun', action='store_true', help='print out a testrun without taking action')
        parser.add_argument('-y', '--noprompt', action='store_true', default=False, help="Don't prompt for confirmation for each directory/subdirectory")
        parser.add_argument('--newdir', default=None, help="specifies a new directory to move the newly renamed files to. By default, files are renamed within their current directory")
        args = parser.parse_args()
        self.topdir = vars(args)['topdir']
        self.recursive = vars(args)['recursive']
        self.noprompt = vars(args)['noprompt']
        self.testrun = vars(args)['testrun']
        self.newdir = vars(args)['newdir']

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
        '''begin renaming files, following options for whether to do it recursively and whether to prompt'''
        for root, dirs, files in os.walk(self.topdir, 
                                        topdown=True, 
                                        onerror=None, 
                                        followlinks=False):
            if self.newdir:
                destdir = self.newdir
            else:
                destdir = root
            if len(files) > 0:
                answer = 'yes'
                move_answer = None
                if not self.noprompt:
                    if len(files) >=3:
                        print(f'\nDirectory {root}\nSample filename: {files[0]}\n                 {files[1]}\n                 {files[2]}')
                    else:
                        print(f'\nDirectory {root}\nSample filename: {files[0]}')                        
                    answer = self.prompt_user(f'Would you like to rename files in this directory?')
                    if answer == 'q':
                        return
                    if (answer != 'yes') and (self.newdir):
                        move_answer = self.prompt_user(f'--would you like to move the files to {self.newdir} (but not rename)?')
                if answer == 'yes':
                    for file in files:
                        if move_answer:
                            new_name = file
                        else:
                            new_name = f'{os.path.basename(root)}_{file}'

                        if self.testrun:
                            print(f'Renames {os.path.join(os.path.basename(root), file)} to {os.path.join(os.path.basename(destdir), new_name)}')
                        else:
                            print(f'{os.path.join(os.path.basename(root), file)} --> {os.path.join(os.path.basename(destdir), new_name)}')
                            os.rename(os.path.join(root, file), os.path.join(destdir, new_name))
                if (self.newdir) and (move_answer == 'yes'):
                    for file in files:
                        if self.testrun:
                            print(f'Moves {os.path.join(os.path.basename(root), file)} to {os.path.join(os.path.basename(destdir), file)}')
                        else:
                            print(f'{os.path.join(os.path.basename(root), file)} --> {os.path.join(os.path.basename(destdir), file)}')
                            self.move_file_to_new_directory(os.path.join(root, file), destdir)
            if not self.recursive:
                return

    def rename_in_place(self, current_pathname, new_filename):
        os.rename(current_pathname, os.path.join(os.path.dirname(current_pathname), new_filename))

    def move_file_to_new_directory(self, current_pathname, new_directory):
        os.rename(current_pathname, os.path.join(new_directory, os.path.basename(current_pathname)))

if __name__ == '__main__':
    cpn = ChangePhotoNames()
    cpn.parse_arguments()
    #print(vars(cpn))
    cpn.start_interactive()

