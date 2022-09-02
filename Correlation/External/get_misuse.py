import sys, os

app = sys.argv[1]
app_list = {"httpd": ["httpd1", "httpd2", "httpd"],
        "openssl": ["openssl"],
        "cpython": ["cpython"],
        "redis": ["redis"],
        "memcached": ["memcached"]}
year_list = ["2017", "2018", "2019", "2020", "2021"]

error_list = ["memory leak", "double free", "use after free"]

def get_api(flist):
    api_list = []
    with open(flist, 'r') as f:
        for line in f:
            api_list.append(line.strip())
    return api_list
    

def check_related(line, funclist):
    for func in funclist:
        if func in line:
            return True, func
    return False, ''

def write_trimed_log(fname, commit_list):
    with open(fname, 'r', encoding = "ISO-8859-1") as f:
        outlog = open(fname+'.noAPIError', 'w')
        log = False
        for line in f:
            if line.startswith('commit '):
                if line.strip().split()[-1] in commit_list:
                    log = True
                else:
                    log = False
            if log:
                outlog.write(line)

def count_commit(gitlog, funclist, error_list):
    flog = open(gitlog, 'r', encoding = "ISO-8859-1")
    #output = open(gitlog+'.trimed', 'w')
    total, APIerror = 0, 0
    detectError = False
    detectAPI = False
    search = True
    commit = ''
    error = ''
    API = ''
    all_commit = []
    api_error_commit = []
    error_count = 0
    error_commit = []
    while True:
        line = flog.readline()
        if line == "":
            break;
        if line.startswith("commit ") and len(line.strip().split()):
            commit = line
            detectError = False
            detectAPI = False
        if line.startswith("Date: "):
            if line.strip().split()[5] not in year_list:
                continue
            total += 1
            all_commit.append(commit.strip().split()[-1])
            while not detectError:
                if "diff --git" in line:
                    break
                if "commit " in line:
                    break
                detectError, Error = check_related(line, error_list)
                line = flog.readline()
            if detectError:
                error_count += 1
                search = True
                error_commit.append(commit.strip().split()[-1])
        if search and not detectAPI: 
                detectAPI, API = check_related(line, func_list)
        if search and detectError and detectAPI:
            search = False
            #output.write(commit.strip() + ' ' + error + ' ' + API + '\n')
            API = ''
            error = ''
            APIerror += 1
            api_error_commit.append(commit.strip().split()[-1])

    write_trimed_log(gitlog, [item for item in error_commit if item not in api_error_commit])
            
    return total, error_count

keywords_list = ["new", "alloc", "create","make","from","resize", "realloc", "dealloc", "free", "release", "del", "clear"]


if app in app_list.keys():
    func_list = get_api(app+".list")
    total_commit = 0
    related_commit = 0
    
    for fname in app_list[app]:
        total, related = count_commit(fname + ".gitlog", func_list, error_list)
        total_commit += total
        related_commit += related
    print(app, '-- total:', total, 'related:', related)
else:
    print(app, "not found!")
