from flask import Flask, session, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml
import random
import time

app = Flask(__name__)
app.secret_key = 'tatanamak'

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)



@app.route('/')
def root():

    session.pop('uid', None)
    session.pop('wid', None)
    session.pop('gid', None)
    return render_template('index.html')


# inserting data into 'USER' table while registering
@app.route('/register', methods=['POST'])
def userdetails():
    # fetching values from form
    name = request.form.get('Name')
    username = request.form.get('Email')
    password = request.form.get('Password')
    college = request.form.get('College')
    type = request.form.get('type')
    queryValues = [username, name, password, college, type]

    # inserting into database
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO `user` (`username`,`name`,`password`,`college`,`type`) VALUES (%s,%s,%s,%s,%s)",
        queryValues)
    cur.close()
    conn.commit()  #committing to the database
    return redirect('/')


# inserting data into register table while logging in
@app.route('/login', methods=['POST'])
def login():


    session.pop('uid', None)
    session.pop('wid', None)
    session.pop('gid', None)

    username = request.form.get('Email')
    password = request.form.get('Password')

    # getting user info from user table
    conn = mysql.connection
    cur = conn.cursor()
    values = cur.execute(
        "SELECT user.userid,user.type,user.username,user.name FROM user where user.username = %s AND user.password = %s",
        [username, password])
    if (values > 0):
        userDetails = cur.fetchall()
        userid = userDetails[0][0]
        type = userDetails[0][1]
        uname = userDetails[0][2]
        name = userDetails[0][3]

        #storing username and userid and grp id and workshop and type in session variable
        session['uid'] = userid

        # session['type'] = type
        session['gid']=-1
        session['name']= name
        session['wid']= "1" #hardcoding the workshop Id


        # storing the userid in the registration table
        queryValues = [1, userid]
        print(userid)

        # checking if the user is loggedin atleast once
        check_user = cur.execute("SELECT reg.userid FROM registration reg WHERE reg.userid = %s",(userid,))

        # If not inserting his data into registration table
        if(check_user == 0):
            cur.execute(
            "INSERT INTO `registration` (`workshopid`, `userid`) VALUES (%s , %s)",
            queryValues)
            cur.close()
            conn.commit()

        if (type == 'admin'):
            return redirect('/admin')
        elif (type == 'participant'):
            return redirect('/waiting')
    else:
        return render_template('404.html')

# logout
@app.route('/logout')
def logout():

    session.pop('uid', None)
    session.pop('wid', None)
    return redirect('/')


# functonalities of all admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get("uid"):
        return redirect("/")
    return render_template('admin.html')

@app.route('/admin/teams', methods=['GET', 'POST'])
def teams():
    if not session.get("uid"):
        return redirect("/")
    return render_template('teams.html')

@app.route('/admin/people', methods=['GET', 'POST'])
def people():
    if not session.get("uid"):
        return redirect("/")
    return render_template('participants.html')


# displaying participants list
@app.route('/admin/people/showparticipants', methods=['post'])
def showparticipants():


    if not session.get("uid"):
        return redirect("/")
    # connecting to database
    conn = mysql.connection
    cur = conn.cursor()
    participantNames = {}
    values = cur.execute(
        "SELECT user.name FROM user where user.type = 'participant' AND user.userid IN (SELECT reg.userid FROM registration reg)"
    )
    if (values > 0):
        userDetails = cur.fetchall()
        cur.close()
        conn.commit()

        # converting to json
        id = 0
        for user in userDetails:
            participantNames[id] = user[0]
            id = id + 1
    return jsonify(participantNames)


