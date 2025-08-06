import os
import pdfplumber

class filter:
    def __init__(self):
        self.plugin_name = "MPT_LOT_files_and_programs v1.0"

    def determine(self, path, file):
        # setup results
        filtered_path = ""
        filtered_filename = file

        # MPT5000 Instrument Verification
        if "Instrument Verification" in file:
            filtered_path = "auto-save"
            return (filtered_path, filtered_filename)
        
        # MPT5000 Software Validation
        if "MPT5000-Validation" in file:
            filtered_path = file.split("MPT5000-Validation")
            filtered_path = filtered_path[0]
            filtered_path = filtered_path.strip()+"/Test Program/MPT5000"
            return (filtered_path, filtered_filename)

        # MPT5000L Software Validation
        if "MPT5000L-Validation" in file:
            filtered_path = file.split("MPT5000L-Validation")
            filtered_path = filtered_path[0]
            filtered_path = filtered_path.strip()+"/Test Program/MPT5000L"
            return (filtered_path, filtered_filename)
        
        # MPT5000 Software
        if ".mpt_product" in file:
            filtered_path = file.split("_")
            filtered_path = filtered_path[0].split(".")
            filtered_path = filtered_path[0]
            filtered_path = filtered_path.strip()+"/Test Program/MPT5000"
            return (filtered_path, filtered_filename)

        # MPT5000L .csv
        if ".csv" in file:
            filtered_path = file.split("_")
            if len(filtered_path) == 1:
                filtered_path = filtered_path[0].split(".csv")
                filtered_path = filtered_path[0]
                filtered_path = filtered_path.strip()+"/Test Program/MPT5000L"
                return (filtered_path, filtered_filename)
        
        # MPT5000L .txt
        if ".txt" in file:
            filtered_path = file.split("_")
            if len(filtered_path) == 1:
                filtered_path = filtered_path[0].split(".txt")
                filtered_path = filtered_path[0]
                filtered_path = filtered_path.strip()+"/Test Program/MPT5000L"
                return (filtered_path, filtered_filename)

        # MPT5000L .cal
        if ".cal" in file:
            filtered_path = file.split("_")
            if len(filtered_path) == 1:
                filtered_path = filtered_path[0].split(".cal")
                filtered_path = filtered_path[0]
                filtered_path = filtered_path.strip()+"/Test Program/MPT5000L"
                return (filtered_path, filtered_filename)
            
        # Passed test
        passed_test = filtered_filename
        passed_test = passed_test.split("_")
        if len(passed_test) == 3:
            datestamp = passed_test[1].strip()
            year = datestamp[5:].strip()
            part_numbner = passed_test[2].strip()
            part_numbner = part_numbner.split(".")
            part_numbner = part_numbner[0]
            filtered_path = part_numbner+"/Test Results/"+year
            return (filtered_path, filtered_filename)

        # Full report
        if "pass" in filtered_filename.lower() or "fail" in filtered_filename.lower() or "abort" in filtered_filename.lower():
            fulltest = filtered_filename
            if ".txt" in fulltest:
                fulltest = fulltest.split("_")
                if len(fulltest) == 5: # [index] partnumber_datestamp_serialnumber_operator_testresult.txt
                    # get part number
                    partnumber = fulltest[0] # [index] partnumber
                    partnumber = partnumber.split("]")
                    partnumber = partnumber[1].strip()
                    # get datestamp
                    datestamp = fulltest[1]
                    datestamp = datestamp.strip()
                    year = datestamp[5:]
                    filtered_path = partnumber+"/Full Report/"+year 
                    return (filtered_path, filtered_filename)
            elif ".pdf" in fulltest:
                try:
                    path_to_file = path+"/"+file
                    if os.path.isfile(path_to_file):
                        partnumber = None
                        year = None
                        serialnumber = None
                        operator = None
                        testresult = None
                        datestamp = None

                        # get data by reading pdf file
                        with pdfplumber.open(path_to_file) as pdf:
                            for page in pdf.pages:
                                txt = str(page.extract_text())
                                lines = txt.split("\n")
                                for line in lines:
                                    if "UUT Serial Number".lower() in line.lower():
                                        line = line.split(":")
                                        line = line[1]
                                        line = ''.join(char for char in line if char.isalnum() or char == '-')
                                        serialnumber = line
                                    elif "Product Name".lower() in line.lower():
                                        line = line.split(":")
                                        line = line[1]
                                        line = line.split("_")
                                        line = line[0]
                                        line = ''.join(char for char in line if char.isalnum())
                                        partnumber = line
                                    elif "Date and Time".lower() in line.lower():
                                        line = line.split(" ") # ['║', 'Date', 'and', 'Time:', 'Jul', '30', '2025', '05:40:39', '║']
                                                               # [ 0 ,  1    ,  2   ,  3     ,  4   ,  5  ,  6    ,  7        , 8]
                                        year = line[6]
                                        month = line[4]
                                        day = line[5]
                                        time = line[7]
                                        time = time.replace(":","")
                                        datestamp = day+month+year+"_"+time
                                    elif "Operator".lower() in line.lower():
                                        line = line.split(":")
                                        line = line[1]
                                        line = ''.join(char for char in line if char.isalnum())
                                        operator = line
                                    elif "Test Result".lower() in line.lower():
                                        line = line.split(":")
                                        line = line[1]
                                        line = ''.join(char for char in line if char.isalnum())
                                        testresult = line
                        # save log
                        if partnumber != None and year != None and serialnumber != None and operator != None and testresult != None and datestamp != None:
                            filtered_path = partnumber+"/Full Report/"+year
                            filtered_filename = partnumber+"_"+datestamp+"_"+serialnumber+"_"+operator+"_"+testresult+".pdf"
                            return (filtered_path, filtered_filename)
                except Exception as e:
                    pass
                
        # return empty result
        filtered_path = ""
        filtered_filename = file
        return (filtered_path, filtered_filename)