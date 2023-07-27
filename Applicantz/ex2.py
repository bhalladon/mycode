import os
import re

os.environ['SourcePath'] = "c:\dir1"
os.environ['BuildNum'] = "11"


def check_filepath_enviorvar(enviornment_variable, filename):
    try:
        os.environ[enviornment_variable]
        # if "environment variable" exists then we need to check file exists or not
        fp = os.path.join(os.environ[enviornment_variable], "develop", "global", "src", str(filename))
        if os.path.exists(fp):
            pass
        else:
            print("file " + str(filename) + " does not exist.")
            exit()
    except KeyError:
        print("Please define a enviornment variable with name " + str(enviornment_variable))
        exit()


check_filepath_enviorvar("SourcePath", "SConstruct")
check_filepath_enviorvar("SourcePath", "VERSION")


# os.environ['SourcePath'] = "c:\dir1"
# os.environ['BuildNum'] = "7"


def updateSconstruct():
    os.chmod(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct"), 0o0755)
    fin = open(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct1"), 'w')

    for line in fin:
        pattern = re.sub("point\=[\d]+", "point="+os.environ["BuildNum"], line)
        fout.write(pattern)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct"))
    os.rename(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct1"),
              os.path.join(os.environ["SourcePath"], "develop", "global", "src", "SConstruct"))

# # VERSION file interesting line
# ADLMSDK_VERSION_POINT=6
def updateVersion():
    os.chmod(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION"), 0o0755)
    fin = open(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION"), 'r')
    fout = open(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION1"), 'w')

    for line in fin:
        pattern=re.sub("ADLMSDK_VERSION_POINT\=[\d]+","ADLMSDK_VERSION_POINT="+os.environ["BuildNum"],line)
        fout.write(pattern)
    fin.close()
    fout.close()
    os.remove(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION"))
    os.rename(os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION1"),
              os.path.join(os.environ["SourcePath"], "develop", "global", "src", "VERSION"))


def main():
            updateSconstruct()
            updateVersion()


main()