# start of creating teams functionality
def arrangeRandom(userIdstuple, count):

    # getting random numbers within a range
    randomNumbers = random.sample(range(len(userIdstuple)), len(userIdstuple))

    # getting ids from tuple of tuples
    userIds = []
    for id in userIdstuple:
        userIds.append(id[0])

    createdTeams = {}  #to store teams
    key = 0  #key for each team
    team = []  #list which stores each team members
    index = 0  #maintains index of 'randomNumbers'
    c = 0  #maintains count
    for id in range(len(userIds) + 1):
        if (index == len(userIds)):
            createdTeams[key] = team
            break
        if (c == count):
            createdTeams[key] = team
            key = key + 1
            c = 0
            team = []
        team.append(userIds[randomNumbers[index]])
        c = c + 1
        index = index + 1
    return createdTeams


@app.route('/admin/createTeams', methods=["POST"])
def createTeams():


    if not session.get("uid"):
        return redirect("/")
    # getting count of memebers in each team from form
    rsp = request.json
    count = int(rsp['count'])
    # connecting to database
    conn = mysql.connection
    cur = conn.cursor()
    query="DELETE FROM `group` WHERE 1;"
    cur.execute(query)
    conn.commit()
    values = cur.execute(
        "SELECT reg.userid FROM registration reg WHERE reg.userid IN (SELECT user.userid FROM user WHERE type = 'participant')"
    )
    if values > 0:

        userIds = cur.fetchall()
        createdTeams = arrangeRandom(userIds, count)
        for key in createdTeams.keys():
             for value in createdTeams[key]:
                 cur.execute("INSERT INTO `group` (`workshopid`,`groupid`, `userid`) VALUES (%s,%s, %s)",(1,key,value))
                 conn.commit()
        conn.commit()
        teams = {}
        for key in createdTeams.keys():
            teams[key] = []
            for value in createdTeams[key]:
                count = cur.execute(
                    "SELECT user.name FROM user WHERE user.userid = %s",
                    [value])
                if (count > 0):
                    name = cur.fetchall()
                    teams[key].append(name[0][0])

        return jsonify(teams)
# end of creating teams functionality


# functonalities of all participants

startTime = int(time.time())
phaseTime = 3600


@app.route("/updatePhase",methods=['GET'])
def updatephase():

    if not session.get("uid"):
        return redirect("/")

    phase = request.args.get('curphase')

    #will fetch this time from DB which contains end time
    global startTime

    currTime = int(time.time())
    if(phase == 'EMP'):

        print(startTime,phaseTime,currTime,)
        if(startTime+phaseTime < currTime ):
            return "true"
        else:
            return "false"

    if(phase == 'DEF'):

        print(startTime,phaseTime,currTime,)
        if(startTime+phaseTime*2 < currTime ):
            return "true"
        else:
            return "false"


    if(phase == 'IDE'):

        print(startTime,phaseTime,currTime,)
        if(startTime+phaseTime*3 < currTime ):
            return "true"
        else:
            return "false"

    if(phase == 'PRO'):

        print(startTime,phaseTime,currTime,)
        if(startTime+phaseTime*4 < currTime ):
            return "true"
        else:
            return "false"



#========================================================================
#========================Prototype Part===============================
#========================================================================


@app.route("/returnProto",methods=['GET'])
def returnProto():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    query="select * from protoTable;"
    cur.execute(query)
    results = cur.fetchall()

    payload = []
    content = {}
    for result in results:
        content = {'imgid': result[0], 'image': result[3]}
        payload.append(content)
        content = {}


    #print(payload);
    cur.close()
    return jsonify(payload)

@app.route("/addProto",methods=['GET'])
def addProto():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    app.logger.info(request.args.keys())
    wid = request.args.get('workid')
    gid = request.args.get('grpid')
    img = request.args.get('image')
    imgid = request.args.get('imgid')


    querycheck = "select * from protoTable where imgid="+imgid+";"
    val = cur.execute(querycheck)
    if(val>0):
        results = cur.fetchall()
        app.logger.info(str(results[0][0]))
        queryUpdate="update protoTable set image='"+img+"' where imgid = "+str(results[0][0])+";"
        cur.execute(queryUpdate)
        mysql.connection.commit()
    else:

        query="insert into protoTable(workshopid,grpid,image) values(%s,%s,%s);"

        record = [wid,gid,img]
        cur.execute(query, record)
        mysql.connection.commit()
    cur.close()
    return 'Proto Added Successfully'


