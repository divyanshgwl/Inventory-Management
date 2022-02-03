from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
def purchaseInterface(request):

    try:
     result = request.session['EMPLOYEE']
     print(result)
     return render(request, "purchase.html", {'result': result})

    except Exception as e:
     return render(request, 'EmployeeLogin.html')
def purchasesubmit(request):
    try:

        categoriesid = request.POST['categoriesid']
        subcategoriesid = request.POST['subcategoriesid']
        productid= request.POST['productid']
        FinalProductid=request.POST['finalproductid']
        supplierid=request.POST['supplierid']
        employeeid = request.POST['employeeid']
        purchasedate=request.POST['purchasedate']
        Stock = request.POST['Stock']
        amount = request.POST['amount']
        q = "insert into purchase (categoriesid, subcategoriesid, productid, finalproductid, supplierid,employeeid, purchasedate, stock, amount)values({},{},{},{},{},{},'{}','{}','{}')".format(categoriesid,subcategoriesid,productid,FinalProductid,supplierid,employeeid,purchasedate,Stock,amount)
        print(q)
        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        q="update finalproduct set Price=((Price+{})/2) , Stock=Stock+{} where finalproductid={}".format(amount,Stock,FinalProductid)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "purchase.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
      print(e)
      return render(request, "purchase.html", {'msg': 'Record NOT Submitted'})

def DisplayAllPurchase(request):
    try:
        db, cmd = pool.ConnectionPool()
        q = "select PP.*,(select C.categoriesname from categories C where C.categoriesid = PP.categoriesid),(select S.subcategoriesname from subcategories S where S.subcategoriesid = PP.subcategoriesid), (select P.productname from products P where P.productid = PP.productid), (select FP.FinalProductName from finalproduct FP where FP.FinalProductId = PP.FinalProductId), (select S.Suppliername from supplier S where S.Supplierid = PP.Supplierid) from purchase PP"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "purchaseDisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "purchaseDisplay.html", {'rows': []})

