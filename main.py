import re, requests, os


class Page:
    def __init__(self):
        self.url = "https://www.heidoc.net/joomla/technology-science/microsoft/67-microsoft-windows-and-office-iso-download-tool"
        self.download_url = "https://www.heidoc.net/php/Windows-ISO-Downloader.exe"
        self.page = None
        self.request_content = None
        self.request = None
        self.file = None
        self.file_name = "Windows-ISO-Downloader.exe"

    def download_program(self):
        """
        Downloads actual program executable
        """
        self.request = requests.get(self.download_url)
        self.request_content = self.request.content
        self.file = open(self.file_name, mode="wb")
        self.file.write(self.request_content)
        self.file.close()

    def get_page(self):
        """
        From self.url get page contents and stores them as self.page variable
        """
        self.request = requests.get(self.url)
        self.page = self.request.text


class Version:

    def __init__(self):
        self.expression = None
        self.version = ""
        self.file = open("version.txt", "r+")
        self.re_check_code = None
        self.match = None

    def get_from_page(self):
        """
        From page contents in Page.page using regular expressions gets the version of the program as string
        because when compared as string with same string it returned false
        :return: Version of the program on the page as string
        """
        page.get_page()
        self.re_check_code = re.compile("\d\.\d\d")  # checks for number followed by dot and two numbers
        self.match = self.re_check_code.search(page.page)
        if self.match is None:  # if previous check didn't work, it will be tried with two digit version number
            self.re_check_code = re.compile("\d\d\.\d\d")   # if program version will get to two digit number
            self.match = self.re_check_code.search(page.page)
        self.version = self.match.group()
        return self.version

    def get_from_file(self):
        """
        From file named version.txt in the same directory returns version as string
        because string returns false when compared with same string
        :return: local program version as string
        """
        self.version = self.file.read()
        return self.version

    def update_file(self):
        """
        Updates file when called
        Writes new version string to file and removes the old one
        gets version from the page using version.get_from_page()
        :return:
        """
        self.file.truncate(0)
        self.file.write(str(self.get_from_page()))
        self.file.close()


if __name__ == "__main__":
    page = Page()
    version = Version()
    print("Windows-ISO-Downloader updater")
    print("Checking for updates...")
    local_version = version.get_from_file()
    # local_version = "8.02"   # there is error with the local version because it works when do I override it like this
    remote_version = version.get_from_page()
    # remote_version = "8.02"
    print(f"Version on the web: {remote_version}")
    print(f"Local version: {local_version}")
    if remote_version == local_version: # THIS THINK DOESN'T WORK!!! EVEN WITH SAME STRINGS!
        print(f"Program is up to date. Launching {page.file_name}...")
        os.system(page.file_name)
        exit()
    else:
        print("Program isn't up to date. Updating...")
        # page.download_program()
        version.update_file()
        print(f"Update completed. Launching {page.file_name}...")
        # os.system(page.file_name)
        exit()
