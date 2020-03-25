import gitinfo

def get_git_hash():
    info = gitinfo.get_git_info()
    return info["commit"], info["message"]
