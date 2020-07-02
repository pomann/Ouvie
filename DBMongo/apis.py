############################
# Made by: Roman Prochazka #
# Student number: 15711579 #
# Date: 28/01/2020         #
############################

import flask
import jwt
import datetime

from flask import request, jsonify
from functools import wraps

from crud import Crud
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "7d18c9ad36175d474d6c00cc0d4657a3523875a67e4160f4dda809ba97394a6bf4c712cb72b9b53c26d993a0aad3c9fea880b44542b96253bacce910b0410749"
CORS(app)

dbo = Crud()


responses = {
    'no_exception' : 'success',
    'exception_raised' : 'failure',
    'success' : 'OV1111',
    'else_raised' : 'OV0000',
    'wrong_arguments' : 'OV0011',
    'no_token' : 'OV0022',
    'wrong_token' : 'OV2200'
}

# Checks if valid token present in header
def req_totoken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['Authorization']
            t_data = jwt.decode(token, app.config['SECRET_KEY'])
            print(t_data['user'], request.args['user'])
            if t_data['user'] != request.args['user']:
                return jsonify({'status': responses['no_exception'], 'code' : responses['wrong_token'], 'data' : []})
        except:
            return jsonify({'status': responses['exception_raised'], 'code' : responses['no_token'], 'data' : []})
        
        return f(*args, **kwargs)
    
    return decorated

# Authenticates Login form
# Args: user, password
@app.route('/api/v1/auth/login', methods=['GET'])
def api_login():
    try:
        args = ['user', 'password']
        if (all([True if x in request.args else False for x in args])):
            user = request.args['user']
            pswd = request.args['password']

            user_check = dbo.retrieve_username(user)
            if (user_check == 'Success'):
                result = dbo.auth_user(user, pswd)
                if (result):
                    token = jwt.encode({'user' : user, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(1800)}, app.config['SECRET_KEY'])
                    return jsonify({'status': responses['no_exception'],
                                    'code' : responses['success'],
                                    'data' : [result['email'], token.decode('UTF-8')]})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Authenticates register forms
# Args: name, username, email, password, optin
@app.route('/api/v1/auth/register/verify', methods=['GET'])
def api_reg_verify():
    try:
        # Check if all arguments present
        args = ['name', 'user', 'email', 'pswd', 'optin']
        if (all([True if x in request.args else False for x in args])):
            # Gets all values
            name = request.args['name']
            user = request.args['user']
            email = request.args['email']
            pswd = request.args['pswd']
            opt_in = request.args['optin']

            # Check if username and email are unique
            user_check = dbo.retrieve_username(user)
            email_check = dbo.retrieve_email(email)

            if (user_check == 'Failure' and email_check == 'Failure'):
                result = dbo.insert_user(name, user, email, pswd, opt_in)
                project_result = dbo.add_project(user, 123, user)
                if (result and project_result):
                    return jsonify({'status': responses['no_exception'], 'code' : responses['success'], 'data' : []})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Checks username availability
# Args: username
@app.route('/api/v1/auth/register/user', methods=['GET'])
def api_reg_user():
    try:
        if ('user' in request.args):
            user = request.args['user']
            result = dbo.retrieve_username(user)
            if (result == 'Failure'):
                return jsonify({'status': responses['no_exception'], 'code' : responses['success'], 'data' : []})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Checks email availability
# Args: Email
@app.route('/api/v1/auth/register/email', methods=['GET'])
def api_reg_email():
    try:
        if ('email' in request.args):
            email = request.args['email']
            result = dbo.retrieve_email(email)

            if (result == 'Failure'):
                return jsonify({'status': responses['no_exception'], 'code' : responses['success'], 'data' : []})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves full name from database
# Args username
@app.route('/api/v1/retrieve/user/details', methods=['GET'])
@req_totoken
def api_retrieve_user_details():
    print(request.data)
    try:
        if ('user' in request.args):
            user = request.args['user']
            result = dbo.retrieve_username(user)
            if (result == 'Success'):
                fullDetails = dbo.retrieve_full_name(user)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : fullDetails})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})


# Retrieves user's project from database
# Args: user
# Returns [String]
@app.route('/api/v1/retrieve/project', methods=['GET'])
@req_totoken
def api_retrieve_project():
    try:
        if ('user' in request.args):
            user = request.args['user']
            result = dbo.retrieve_username(user)
            if (result == 'Success'):
                projects = dbo.retrieve_projects(user)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : projects})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves project's pid given pname
# Args: username, pname
@app.route('/api/v1/retrieve/pid', methods=['GET'])
@req_totoken
def api_retrieve_pid_from_pname():
    try:
        if ('user' in request.args and 'pname' in request.args):
            user = request.args['user']
            pname = request.args['pname']

            result = dbo.retrieve_username(user)

            if (result == 'Success'):
                pid = dbo.retrieve_pid_from_pname(user, pname)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : [pid]})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves project's pname given pid
