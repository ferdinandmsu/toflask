import sys
import os
from bs4 import BeautifulSoup as bs
import shutil

class ToFlask:

    def __init__(self, outputPath, projectFolder, serverfilename):
        self.projectfolder = os.path.abspath(ToFlask.strippath(outputPath))
        self.path = os.path.abspath(ToFlask.strippath(projectFolder))
        self.serverfilename = serverfilename
        self.startpy = '''from flask import Flask, render_template

app = Flask(__name__)



if __name__ == "__main__":
    app.run()

'''

    def makeStructure(self):
        # make project folder
        if not os.path.exists(self.projectfolder):
            os.mkdir(self.projectfolder)
        os.chdir(self.projectfolder)
        # make static and templates folders
        if not os.path.exists("static"):
            os.mkdir("static")
        if not os.path.exists("templates"):
            os.mkdir("templates")
        # make server file
        with open(self.serverfilename, "w") as server:
            server.write(self.startpy)


    def parseHtml(self):
        # main path
        tmp = ToFlask.strippath(os.path.abspath(self.projectfolder + "/templates/"))
        # parse all html files in templates
        for htmlfile in os.listdir(tmp):

            with open(os.path.abspath(tmp + "/" + htmlfile), "r") as file:
                html = file.read()

            # soup
            soup = bs(html, 'html.parser')
            links = soup.find_all('link')
            images = soup.find_all('img')
            scripts = soup.find_all('script')

            # look for links
            for link in links:
                try:
                    if "http" in link.attrs["href"]:
                        continue
                    link.attrs["href"] = "static/" + link.attrs["href"]
                except IndexError:
                    continue
            # look for images
            for image in images:
                try:
                    if "http" in image.attrs["src"]:
                        continue
                    image.attrs["src"] = "static/" + image.attrs["src"]
                except IndexError:
                    continue
            # look for scripts
            for script in scripts:
                try:
                    if "http" in script.attrs["src"]:
                        continue
                    script.attrs["src"] = "static/" + script.attrs["src"]
                except IndexError:
                    continue
            # wirte html
            with open(os.path.abspath(tmp + "/" + htmlfile), "w") as file:
                file.write(soup.prettify())
            


    def copyFiles(self):
        for filename in os.listdir(self.path):
            # check if is html file
            if ".html" in filename or ".php" in filename:
                # copy in templates
                with open(os.path.abspath(self.path + "/" + filename), "r") as file:
                    content = file.read()

                with open(os.path.abspath(self.projectfolder + "/templates/" + filename), "w") as wfile:
                    wfile.write(content)
            # copy folders
            elif not "." in filename:
                shutil.copytree(os.path.abspath(self.path + "/" + filename), os.path.abspath(self.projectfolder + "/static/" + filename))


    @staticmethod
    def strippath(path):

        if path[-1] == "\\":
            path = path.strip("\\")
        elif path[-1] == "/":
            path = path.strip("/")

        return path

    def run(self):
        self.makeStructure()
        self.copyFiles()
        self.parseHtml()


            



