import sys, os, shutil, glob
from pathlib importPath

apps = ["openssl", "cpython", "memcached", "redis", "httpd", "httpd1", "httpd2"]
#apps = ['httpd1']

root = str(Path.home())+'/tmp/'

def trim_log(log_path):
    all_commit = 0
    year_valid_commit = 0
    write_line = False
    buf = ''
    trimed_log = open(log_path+'.valid_year', 'w')
    commit_set = []
    current_commit = ''
    newlyAdded = False
    with open(log_path, 'r') as f:
        for line in f:
            if line.startswith('commit '):
                write_line = False
                buf = line
                current_commit = line.strip().split()[1]
                if current_commit not in commit_set:
                    all_commit += 1
                    newlyAdded = True
                    commit_set.append(current_commit)
                else:
                    newlyAdded = False
            if line.startswith('Date: ') and buf != '':
                year = int(line.strip().split()[5])
                if year >= 2021 and year <= 2022:
                    write_line = True
                    if newlyAdded:
                        year_valid_commit += 1
                        trimed_log.write('**new** ')
                    trimed_log.write(buf)
                    buf = ''
            if write_line:
                trimed_log.write(line)
    return all_commit, year_valid_commit
def read_api_list(app):
    #loc_dict = {}
    os.chdir(root+app)
    log_path = app+'.api_related.log'
    if os.path.exists(log_path):
        os.remove(log_path)
    with open(app+'.list', 'r') as f:
        for line in f:
            line = line.strip().split()
            #loc_dict[line[2]] = line[0]
            func = line[2]
            func_path = line[0]
            os.system('git log -L :'+func+':'+func_path+' >> '+log_path)
    os.system('cat '+log_path+' > '+log_path+'1')
    os.system('mv '+log_path+'1 '+log_path)
    return trim_log(log_path)
    #return loc_dict

for app in apps:
    all_commit, year_valid_commit = read_api_list(app)
    print(app, all_commit, year_valid_commit)
