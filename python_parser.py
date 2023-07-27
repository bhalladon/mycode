import csv, os, re, time


def pythonparser():
    print "starting python parser"
    result_file = "result.csv"
    fields = ["test_name", "result", "comment"]

    with open(result_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

    fp = os.path.join(os.getcwd(), "results")
    f = []
    for (_,_,filenames) in os.walk(fp):
        f.extend(filenames)
    for i in f:
        fp1 = os.path.join(fp, i)
        file1 = open(fp1, 'r')
        lines = file1.readlines()
        row = []
        for line in lines:
            if line.startswith("test"):
                classname = line.replace("test.ba.", "").replace(":","")
                row.append(classname)
                csv
            elif line.startswith("	PASS") or line.startswith("FAIL"):
                result = line.split(":")
                row.append(result[0])
                row.append(result[1])
                print row
                csvwriteinfile()
                csvwriter.writerow(row)
                time.sleep(60)
            else:
                pass





pythonparser()