from django.shortcuts import render
from . import pool
import uuid
from django.http import JsonResponse
import os
def categoriesInterface(request):
    return render(request,"categoriesdetail.html")

def DashboardInterface(request):
    return render(request,"dashboardview.html")
def categoriessubmit(request):
    try:
        categoriesname=request.POST['categoriesname']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "insert into categories(categoriesname, picture)values('{}','{}')".format(categoriesname, filename)


        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("F:/MM/assets/" + filename, "wb")

        for chunk in picture.chunks():
         F.write(chunk)
         F.close()
         db.close()
         return render(request, "categoriesdetail.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
      print(e)
      return render(request, "categoriesdetail.html", {'msg': 'Record NOT Submitted'})
def DisplayAllCategories(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select S .* from categories S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "categoriesdisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "categoriesdisplay.html", {'rows': []})

def GETCategoriesJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select S .* from categories S"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

def displaycategoriesid(request):
    caid=request.GET["caid"]
    print("ankit")
    try:
        db, cmd = pool.ConnectionPool()
        q="select C.*  From categories C where categoriesid={}".format(caid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "displaycategoriesid.html", {'row':row})
    except Exception as e:
        return render(request, "displaycategoriesid.html", {'row': []})

def EditDeleteRecord(request):
    btn=request.GET['btn']
    caid = request.GET["caid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
     categoriesname = request.GET['categoriesname']

     try:
         db, cmd = pool.ConnectionPool()
         q = "update categories set categoriesname='{}' where categoriesid={}".format(categoriesname,caid)
         print (q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAllCategories(request)
     except Exception as e:
        print("Error:", e)
        return DisplayAllCategories(request)

    elif(btn=="Delete"):

     try:
         db, cmd = pool.ConnectionPool()
         q="delete  From categories  where categoriesid={}".format(caid)
         cmd.execute(q)

         db.commit()
         db.close()
         return DisplayAllCategories(request)
     except Exception as e:
        return DisplayAllCategories(request)
def EditCategoryPicture(request):
    try:
        categoriesid=request.GET['caid']
        categoriesname=request.GET['categoriesname']
        picture=request.GET['picture']
        row=[categoriesid,categoriesname,picture]
        return render(request,"EditCategoryPicture.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditCategoryPicture.html",{'row':[]})

def SaveEditCategoryIcon(request):
    try:
        categoriesid=request.POST['caidp']
        #oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update categories set picture='{}' where categoriesid={}".format(filename,categoriesid)
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
        return DisplayAllCategories(request)
    except Exception as e:
        print("Error:", e)
        return DisplayAllCategories(request)


