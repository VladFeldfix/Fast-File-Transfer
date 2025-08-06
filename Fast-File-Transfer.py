# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import shutil

if not os.path.isfile("plugins.py"):
    file = open("plugins.py", 'w')
    file.write("list_of_plugins = {}\n")
    file.close()

import plugins
from plugins import list_of_plugins


# launch
class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sv = "2.0"
        self.sc = SmartConsole("Fast File Transfer", self.sv)

        # set-up main memu
        if len(list_of_plugins) > 0:
            for key, plugin in list_of_plugins.items():
                self.sc.add_main_menu_item("RUN PLUGIN: "+plugin[0], self.filtered_run)
        self.sc.add_main_menu_item("RUN", self.run)

        # get settings
        self.path_from = self.sc.get_setting("From")
        self.path_to = self.sc.get_setting("To")
        self.logs = self.sc.get_setting("Logs")

        # test all paths
        self.sc.test_path(self.path_from)
        self.sc.test_path(self.path_to)
        self.sc.test_path(self.logs)

        # display main menu
        self.sc.start()
    
    def run(self):
        # transfer file according to filter
        self.path_from = self.path_from.replace("\\","/")
        self.path_to = self.path_to.replace("\\","/")
        index = 0
        log = ""
        logname = self.sc.current_year()+self.sc.current_month()+self.sc.current_day()+self.sc.current_hour()+self.sc.current_minute()+self.sc.current_second()+".txt"
        start = self.sc.today()+" "+self.sc.right_now()
        log += "-----------------------------------------------\n"
        log += "Fast File Transfer"+" v"+self.sv+"\n"
        log += "Date and time: "+start+"\n"
        log += "From: "+self.path_from+"\n"
        log += "To: "+self.path_to+"\n"
        log += "-----------------------------------------------\n"

        # make a list of files in path from
        from_files = []
        self.sc.print("Reading files from source...")
        for path, dirnames, filenames in os.walk(self.path_from):
            for file in filenames:
                path = path.replace("\\","/")
                path = path.replace(self.path_from, "")
                from_files.append(path+"/"+file)

        # make a list of files in path to
        to_files = []
        self.sc.print("Reading files from destination...")
        for path, dirnames, filenames in os.walk(self.path_to):
            for file in filenames:
                path = path.replace("\\","/")
                path = path.replace(self.path_to, "")
                to_files.append(path+"/"+file)

        # compare lists
        set_from = set(from_files)
        set_to = set(to_files)
        newfiles = set_from.difference(set_to)
        
        # transfer only new files
        self.sc.print("Transfering new files...")
        for file in newfiles:
            index += 1
            log += "["+str(index)+"] "+file+"\n"
            oldfilename = self.path_from+file
            newfilename = self.path_to+file
            newdirectory = file.split("/")
            newdirectory =  '/'.join(newdirectory[:-1])
            newdirectory = self.path_to+newdirectory
            if not os.path.isdir(newdirectory):
                os.makedirs(newdirectory)
            if not os.path.isfile(newfilename):
                shutil.copy(oldfilename, newfilename)
                self.sc.print("["+str(index)+"] "+file)

        # save log
        end = self.sc.today()+" "+self.sc.right_now()
        log += "-----------------------------------------------\n"
        log += "Done: "+end
        file = open(self.logs+"/"+logname, 'w')
        file.write(log)
        file.close()
        os.system('"'+self.logs+'\\'+logname+'"')

        # restart
        self.sc.restart()
    
    def filtered_run(self):
        # call filter
        filter_index = self.sc.selected_main_menu_item()-1
        filter = list_of_plugins[filter_index][1]()

        # transfer file according to filter
        index = 0
        log = ""
        logname = self.sc.current_year()+self.sc.current_month()+self.sc.current_day()+self.sc.current_hour()+self.sc.current_minute()+self.sc.current_second()+".txt"
        start = self.sc.today()+" "+self.sc.right_now()
        log += "-----------------------------------------------\n"
        log += "Fast File Transfer"+" v"+self.sv+"\n"
        log += "Date and time: "+start+"\n"
        log += "From: "+self.path_from+"\n"
        log += "To: "+self.path_to+"\n"
        log += "Plugin: "+filter.plugin_name+"\n"
        log += "-----------------------------------------------\n"
        
        # create file history to avoid double testing files
        self.sc.print("Searching for new files...")
        filehistoylog = open("history.txt", "a")
        filehistoylog.close()
        filehistoylog = open("history.txt", "r")
        history = filehistoylog.readlines()
        filehistoylog.close()
        testfiles = []
        for path, dirnames, filenames in os.walk(self.path_from):
            for file in filenames:
                path = path.replace("\\","/")
                filename = path+"/"+file+"\n"
                if not filename in history:
                    history.append(filename)
                    testfiles.append((path,file))
        filehistoylog = open("history.txt", "w")
        for h in history:
            filehistoylog.write(h)
        filehistoylog.close()
    
        # go over files
        if len(testfiles) > 0:
            for data in testfiles:
                path = data[0]
                file = data[1]
                index += 1
                left = None
                right = None
                color = 'white'
                old_filename = path+"/"+file
                filter_result = filter.determine(path, file)
                filtered_path = self.path_to+"/"+filter_result[0]
                filtered_filename = filter_result[1]
                new_filename = filtered_path+"/"+filtered_filename
                if not os.path.isdir(filtered_path):
                    os.makedirs(filtered_path)
                
                if not os.path.isfile(new_filename):
                    shutil.copy(old_filename, new_filename)
                    left = old_filename
                    right = new_filename
                    color = 'green'
                else:
                    left = old_filename
                    right = "Already Exists"
                    color = 'cyan'
                
                txt = "["+str(index)+"] "+left.replace(path+"/","")+" | "+right.replace(self.path_to+"/","")
                self.sc.print(txt, color)
                log += txt+"\n"
        else:
            self.sc.good("No new files to transfer")
        # save log
        end = self.sc.today()+" "+self.sc.right_now()
        log += "-----------------------------------------------\n"
        log += "Done: "+end
        file = open(self.logs+"/"+logname, 'w')
        file.write(log)
        file.close()
        os.system('"'+self.logs+'\\'+logname+'"')

        # restart
        self.sc.restart()

main()