# Args: username, pname
@app.route('/api/v1/retrieve/pname', methods=['GET'])
@req_totoken
def api_retrieve_pname_from_pid():
    try:
        if ('user' in request.args and 'pid' in request.args):
            user = request.args['user']
            pid = request.args['pid']

            result = dbo.retrieve_username(user)

            if (result == 'Success'):
                pname = dbo.retrieve_pname_from_pid(user, pid)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : [pname]})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves stream of commits for a given project
# Args: user, pid, chash, branch
@app.route('/api/v1/retrieve/commits', methods=['GET'])
def api_retrieve_commit():
    try:
        if ('user' in request.args and 'pid' in request.args):
            user = request.args['user']
            pid = request.args['pid']
            chash = ""
            branch = "master"
            try:
                chash = request.args['chash']
            except:
                pass
            try:
                branch = request.args['branch']
            except:
                pass

            result = dbo.retrieve_username(user)
            if (result == 'Success'):
                commits = dbo.retrive_project_commits(user, pid, chash, branch)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : commits})

        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves files project files in a given project using chash or branch
# Args: user, pname, branch or chash
# Use branch to retrieve latest files on a branch
# Use chash to retrieve files from that chash
@app.route('/api/v1/retrieve/commit/files', methods=['GET'])
@req_totoken
def api_retrieve_commit_files():
    try:
        if ('user' in request.args and 'pname' in request.args and ('chash' in request.args or 'branch' in request.args) ):
            user = request.args['user']
            pname = request.args['pname']
            branch = None
            chash = None

            try:
                branch = request.args['branch']
            except:
                pass
            
            try:
                chash = request.args['chash']
            except:
                pass

            if (chash and branch):
                return jsonify({'status': responses['no_exception'], 'code' : responses['wrong_arguments'], 'data' : []})

            result = dbo.retrieve_username(user)
            if (result == 'Success'):
                if (branch):
                    commitFiles = dbo.retrieve_commit_files(pname, user, branch, None)
                    print(commitFiles, "CFB")
                else:
                    commitFiles = dbo.retrieve_commit_files(pname, user, None, chash)
                    print(commitFiles, "CFC")
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : commitFiles})


        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves number of commits on a branch, if branch not specified, retrieves all commits in a project
# Args: user, pname, optional(branch)
@app.route('/api/v1/retrieve/commit/count', methods=['GET'])
@req_totoken
def api_retrieve_commit_count():
    try:
        if ('user' in request.args and 'pname' in request.args):
            user = request.args['user']
            pname = request.args['pname']
            branch = ""

            try:
                branch = request.args['branch']
            except:
                pass

            result = dbo.retrieve_username(user)

            if (result == 'Success'):
                print(branch)
                commitCount = dbo.retrieve_commit_count(user, pname, branch)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : commitCount})


        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Retrieves branch names
# Args: user, pname
@app.route('/api/v1/retrieve/branch/count', methods=['GET'])
@req_totoken
def api_retrieve_branch_count():
    try:
        if ('user' in request.args and 'pname' in request.args):
            user = request.args['user']
            pname = request.args['pname']
            result = dbo.retrieve_username(user)

            if (result == 'Success'):
                branchCount = dbo.retrieve_branch_count(user, pname)
                return jsonify({'status' : responses['no_exception'], 'code' : responses['success'], 'data' : branchCount})


        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Adds new user project to database
# Args user, name, pid
@app.route('/api/v1/add/project', methods=['GET'])
def api_create_project():
    try:
        if ('user' in request.args):
            # Retrieve request params
            user = request.args['user']
            name = request.args['name']
            pid = request.args['pid']

            result = dbo.retrieve_username(user)

            if (result == 'Success'):

                project_added = dbo.add_project(name, pid, user)

                if (project_added):
                    return jsonify({'status': responses['no_exception'], 'code' : responses['success'], 'data' : []})


        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

# Adds new commit
# Args: user, chash, phash, snap, pid, cfiles, optional(brach)
@app.route('/api/v1/add/commit', methods=['GET'])
def api_add_commit():
    try:
        if ('user' in request.args):
            user = request.args['user']
            chash = request.args['chash']
            phash = request.args['phash']
            snap = request.args['snap']
            pid = request.args['pid']
            cfiles = request.args['cfiles']
            branch = 'master'
            try:
                branch = request.args['branch']
            except:
                pass

            result = dbo.retrieve_username(user)

            if (result == 'Success'):
                commit_added = dbo.add_project_commit(pid, chash, phash, snap, branch, cfiles, user)

                if (commit_added):
                    return jsonify({'status': responses['no_exception'], 'code' : responses['success'], 'data' : []})


        return jsonify({'status': responses['no_exception'], 'code' : responses['else_raised'], 'data' : []})
    except:
        return jsonify({'status': responses['exception_raised'], 'code' : responses['else_raised'], 'data' : []})

#Handles unknown api requests
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>ERROR: 404</h1><p>OOPS it wans't me <br> Go blame Jamie</p>", 404

app.run()
