from django.shortcuts import render
from . import pool,poolDict
import uuid
import os
from django.http import JsonResponse
def finalproductInterface(request):
    return render(request,"Final Product.html")

def DisplayFinalProductByIdJSON(request):
    finalproductid=request.GET["finalproductid"]
    try:
        dbe, cmd = poolDict.ConnectionPool()
        q = "select FP.*,(select C.categoriesname  from categories C where C.categoriesid = FP.categoriesid),(select S.subcategoriesname from subcategories S where S.subcategoriesid = FP.subcategoriesid), (select P.productname from products P where P.productid = FP.productid) from finalproduct FP where FinalProductId={}".format(finalproductid)

        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return JsonResponse(row, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def DisplayStock(request):
    return render(request, "listofallemployee.html")

def DisplayFinalProductByAllJSON(request):
    pattern=request.GET["pattern"]
    try:
        dbe, cmd = poolDict.ConnectionPool()
        q = "select FP.*,(select C.categoriesname  from categories C where C.categoriesid = FP.categoriesid),(select S.subcategoriesname from subcategories S where S.subcategoriesid = FP.subcategoriesid), (select P.productname from products P where P.productid = FP.productid) from finalproduct FP where FinalProductName='%{}%' ".format(pattern)

        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)


def DisplayUpdatedStock(request):
    return render(request, "ListProductsEmployee.html")


def finalproductssubmit(request):
    try:
        categoriesid = request.POST['categoriesid']
        subcategoriesid = request.POST['subcategoriesid']
        productid= request.POST['productid']
        FinalProductName=request.POST['FinalProductName']
        Size=request.POST['Size']
        Weight=request.POST['Weight']
        Price = request.POST['Price']
        Stock = request.POST['Stock']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "insert into finalproduct (categoriesid, subcategoriesid, productid, FinalProductName, Size, Weight, Price, Stock, Picture)values({},{},{},'{}','{}',{},'{}','{}','{}')".format(categoriesid,subcategoriesid,productid,FinalProductName,Size,Weight,Price,Stock,filename)


        db, cmd = pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("F:/MM/assets/" + filename, "wb")

        for chunk in picture.chunks():
         F.write(chunk)
         F.close()
         db.close()
         return render(request, "Final Product.html", {'msg': 'Record Successfully Submitted'})

    except Exception as e:
      print(e)
      return render(request, "Final Product.html", {'msg': 'Record NOT Submitted'})

def DisplayAllFinalProducts(request):
    try:
        db, cmd = pool.ConnectionPool()
        q = "select FP.*,(select C.categoriesname  from categories C where C.categoriesid = FP.categoriesid),(select S.subcategoriesname from subcategories S where S.subcategoriesid = FP.subcategoriesid), (select P.productname from products P where P.productid = FP.productid) from finalproduct FP"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request, "FinalProductDisplay.html", {'rows':rows})
    except Exception as e:
        print(e)
        return render(request, "FinalProductDisplay.html", {'rows': []})

def displayFinalproductid(request):
    pfid=request.GET["pfid"]
    print("ankit")
    try:
        db, cmd = pool.ConnectionPool()
        q = "select FP.*,(select C.categoriesname  from categories C where C.categoriesid = FP.categoriesid),(select S.subcategoriesname from subcategories S where S.subcategoriesid = FP.subcategoriesid), (select P.productname from products P where P.productid = FP.productid) from finalproduct FP where FinalProductId={}".format(pfid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request, "Finaldisplayproductid.html", {'row':row})
    except Exception as e:
        return render(request, "Finaldisplayproductid.html", {'row': []})
def GETFinalProductJSON(request):
    try:
        db, cmd = pool.ConnectionPool()
        q="select PF .* from finalproduct PF"
        cmd.execute(q)
        rows=cmd.fetchall()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([],safe=False)




def EditDeleteRecordPF(request):
    btn=request.GET['btn']
    pfid = request.GET["pfid"]
    print("xxxxxxxxxxxx",btn)
    if(btn=="Edit"):
        categoriesid=request.GET['categoriesid']
        subcategoriesid=request.GET['subcategoriesid']
        productid = request.GET['productid']
        FinalProductName = request.GET['FinalProductName']
        Size=request.GET['Size']
        Weight=request.GET['Weight']
        Price = request.GET['Price']
        Stock = request.GET['Stock']
        try:
         db, cmd = pool.ConnectionPool()
         q = "update finalproduct set categoriesid={},subcategoriesid={},productid={},FinalProductName='{}',Size='{}',Weight='{}',Price='{}',Stock='{}' where FinalProductId={} ".format(categoriesid,subcategoriesid,productid,FinalProductName,Size,Weight,Price,Stock,pfid)
         print (q)
         cmd.execute(q)
         db.commit()
         db.close()
         return DisplayAllFinalProducts(request)
        except Exception as e:
         print("Error:", e)
         return DisplayAllFinalProducts(request)

    elif (btn == "Delete"):

     try:
        db, cmd = pool.ConnectionPool()
        q = "delete  From finalproduct  where FinalProductId={}".format(pfid)
        cmd.execute(q)

        db.commit()
        db.close()
        return DisplayAllFinalProducts(request)
     except Exception as e:
        return DisplayAllFinalProducts(request)
def EditProductPicturePF(request):
    try:
        FinalProductId=request.GET['pfid']
        FinalProductName=request.GET['FinalProductName']
        picture=request.GET['picture']
        row=[FinalProductId,FinalProductName,picture]
        return render(request,"EditCategoryPicture.html",{'row':row})
    except Exception as e:
        print('error:',e)
        return render(request,"EditCategoryPicture.html",{'row':[]})

def SaveEditCategoryIconPF(request):
    try:
        FinalProductId=request.POST['pfidp']
        #oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update finalproduct set picture='{}' where FinalProductId={} ".format(filename,FinalProductId)
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
        return DisplayAllFinalProducts(request)
    except Exception as e:
        print("Error:", e)
        return DisplayAllFinalProducts(request)




