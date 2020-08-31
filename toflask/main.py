import argparse

from ToFlask import ToFlask


def main():
    
    # argument parser
    parser = argparse.ArgumentParser(description="Tool for converting an HTML project in an Flask Project...")
    parser.add_argument("--output", type=str, help="Enter a your output project path. (str)", required=True)
    parser.add_argument("--project", type=str, help="Enter old Project path. (str)", required=True)
    parser.add_argument("--serverFile", type=str, help="Enter the name of the server file cannot be Flask.py. (str)", required=False, default="server.py")
    args = parser.parse_args()
    
    # start class
    outpath = args.output
    projectpath = args.project
    servername = args.serverFile

    toflask = ToFlask(outpath, projectpath, servername)
    toflask.run()

if __name__ == "__main__":
    main()