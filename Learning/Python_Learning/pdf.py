import urllib2

def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("document.pdf", 'w')
    file.write(response.read())
    file.close()
    print("Completed")
