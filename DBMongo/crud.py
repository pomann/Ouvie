############################
# Made by: Roman Prochazka #
# Student number: 15711579 #
# Date: 28/01/2020         #
############################

from conn import OuvieDB

class Crud:

    def __init__(self):
        self.dtb = OuvieDB()

    # Inserts user into database
    def insert_user(self, name, user, email, pswd, opt_in):
        email_check = self.retrieve_email(email)
        user_check = self.retrieve_username(user)

        if (email_check == 'Failure' and user_check == 'Failure'):
            result = self.dtb.details.insert_one({
                'name' : name,
                'user' : user,
                'email' : email,
                'password' : pswd,
                'opt_in' : opt_in,
            })
        return result

    # Updates entry in database
    def update_user(self):
        return None

    # Checks if username is present in database
    def retrieve_username(self, user):
        result = self.dtb.details.find_one({"user": user})

        if (result):
            return 'Success'
        else:
            return 'Failure'

    # Checks if email is present in database
    def retrieve_email(self, email):
        result = self.dtb.details.find_one({"email": email})

        if (result):
            return 'Success'
        else:
            return 'Failure'

    # Retrieves user's full name 
    def retrieve_full_name(self, user):
        result = self.dtb.details.find_one({"user": user})

        if (result):
            return result['name']
        else:
            return None

    # Retrieves user's projects
    def retrieve_projects(self, user):
        try:
            return [i['name'] for i in self.dtb.db_files[user].find()]
        except:
            return None
            
    # Retrieves stream of commits needed to rebuild a project
    def retrive_project_commits(self, user, pid, chash, branch):
        commits = []
        if (chash != ''):
            is_snapshot = False
            while(not is_snapshot):
                result = self.dtb.db_files[pid].find_one({'chash' : chash})
                commits.append(chash)
                chash = result['phash']
                snapshot = result['snap']
                if snapshot.upper() == 'TRUE':
                    is_snapshot = True
        else:
            commits_on_branch = {i['phash'] : i['chash'] for i in self.dtb.db_files[pid].find({'branch' : branch})}
            for i in commits_on_branch:
                if commits_on_branch[i] not in commits_on_branch.keys():
                    return [commits_on_branch[i]]
            
        return list(reversed(commits))

    # Retrieve PID given USER and PNAME
    def retrieve_pid_from_pname(self, user, pname):
        return self.dtb.db_files[user].find_one({'name' : pname})['pid']

    # Retrieve PNAME given PID and USER
    def retrieve_pname_from_pid(self, user, pid):
        return self.dtb.db_files[user].find_one({'pid' : pid})['pname']

    # Retrieve commit count USER and PNAME, if branch provided retrieves Number of commits on a given branch
    # If branch is provided returns list of ids else list containing one number
    def retrieve_commit_count(self, user, pname, branch):
        try:
            pid = self.dtb.db_files[user].find_one({'name' : pname})['pid']
            opt = None
            latest_commit = None

            if branch:
                opt = {"branch" : branch}
                latest_commit = self.retrive_project_commits(user, pid, '', branch)[0]
            count = []

            if (latest_commit):
                commits_on_branch = {i['phash'] : i['chash'] for i in self.dtb.db_files[pid].find({'branch' : branch})}

                for i in range(len(commits_on_branch)):
                    count.append(latest_commit)
                    for key in commits_on_branch.keys():
                        if commits_on_branch[key] == latest_commit:
                            latest_commit = key

                return list(reversed(count))
            else:
                for i in self.dtb.db_files[pid].find(opt):
                    count.append(i)
            return [len(count)]

        except:
            return None
    
    # Retrieves branch names [string]
    def retrieve_branch_count(self, pname, user):
        try:
            pid = self.dtb.db_files[user].find_one({'name' : pname})['pid']
            branches = []
            for i in self.dtb.db_files[pid].find():
                if i['branch']:
                    if i['branch'] not in branches:
                        branches.append(i['branch'])
            return branches 
        except:
            return ['master']

    # Retrieves files for a certan commit, if commit hash not provided retrieves files for the latest commit on a given branch
    def retrieve_commit_files(self, pname, user, branch = None, chash = None):
        try:
            if (chash == None):
                pid = self.dtb.db_files[user].find_one({'name' : pname})['pid']
                if (pid):
                    commits_on_branch = {i['phash'] : i['chash'] for i in self.dtb.db_files[pid].find({'branch' : branch})}

                    for i in commits_on_branch:
                        if commits_on_branch[i] not in commits_on_branch.keys():
                            return [p['files'] for p in self.dtb.db_files[commits_on_branch[i]].find()]
            elif (branch == None):
                print('yas')
                return [p['files'] for p in self.dtb.db_files[chash].find()]
                
            return None
        except:
            return None


    # Authenticates user during login
    def auth_user(self, user, psswd):
        return self.dtb.details.find_one({'user' : user, 'password' : psswd})

    # Adds user's project to database
    def add_project(self, name, pid, user):
        user_check = self.retrieve_username(user)
        if (user_check == 'Success'):
            # Inserts entry into project database
            result = self.dtb.db_files[user].insert_one({
                'name' : name,
                'pid' : pid
            })
        return result

    # Adds user's commit to database
    def add_project_commit(self, pid, chash, phash, snap, branch, cfiles, user):
        user_check = self.retrieve_username(user)

        if (user_check == 'Success'):
            # Inserts entry into project database
            result = self.dtb.db_files[pid].insert_one({
                'chash' : chash,
                'phash' : phash,
                'snap' : snap,
                'branch' : branch
            })

            if result:
                files_added = self.add_files_to_commit(chash, cfiles)
                if files_added:
                    return files_added

        return None


    def add_files_to_commit(self, chash, cfiles):

        # Inserts entry into project database
        result = self.dtb.db_files[chash].insert_one({
            'files' : cfiles
        })

        return result
