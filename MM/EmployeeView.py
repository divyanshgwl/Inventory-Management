from django.shortcuts import render
from . import pool,poolDict
import random
import os
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import uuid
from.import EmailService
@xframe_options_exempt
def EmployeeLogin(request):
    return render(request,'EmployeeLogin.html')

@xframe_options_exempt
def CheckEmployeeLogin(request):
  try:
    emailaddress = request.POST['emailid']
    password = request.POST['password']

    dbe,cmd = poolDict.ConnectionPool()
    q = "select * from employeedata where email = '{}' and password = '{}'".format(emailaddress,password)
    cmd.execute(q)
    result = cmd.fetchone()
    print(result)
    if(result):
        request.session['EMPLOYEE'] = result
        return render(request,"EmployeeDashboard.html",{'result': result})
    else:
        return render(request,"EmployeeLogin.html",{'result': result, 'msg': 'Invalid Email / Password '})
    dbe.close()
  except Exception as e:
    print(e)
    return render(request,"EmployeeLogin.html",{'result': {}, 'msg' : 'Server Error'})


@xframe_options_exempt
def EmployeeLogout(request):
    del request.session['EMPLOYEE']
    return render(request,'EmployeeLogin.html')


@xframe_options_exempt
def EmployeeDashboard(request):
  return render(request,"EmployeeDashboard.html")





def EmployeeInterface(request):
   try:
        result=request.session['EMPLOYEE']
        return render(request, "EmployeeDetail.html", {'result': result})

   except Exception as e:

     return render(request,"EmployeeDashboard.html")
def Employeesubmit(request):
    try:
        firstname=request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        Birthdate = request.POST['birthdate']
        paddress = request.POST['paddress']
        State = request.POST['state']
        city = request.POST['city']
        caddress = request.POST['caddress']
        Email = request.POST['emailaddress']
        Mnunder = request.POST['mobilenumber']
        Designation = request.POST['designation']
        picture=request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        password = "".join(random.sample(['1', 'a', '4', 'x', '6', '66', '#', '@'], k=7))

        q = "insert into employeedata(firstname, lastname, gender, dob, paddress, stateid, cityid, caddress, email, mnumber, designation, picture, password)values('{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format(
            firstname, lastname, gender, Birthdate, paddress, State, city, caddress,Email, Mnunder,Designation, filename,password)

        print(q)
        db,cmd=pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("F:/MM/assets/"+filename,"wb")

        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
      #  result = Smssend.SendMessage("Hi {} Your Password is {}".format(firstname, password), Mnunder)
       # print(result.json())


        # EmailService.SendMail(emailaddress,"Hi {} Your Password is {}".format(firstname,password))
        EmailService.SendHTMLMail(Email, "Hi {} Your Password is {}".format(firstname, password))
        return render(request, "EmployeeDetail.html", {'msg': 'Record Successfully Submitted'})



    except Exception as e:
        print(e)
        return render(request, "EmployeeDetail.html", {'msg': 'Record NOT Submitted'})

def DisplayAll(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select E.*,(select C.cityname from Cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employeedata E "
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "employeedisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "employeedisplay.html", {'rows': []})
def GETEmployeeJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select E .* from employeedata E"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

def displayemployeeid(request):
    empid=request.GET["empid"]
    try:
        db, cmd = pool.ConnectionPool()
        q="select E.*,(select C.cityname from Cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employeedata E where employeeid={}".format(empid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "displayEmployeeid.html", {'row':row})
    except Exception as e:
        return render(request, "displayEmployeeid.html", {'row': []})

def EditDeleteRecord(request):
    btn=request.GET['btn']
    empid = request.GET["empid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):

     firstname = request.GET['firstname']
     lastname = request.GET['lastname']
     gender =    request.GET['gender']
     birthdate = request.GET['birthdate']
     paddress = request.GET['paddress']
     state = request.GET['state']
     city = request.GET['city']
     caddress = request.GET['caddress']
     emailaddress = request.GET['emailaddress']
     Mnunder = request.GET['mobilenumber']
     designation = request.GET['designation']

     try:
        db, cmd = pool.ConnectionPool()
        q = "update employeedata set firstname='{}', lastname='{}', gender='{}', dob='{}', paddress='{}', stateid={}, cityid={}, caddress='{}', email='{}', mnumber='{}', designation='{}' where employeeid={}".format(firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, Mnunder,designation,empid)
        print (q)
        cmd.execute(q)
        db.commit()
        db.close()
        return DisplayAll(request)
     except Exception as e:
        print("Error:", e)
        return DisplayAll(request)

    elif (btn=="Delete"):

        try:
            db, cmd = pool.ConnectionPool()
            q = "delete from employeedata where employeeid={}".format(empid)
            cmd.execute(q)

            db.commit()
            db.close()
            return DisplayAll(request)
        except Exception as e:

            return DisplayAll(request)

def EditEmployeePicture(request):
   try:
    empid = request.GET["empid"]
    firstname = request.GET['firstname']
    lastname = request.GET['lastname']
    picture = request.GET['picture']
    row=[empid,firstname,lastname,picture]
    return render(request, "EditEmployeePicture.html", {'row': row})
   except Exception as e:
    return render(request, "EditEmployeePicture.html", {'row': []})

def saveeditpicture(request):
    try:
       empid=request.POST['empid']
       oldpicture = request.POST['oldpicture']
       picture=request.FILES['picture']

       filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
       q="update employeedata set   picture='{}' where employeeid={}".format(filename,empid)
       print(q)
       db,cmd=pool.ConnectionPool()
       cmd.execute(q)
       db.commit()
       F=open("F:/MM/assets/"+filename,"wb")
       for chunk in picture.chunks():
           F.write(chunk)
       F.close()

       db.close()
       os.remove('F:/MM/assets/'+oldpicture)
       return DisplayAll(request)
    except Exception as e:
       return DisplayAll(request)











