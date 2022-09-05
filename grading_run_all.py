import os

# this script is used for grading
# it calls all python files from the present/current working directory (pwd/cwd)
# in any subfolder

# this obviously has security ramifications, so we only use this for grading...

# if students followed instructions, one can then look over their printed output
# to see if it matches the expected values

# common issues and rubric:
# scored out of 100
# 1) -1pt: student submits .ipynb: manually convert via Jupyter (load it download as .py)
# 2) -1pt: student doesn't print any or all tests (add tests)
# 3) -1pt to -5pts: some minor issue with edge cases not working or some 
#    minor error where values don't quite match expected
# 4) discretionary: some major issue, please let professors know and we will look

rootdir = os.fsencode(os.getcwd())
this_script_name = os.path.basename(__file__)

# recursively iterative over all subdirectories and files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print(subdir)
        #print(file)
        
        filename = os.fsdecode(file)
        # check if python files (requested to submit .py)
        if filename.endswith(".py"):
            fps = os.fsdecode(subdir) + os.sep + os.fsdecode(file)
            print(fps)
            
            
            
            # don't call this script itself again
            if filename.startswith( this_script_name ):
                continue
            # otherwise, call python on the identified file
            else:
                # put file in quotes in case it has spaces, etc., may
                # need to check cross-platform compatibility
                os.system('python "' + fps + '"')
            print()
