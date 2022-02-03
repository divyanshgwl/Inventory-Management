from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
def productInterface(request):
    return render(request,"products.html")
def productssubmit(request):
    try:
        categoriesid = request.POST['categoriesid']
        subcategoriesid = request.POST['subcategoriesid']
        productname=request.POST['productname']
        Description=request.POST['Description']
        gst=request.POST['gst']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "insert into products (categoriesid,subcategoriesid,productname,Description,gst, picture)values({},{},'{}','{}',{},'{}')".format(categoriesid,subcategoriesid,productname,Description,gst, filename)


        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("F:/MM/assets/" + filename, "wb")

        for chunk in picture.chunks():
         F.write(chunk)
         F.close()
         db.close()
         return render(request, "products.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
      print(e)
      return render(request, "products.html", {'msg': 'Record NOT Submitted'})

def DisplayAllProducts(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select P .* from products P"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "productdisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "productdisplay.html", {'rows': []})

def displayproductid(request):
    pid=request.GET["pid"]
    print("ankit")
    try:
        db, cmd = pool.ConnectionPool()
        q="select P.*  From products P where productid={}".format(pid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "displayproductid.html", {'row':row})
    except Exception as e:
        return render(request, "displayproductid.html", {'row': []})
def GETProductJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select P .* from products P"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)


def EditDeleteRecordP(request):
    btn=request.GET['btn']
    pid = request.GET["pid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        categoriesid=request.GET['categoriesid']
        subcategoriesid=request.GET['subcategoriesid']
        productname = request.GET['productname']
        description=request.GET['description']
        gst=request.GET['gst']
        try:
         db, cmd = pool.ConnectionPool()
         q = "update products set categoriesid={},subcategoriesid={},productname='{}',description='{}',gst={} where productid={} ".format(categoriesid,subcategoriesid,productname,description,gst,pid)
         print (q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAllProducts(request)
        except Exception as e:
         print("Error:", e)
         return DisplayAllProducts(request)

    elif (btn == "Delete"):

     try:
        db, cmd = pool.ConnectionPool()
        q = "delete  From products  where productid={}".format(pid)
        cmd.execute(q)

        db.commit()
        db.close()
        return DisplayAllProducts(request)
     except Exception as e:
        return DisplayAllProducts(request)
def EditProductPictureP(request):
    try:
        productid=request.GET['pid']
        productname=request.GET['productname']
        picture=request.GET['picture']
        row=[productid,productname,picture]
        return render(request,"EditCategoryPicture.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditCategoryPicture.html",{'row':[]})

def SaveEditCategoryIconP(request):
    try:
        productid=request.POST['pidp']
        #oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update products set picture='{}' where productid={}".format(filename,productid)
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
        return DisplayAllProducts(request)
    except Exception as e:
        print("Error:", e)
        return DisplayAllProducts(request)