#========================================================================
#========================Sticky Notes Part===============================
#========================================================================

@app.route("/deleteSticky",methods=['GET'])
def deleteSticky():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    uid = request.args.get('noteid')
    query="delete from wall where notesid="+uid+";"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return "true"

@app.route("/returnSticky",methods=['GET'])
def returnSticky():

    if not session.get("uid"):
        return redirect("/")


    wid = request.args.get('workid')
    userid = request.args.get('userid')
    grpid = request.args.get('grpid')

    cur = mysql.connection.cursor()
    query="select * from wall where workshopid="+wid+" and grpid= "+grpid+" and userid = "+userid+";"
    cur.execute(query)
    results = cur.fetchall()

    payload = []
    content = {}
    for result in results:
        content = {'notesid': result[3], 'textnote': result[4], 'userid': result[2]}
        payload.append(content)
        content = {}


    #print(payload);
    cur.close()
    return jsonify(payload)


@app.route("/returnStickyDefine",methods=['GET'])
def returnStickyDefine():

    if not session.get("uid"):
        return redirect("/")


    wid = request.args.get('workid')
    userid = request.args.get('userid')
    grpid = request.args.get('grpid')

    cur = mysql.connection.cursor()
    query="select * from wall where workshopid="+wid+" and grpid= "+grpid+";"
    cur.execute(query)
    results = cur.fetchall()

    payload = []
    content = {}
    for result in results:
        content = {'notesid': result[3], 'textnote': result[4], 'userid': result[2]}
        payload.append(content)
        content = {}


    #print(payload);
    cur.close()
    return jsonify(payload)

@app.route("/addSticky",methods=['GET'])
def addSticky():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    wid = request.args.get('workid')
    gid = request.args.get('grpid')
    uid = request.args.get('userid')
    msg = request.args.get('notes')


    query="insert into wall(workshopid,grpid,userid,notes) values(%s,%s,%s,%s);"

    record = [wid,gid,uid,msg]
    cur.execute(query, record)
    mysql.connection.commit()
    cur.close()
    return 'Added Successfully'




@app.route("/addMessage",methods=['GET'])
def addMessage():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    msg = request.args.get('msg')
    userid = request.args.get('userid')
    wid = request.args.get('wid')
    grpid = request.args.get('grpid')
    query="insert into chat(workshopid,groupid,userid,text) values(%s,%s,%s,%s)"

    record = [wid,grpid,userid,msg]
    cur.execute(query, record)
    mysql.connection.commit()
    cur.close()
    return 'Added Successfully'

@app.route("/getmsg")
def getmsg():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    
    userid = request.args.get('userid')
    
    wid = request.args.get('wid')
    gid = request.args.get('grpid')

    query1="select * from chat where workshopid ="+wid+" and groupid="+gid+" order by messageid;"
    cur.execute(query1)
    results = cur.fetchall()

    payload = []
    content = {}
    for result in results:
        content = {'uid': result[2], 'text': result[4]}
        payload.append(content)
        content = {}


    #print(payload);
    cur.close()
    return jsonify(payload)


@app.route("/waiting")
def waiting():

    if not session.get("uid"):
        return redirect("/")

    info={}
    info['wid']=session['wid']
    info['uid']=session['uid']
    info['gid']="1"
    info['name']=session['name']

    cur = mysql.connection.cursor()
    query1="select * from `group` where userid = "+str(info['uid'])+" ;"
    cur.execute(query1)
    results = cur.fetchall()
    gid = results[0][2]
    app.logger.warning(gid);
    session['gid']=gid

    if session.get("gid")!=-1:
        app.logger.warning("sessin gid not set");

    return render_template('waiting.html',data=info)

