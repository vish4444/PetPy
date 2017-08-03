import os, datetime, glob

#logdir='C:\\Users\\vishalm\\Downloads\\WeeklyIncrementalFile_UnZipped' # path to your log directory
'''
#fetching the most recent file from dir
new_files = sorted(os.listdir(logdir), key=os.path.getmtime, reverse=True)
print (new_files)
#logfiles = sorted([ f for f in os.listdir(logdir) if f.startswith('npidata_')], key = os.path.getmtime)

#print ("Most recent file = %s" % (logfiles[-1],))

'''
'''
#make folder with timestamp
def filecreation(wrkdir):
    mydir = os.path.join(wrkdir + "WeeklyIncrementalFile_UnZipped_" + datetime.datetime.now().strftime('%m-%d-%Y'))
    #print (mydir)    
    
    os.makedirs(mydir)
    return mydir
    #print (mydir)

#filecreation()
print (filecreation('C:\\Users\\vishalm\\Downloads\\'))

'''
#fetch files matching a certain pattern using glob method in a directory.
def check_glob(src):
    
    files = glob.glob(src+"*.csv")
        #src+"*.csv")
    print (files)


check_glob("C:\\Users\\vishalm\\Downloads\\WeeklyIncrementalFile_UnZipped_08-05-2016\\")
