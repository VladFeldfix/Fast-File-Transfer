from SmartConsole import *
import shutil

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Fast File Transfer", "1.0")
        
        # set-up main memu
        self.sc.add_main_menu_item("RUN", self.run)

        # get settings
        self.path_from = self.sc.get_setting("From")
        self.path_to = self.sc.get_setting("To")

        # test all paths
        self.sc.test_path(self.path_from)
        self.sc.test_path(self.path_to)

        # display main menu
        self.sc.start()
    
    def run(self):
        self.sc.print("Uploading files...")
        for path, dirnames, filenames in os.walk(self.path_from):
            for file in filenames:
                oldfilename = path+"/"+file
                newfilename = self.path_to+oldfilename.replace(self.path_from, "")
                newdirectory = newfilename.replace(file ,"")
                if not os.path.isdir(newdirectory):
                    os.makedirs(newdirectory)
                if not os.path.exists(newfilename):
                    self.sc.print(newfilename)
                    shutil.copy(oldfilename, newfilename)
        # restart
        self.sc.restart()

main()