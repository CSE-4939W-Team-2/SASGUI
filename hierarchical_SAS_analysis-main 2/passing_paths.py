import sys

#In order to import python files they have to be in your search path
#By default import, such as 'import numpy' can only find things in the directory wherever python install modules
#It is possible to add files there but it's kind of annoying
#in order to import local files they need to be in the search path
#basically instructions for how to navigate the file structure to find a file

sys.path.append('.')
#This command adds the directory where the file is called from, sometimes this is added by default. 

sys.path.append('..')
#this appends the parent directory

sys.path.append('../..')
#This adds the parent directory of the parent directory

sys.path.append('hierarchical')
#This allows python to search the hierarchical directory

sys.path.append('hierarchical/../data')
#This allows python to search the data directory inn the parent directory of the hierarchical directory
#This is equivalent to 
sys.path.append('./data')
#since this directory is the parent directory of hierarchical

# a sinngle period ./ means current directory and a double period, '../' means parent directory. One other useful shorthand is tilde, '~' which is a shortcut to your home directory
