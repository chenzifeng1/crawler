import urllib.request


def getOpenerf(header=''):
    headers = {
        "Accept": "text/html,Applicat/xhtml+xml,Application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Fiddler/5.0.20181.14850 (.NET 4.6.2; WinNT 10.0.17134.0; zh-CN; 4xAMD64; Auto Update; Full Instance; Extensions: APITesting, AutoSaveExt, EventLog, FiddlerOrchestraAddon, HostsFile, RulesTab2, SAZClipboardFactory, SimpleFilter, Timeline)",
        "Connection": "keep-alive",
        "referer": "http://www.163.com/"
    }
    headll = []
    for key, value in headers.items():
        item = (key, value)
        headll.append(item)

    opener = urllib.request.build_opener()
    opener.addheaders = headll
    return opener
