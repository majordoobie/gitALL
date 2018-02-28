import requests
import sys
import re
import os
url_base = "https://api.github.com/users/"
url_suff = "/repos"


def clone_repos(repo_urls,output_dir):
    print("Cloning {} repositories.".format(len(repo_urls)))
    for url in repo_urls:
        print("cloaning {}".format(url))
        name = url.split('/')[-1]
        os.system("git clone {} {}".format(url, output_dir+"\\"+name))
    print('done')

def get_repos(url,user_url):
    repo_list = requests.get(url)
    if repo_list.status_code != 200:
        print("You user that's the right user?")
        sys.exit()
    else:
        print("Query success, starting to parse out the urls.")
        search_term = user_url+"/[a-zA-Z0-9\-_!@#$%^&*()]+"
        search = re.compile(search_term)
        repos = search.findall(repo_list.text)
        unique_repo = []
        for address in repos:
            if address not in unique_repo:
                unique_repo.append(address)
        return(unique_repo)


if __name__ == '__main__':
    user_url = sys.argv[1]
    user = user_url.split('/')[-1]
    print("Is {} the correct user name for this account?".format(user))
    answer = input(" [Y/n] --> ")
    if answer in ["Y","n"]:
        if answer == "n":
            user = input("Enter users name")
            user_user = "https://github.com/"+user
        
    output_dir = sys.argv[2]
    if os.path.isdir(output_dir) == False:
        print("Dir doesn't exist.")
        sys.exit()

    API_url = url_base+user+url_suff
    repo_urls = get_repos(API_url,user_url)
    clone_repos(repo_urls,output_dir)