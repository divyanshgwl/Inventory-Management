from django.shortcuts import render
from . import pool
import os
from django.views.decorators.clickjacking import xframe_options_exempt
import uuid
from django.http import JsonResponse
def SupplierInterface(request):
   # try:
      #  result=request.session['ADMIN']
       # return render(request, "AdminDashboard.html", {'result': result})

    #except Exception as e:

     return render(request,"supplier.html")
def suppliersubmit(request):
    try:
        Suppliername=request.POST['Suppliername']
        mobileno = request.POST['mobileno']
        emailid = request.POST['emailid']
        address = request.POST['address']
        stateid = request.POST['state']
        cityid = request.POST['city']

        q = "insert into supplier( Suppliername, mobileno, emailid, address, stateid, cityid)values('{}','{}','{}','{}',{},{})".format(Suppliername, mobileno, emailid, address, stateid, cityid)

        print(q)
        db,cmd=pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "supplier.html", {'msg': 'Record Successfully Submitted'})
    except Exception as e:
        print(e)
        return render(request, "supplier.html", {'msg': 'Record NOT Submitted'})

def DisplayAllSupplier(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select PF.*,(select C.cityname from Cities C where C.cityid=PF.cityid),(select S.statename from states S where S.stateid=PF.stateid) from supplier PF "
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "SupplierDispaly.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "SupplierDispaly.html", {'rows': []})
def GETSupplierJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select S .* from supplier S "
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