@app.route("/emphasize")
def participants():

    if not session.get("uid"):
        return redirect("/")

    global startTime
    startTime = int(time.time())

    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = session['wid']
    #gid = 1
    uid = session['uid']

    cur = mysql.connection.cursor()
    query1="select * from `group` where userid = "+str(uid)+" ;"
    cur.execute(query1)
    results = cur.fetchall()
    gid = results[0][2]

    session['gid']=gid



    #data={"workshopid":wid, "groupid": gid, "userid" : uid,"name":session['name'] }

    #return render_template('emphasize.html',user=data)


    if not session.get("uid"):
        return redirect("/")

    info={}
    info['wid']=session['wid']
    info['uid']=session['uid']
    info['gid']=gid
    info['name']=session['name']


    return render_template('emphasize.html',user=info)

@app.route("/isCreated", methods=["GET"])
def isCreated():

    if not session.get("uid"):
        return redirect("/")

    cur = mysql.connection.cursor()
    uid = request.args.get('userid')

    empty="SELECT * FROM `group`;"
    numRow = cur.execute(empty)
    if(numRow==0):
        return "false"
    else:
        getGrp = "SELECT userid FROM `group` WHERE groupid = ( SELECT groupid FROM `group` AS g WHERE g.userid = %s );"
        cur.execute(getGrp, [uid])
        results = cur.fetchall()
        namelst=[]

        for row in results:
            getName = "SELECT name FROM `user` WHERE userid= %s"
            print(row[0])
            cur.execute(getName,[row[0]])
            name = cur.fetchall()
            namelst.append(name[0][0])

        #print(namelst)
        participantNames={}
        id = 0
        for user in namelst:
            participantNames[id] = user
            id = id + 1



        return jsonify(participantNames)

@app.route("/clearproto",methods=['POST'])
def clearproto():


    if not session.get("uid"):
        return redirect("/")


    cur = mysql.connection.cursor()

    response=request.form.keys()

    app.logger.info("sfdkjhsdkljsdhkjsdfhkjsdfhsfdakl")
    app.logger.info(response)


    for row in response:
        #app.logger.info(request.form.get(row))
        id=request.form.get(row);
        id=id.split("myCanvas")[-1]
        app.logger.info(id)
        query="delete from protoTable where imgid="+id+";"
        cur.execute(query)



    mysql.connection.commit()
    cur.close()
    return "Cleared all Proto"




@app.route("/proto")
def prototype():

    if not session.get("uid"):
        return redirect("/")
    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    if session.get("gid") == -1:
        return redirect("/waiting")

    wid = session['wid']
    uid = session['uid']
    gid = session['gid']

    data={"wid":wid, "gid": gid, "uid" : uid,"name":session['name']}

    return render_template('prototype.html',user=data)


@app.route("/chat")
def chatbox():

    if not session.get("uid"):
        return redirect("/")

    return render_template('chatbox.html')


@app.route("/define")
def define():

    if not session.get("uid"):
        return redirect("/")

    if session.get("gid") == -1:
        return redirect("/waiting")

    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = session['wid']
    uid = session['uid']
    gid = session['gid']

    data={"wid":wid, "gid": gid, "uid" : uid,"name":session['name']}
    return render_template('define.html',user=data)


@app.route("/ideate")
def ideate():

    if not session.get("uid"):
        return redirect("/")

    if session.get("gid") == -1:
        return redirect("/waiting")

    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = session['wid']
    uid = session['uid']
    gid = session['gid']

    app.logger.warning(wid)
    app.logger.warning(uid)
    app.logger.warning(gid)

    data={"wid":wid, "gid": gid, "uid" : uid, "name" : session['name'] }


    return render_template('ideate.html',user=data)



@app.route("/finalwall")
def finalwall():

    if not session.get("uid"):
        return redirect("/")
    # global startTime
    # startTime = int(time.time())
    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}
    return render_template('finalwall.html',user=data)



if __name__ == '__main__':
    app.run(debug=True)
