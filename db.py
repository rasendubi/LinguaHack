import hashlib
import psycopg2
import math

def dbconnect():
   "Create db connection"
   con = psycopg2.connect(database="LinguaHack", user="garage48", password="$garage48Ghjcnj156$", host="world-of-happiness.com") 
   return con

def dbdisconnect(con):
	"Close db connection"
	con.close()
	return
	
def GetHash(password,login):
	"Make hash of password"
	h = hashlib.sha256(str(password)+str(login))
	return h.hexdigest()
	
def register(login, password, name, birth):
	"User registration"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("INSERT INTO Users(login,password,name,birth) VALUES('"+login+"','"+GetHash(password,login)+"','"+name+"',"+str(birth)+");");
	con.commit()
	dbdisconnect(con)
	return 
	
def addplacesinfo(description, type):
	"Add proposition of the place"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("INSERT INTO Placesinfo(description, type) VALUES('"+description+"',"+str(type)+");");
	con.commit()
	dbdisconnect(con)
	return
	
def adduserplaces(userid, name, userplacestype, places):
	"Add place related to the user (under deployment?)"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("INSERT INTO Userplaces(userid, name, createdat, updatedat, userplacestype, places) VALUES("+str(userid)+",'"+name+"', "+str(createdat)+", "+str(updatedat)+", "+str(userplacestype)+", "+str(places)+";");
	con.commit()
	dbdisconnect(con)
	return

def radius(DiffLatitude,DiffLongitude,AvgLatitude):
	"Calculate distance between points from difference of latitude and longitude"
	return math.sqrt(DiffLatitude*DiffLatitude+math.cos(AvgLatitude)*math.cos(AvgLatitude)*DiffLongitude*DiffLongitude)

def getplaceinfo(index):
	"Get descriptions of offers"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT name, latitude,longitude, description, type FROM Place as p INNER JOIN PlacesInfo as pi ON p.fk_pl=pi.id INNER JOIN PlacesType as pt ON pt.id=pi.ptype WHERE p.id IN("+str(index)+");");
	res = cur.fetchall()
	dbdisconnect(con)
	return res

def getcalendarradius(latitude, longitude, max, userid):
	"Get all places from calendar that within given radius. Weak boundary from db. Strong boundary from python function."
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT * FROM GetCalendarRadius("+str(latitude)+","+str(max)+","+str(userid)+");");
	res = cur.fetchall()
	fetched = list()
	index = str()
	for r in res: 
		difflatitude = abs(r[1]-latitude)
		difflongitude = abs(r[2]-longitude)
		avglatitude = math.pi*(r[1]+latitude)/360
		if radius(difflatitude, difflongitude, avglatitude) < max*0.00545: ## adjusted for city. Straight distance is 0.009
			index += str(r[0])+","
	if len(index)!=0:
		index = index[:len(index)-1]
		fetched += getplaceinfo(index)
	dbdisconnect(con)
	return fetched
	
	
def getcalendaruserplacename(userid, name):
	"Get data according to the place name"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT c.id, title, text, createdat, updateat, alarmtime, type, latitude, longitude FROM Calendar as c INNER JOIN Place as p ON p.id=c.fk_place INNER JOIN calendartype as ctype ON c.ctype=ctype.id WHERE c.userid="+str(userid)+" AND p.name='"+name+"';");
	res = cur.fetchall()
	dbdisconnect(con)
	return res
	
def getcalendartype(userid, type):
	"Get data according to the type"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT * FROM Calendar WHERE ctype IN(SELECT id FROM CalendarType WHERE type LIKE '%"+type+"%') AND userid="+str(userid)+";");
	res = cur.fetchall()
	dbdisconnect(con)
	return res
	
def getcalendaralarm(userid, alarmmin, alarmmax):
	"Get data for selected time"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT * FROM Calendar WHERE alarmtime > "+str(alarmmin)+" AND alarmtime < "+str(alarmmax)+" AND userid ="+str(userid)+";");
	res = cur.fetchall()
	dbdisconnect(con)
	return res
	
def getcalendarcomplex(userid, alarmmin, alarmmax, latitude, longitude, max, type):
	"Get data passed through multiple filters"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT c.id,p.latitude,p.longitude FROM Calendar as c INNER JOIN Place as p ON p.id=c.fk_place WHERE abs(p.latitude-"+str(latitude)+")<"+str(0.00545*max)+" AND alarmtime<"+str(alarmmax)+" AND alarmtime>"+str(alarmmin)+" AND ctype IN(SELECT id FROM CalendarType WHERE type LIKE ('%"+type+"%')) AND userid="+str(userid)+";");
	res = cur.fetchall()
	fetched = list()
	index = str()
	for r in res: 
		difflatitude = abs(r[1]-latitude)
		difflongitude = abs(r[2]-longitude)
		avglatitude = math.pi*(r[1]+latitude)/360
		if radius(difflatitude, difflongitude, avglatitude) < max*0.00545: ## adjusted for city. Straight distance is 0.009
			index += str(r[0])+","
	if len(index)!=0:
		index = index[:len(index)-1]
		fetched += getplaceinfo(index)
	dbdisconnect(con)
	return fetched

def getuserplacestype(userid, type):
	"Get data from user_places that match given type"
	con = dbconnect()
	cur = con.cursor()
	ex = cur.execute("SELECT * FROM UsersPlacesType as ust INNER JOIN UsersPlaces as up ON up.ustype=ust.id WHERE ust.type='"+type+"' AND up.userid="+str(userid)+";");
	res = cur.fetchall()
	dbdisconnect(con)
	return res

def insertusersplacestype(type):
	"Add new users place type"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("INSERT INTO  UsersPlacesType (type) VALUES('"+type+"');");
	con.commit()
	dbdisconnect(con)
	return

def insertcalendar(userid, title, text, createat, alarmtime, ctypename, fk_placename):
	"Add new happening"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("Insert into Calendar (userid, title, text, createdat, updateat, alarmtime, ctype, fk_place) Values ()");
	con.commit()
	dbdisconnect(con)
	return
	
def insertcontact(userid,tel,cityname,fieldcontacts):
	"Add new contact"
	con = dbconnect()
	cur = con.cursor()
	cur.execute("INSERT INTO Contacts (userid,tel,cityname,FieldContacts) VALUES("+str(userid)+","+str(tel)+",'"+cityname+"','"+fieldcontacts+"')");
	con.commit()
	dbdisconnect(con)
	return
	
print(getcalendarradius(50.4393483,30.5150462,1,1))
