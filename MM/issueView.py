from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
def IssueInterface(request):
   try:
     result = request.session['EMPLOYEE']
     print(result)
     return render(request, "issue.html", {'result': result})

   except Exception as e:
      return render(request, 'EmployeeLogin.html')
def Issuesubmit(request):
    try:

        employeeid=request.POST['employeeid']
        categoriesid = request.POST['categoriesid']
        subcategoriesid = request.POST['subcategoriesid']
        productid= request.POST['productid']
        FinalProductid=request.POST['finalproductid']
        demand_employeeid = request.POST['demand_employeeid']
        issuedate=request.POST['issuedate']
        qty = request.POST['qty']
        remark = request.POST['remark']
        q = "insert into  issue (employeeid,categoriesid, subcategoriesid, productid, finalproductid,demand_employeeid, issuedate, qty, remark)values({},{},{},{},{},{},'{}',{},'{}')".format(employeeid,categoriesid,subcategoriesid,productid,FinalProductid,demand_employeeid,issuedate,qty,remark)
        print(q)
        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        q = "update finalproduct set Stock=Stock-{} where finalproductid={}".format(qty,FinalProductid)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "issue.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
      print(e)
      return render(request, "issue.html", {'msg': 'Record NOT Submitted'})

def DisplayAllIssue(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select I.* from issue I"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "IssueDisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "IssueDisplay.html", {'rows': []})

def displayissueid(request):
    Iid=request.GET["Iid"]
    print("ankit")
    try:
        db, cmd = pool.ConnectionPool()
        q="select I.*  From issue I where issueid={}".format(Iid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "displayproductid.html", {'row':row})
    except Exception as e:
        return render(request, "displayproductid.html", {'row': []})


def EditDeleteRecordI(request):
    btn=request.GET['btn']
    Iid = request.GET["Iid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        employeeid = request.GET['employeeid']
        categoriesid = request.GET['categoriesid']
        subcategoriesid = request.GET['subcategoriesid']
        productid = request.GET['productid']
        finalproductid = request.GET['finalproductid']
        demand_employeeid = request.GET['demand_employeeid']
        issuedate = request.GET['issuedate']
        qty = request.GET['qty']
        remark = request.GET['remark']
        try:
         db, cmd = pool.ConnectionPool()
         q = "update issue set employeeid={},categoriesid={},subcategoriesid={},productid={},FinalProductid={},demand_employeeid={},issuedate='{}', qty={},remark='{}'  where issueid={} ".format( employeeid, categoriesid, subcategoriesid, productid, finalproductid, demand_employeeid, issuedate, qty, remark,Iid)
         print (q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAllIssue(request)
        except Exception as e:
         print("Error:", e)
         return DisplayAllIssue(request)

    elif (btn == "Delete"):

     try:
        db, cmd = pool.ConnectionPool()
        q="delete I.*  From issue I where issueid={}".format(Iid)
        cmd.execute(q)

        db.commit()
        db.close()
        return DisplayAllIssue(request)
     except Exception as e:
        return DisplayAllIssue(request)

