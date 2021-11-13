from flask import Flask, session, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml, json
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


@app.route('/', methods=['GET', 'POST'])
def root():
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
    userid = cur.execute(
        "INSERT INTO `user` (`username`,`name`,`password`,`college`,`type`) VALUES (%s,%s,%s,%s,%s)",
        queryValues)
    cur.close()
    conn.commit()  #committing to the database
    return redirect('/')


# inserting data into register table while logging in
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('Email')
    password = request.form.get('Password')

    # getting user info from user table
    conn = mysql.connection
    cur = conn.cursor()
    values = cur.execute(
        "SELECT user.userid,user.type,user.username  FROM user where user.username = %s AND user.password = %s",
        [username, password])
    if (values > 0):
        userDetails = cur.fetchall()
        userid = userDetails[0][0]
        type = userDetails[0][1]
        uname = userDetails[0][2]

        #storing username and userid and grp id and workshop and type in session variable
        session['uid'] = userid
        session['type'] = type
        session['uname']= uname
        session['wid']= "1" #hardcoding the workshop Id


        # storing the userid in the registration table
        
        queryValues = [1, userid]
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


# functonalities of all admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/admin/teams', methods=['GET', 'POST'])
def teams():
    return render_template('teams.html')

@app.route('/admin/people', methods=['GET', 'POST'])
def people():
    return render_template('participants.html')


# displaying participants list
@app.route('/admin/people/showparticipants', methods=['post'])
def showparticipants():

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

    # getting count of memebers in each team from form
    # count = request.form.get('count')

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
        createdTeams = arrangeRandom(userIds, 3)
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
    cur = mysql.connection.cursor()
    app.logger.info(request.args.keys())
    wid = request.args.get('workid')
    gid = request.args.get('grpid')
    img = request.args.get('image')
    
    wid=1
    gid=1

    #cur.execute("select * from protoTable where ")

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
    
    cur = mysql.connection.cursor()
    uid = request.args.get('noteid')
    query="delete from wall where notesid="+uid+";"
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return "true"
    
@app.route("/returnSticky",methods=['GET'])
def returnSticky():
    cur = mysql.connection.cursor()
    query="select * from wall;"
    cur.execute(query)
    results = cur.fetchall()
    
    payload = []
    content = {}
    for result in results:
        content = {'notesid': result[3], 'textnote': result[4]}
        payload.append(content)
        content = {}
    

    #print(payload);
    cur.close()
    return jsonify(payload)


@app.route("/addSticky",methods=['GET'])
def addSticky():
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
    cur = mysql.connection.cursor()
    query1="select * from chat order by messageid;"
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


@app.route("/emphasize")
def participants():
    global startTime
    startTime = int(time.time())














































































































    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}

    return render_template('emphasize.html',user=data)

@app.route("/waiting")
def waiting():
    #useing session variable.........
    info={}
    info['wid']=session['wid']
    info['uid']=session['uid']
    info['gid']="1"
    return render_template('waiting.html',data=info)

@app.route("/isCreated", methods=["GET"])
def isCreated():
    cur = mysql.connection.cursor()
    uid = request.args.get('userid')

    empty="SELECT * FROM `group`;"
    numRow = cur.execute(empty)
    if(numRow==0):
        return "false"
    else:
        getGrp = "SELECT userid FROM `group` WHERE groupid = ( SELECT groupid FROM `group` AS g WHERE g.userid = %s );"
        cur.execute(getGrp, [uid])
        results = cur.fetchall();
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







@app.route("/proto")
def prototype():
    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}

    return render_template('prototype.html',user=data)


@app.route("/chat")
def chatbox():
    return render_template('chatbox.html')


@app.route("/define")
def define():
    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}
    return render_template('define.html',user=data)


@app.route("/ideate")
def ideate():
    #*********** Run Sql Query To fetch wid, Gid Uid From DAtabase

    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}


    return render_template('ideate.html',user=data)



@app.route("/finalwall")
def finalwall():
    # global startTime
    # startTime = int(time.time())
    wid = 1
    gid = 1
    uid = 2

    data={"workshopid":wid, "groupid": gid, "userid" : uid}
    return render_template('finalwall.html',user=data)






if __name__ == '__main__':
    app.run(debug=True)
