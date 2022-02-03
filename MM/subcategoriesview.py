from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
import cryptography
def subcategoriesInterface(request):
    return render(request,"subcategoriesdetails.html")
def subcategoriessubmit(request):
    try:
        categoriesid=request.POST['categoriesid']
        subcategoriesname = request.POST['subcategoriesname']
        Description=request.POST['Description']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "insert into subcategories (categoriesid, subcategoriesname, Description, picture)values({},'{}','{}','{}')".format(categoriesid,subcategoriesname,Description,filename)
        print(q)
        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("F:/MM/assets/" + filename, "wb")

        for chunk in picture.chunks():
            F.write(chunk)
            F.close()
            db.close()
            return render(request, "subcategoriesdetails.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
        print("dbjhsgihihsi",e)
        return render(request, "subcategoriesdetails.html", {'msg': 'Record NOT Submitted'})
def DisplayAllSUBCategories(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select S .* from subcategories S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "subcategoriesdisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "subcategoriesdisplay.html", {'rows': []})

def GETSUBCategoriesJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select S .* from subcategories S"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)

def displaysubcategoriesid(request):
    scaid=request.GET["scaid"]
    print("ankit")
    try:
        db, cmd = pool.ConnectionPool()
        q="select C.*  From subcategories C where subcategoriesid={}".format(scaid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "displaysubcategoriesid.html", {'row':row})
    except Exception as e:
        return render(request, "displaysubcategoriesid.html", {'row': []})

def EditDeleteRecordS(request):
    btn=request.GET['btn']
    scaid = request.GET["scaid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        categoriesid=request.GET['categoriesid']
        subcategoriesname = request.GET['subcategoriesname']
        Description=request.GET['Description']

        try:
         db, cmd = pool.ConnectionPool()
         q = "update subcategories set categoriesid={},subcategoriesname='{}',Description='{}' where subcategoriesid={}".format(categoriesid,subcategoriesname,Description,scaid)
         print (q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAllSUBCategories(request)
        except Exception as e:
         print("Error:", e)
         return DisplayAllSUBCategories(request)

    elif (btn == "Delete"):

     try:
        db, cmd = pool.ConnectionPool()
        q = "delete  From subcategories  where subcategoriesid={}".format(scaid)
        cmd.execute(q)

        db.commit()
        db.close()
        return DisplayAllSUBCategories(request)
     except Exception as e:
        return DisplayAllSUBCategories(request)


def EditCategoryPictureS(request):
    try:
        subcategoriesid = request.GET['scaid']
        subcategoriesname = request.GET['subcategoriesname']
        picture = request.GET['picture']
        row = [subcategoriesid, subcategoriesname, picture]
        return render(request, "EditCategoryPicture.html", {'row': row})
    except Exception as e:
        print('error:', e)
        return render(request, "EditCategoryPicture.html", {'row': []})


def SaveEditCategoryIconS(request):
    try:
        subcategoriesid = request.POST['scaidp']
        #oldpicture = request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "update subcategories set picture='{}' where subcategoriesid={}".format(filename, subcategoriesid)
        print(q)
        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("F:/MM/assets/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('F:/MM/assets/' + oldpicture)
        return DisplayAllSUBCategories(request)
    except Exception as e:
        print("Error:", e)
        return DisplayAllSUBCategories(request)









