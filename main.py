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
        self.request = requests.get(self.download_url)
        self.request_content = self.request.content
        self.file = open(self.file_name, mode="wb")
        self.file.write(self.request_content)
        self.file.close()

    def get_page(self):
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
        page.get_page()
        self.re_check_code = re.compile("\d\.\d\d")
        self.match = self.re_check_code.search(page.page)
        if self.match is None:
            self.re_check_code = re.compile("\d\d\.\d\d")
            self.match = self.re_check_code.search(page.page)
        self.version = float(self.match.group())
        return self.version

    def get_from_file(self):
        try:
            self.version = float(self.file.read())
        except ValueError:
            self.version = 0.0
        return self.version

    def update_file(self):
        self.file.truncate(0)
        self.file.write(str(version.get_from_page()))
        self.file.close()


if __name__ == "__main__":
    page = Page()
    version = Version()
    print("Windows-ISO-Downloader updater")
    print("Checking for updates...")
    local_version = float(version.get_from_file())
    remote_version = float(version.get_from_page())
    print(f"Version on the web: {remote_version}")
    print(f"Local version: {local_version}")
    if remote_version == local_version:
        print(f"Program is up to date. Launching {page.file_name}...")
        os.system(page.file_name)
        exit()
    else:
        print("Program isn't up to date. Updating...")
        page.download_program()
        version.update_file()
        print(f"Update completed. Launching {page.file_name}...")
        os.system(page.file_name)
        exit()








