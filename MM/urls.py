"""MM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views import View

from . import EmployeeView, categoriesview, subcategoriesview, productview, adminView, FinalProductView, supplierView, \
    purchaseView, issueView
from . import statecity





urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),
    path('AdminLogin/', adminView.AdminLogin),
    path('checkadminlogin',adminView.checkadminlogin),
    path('AdminLogout/',adminView.AdminLogout),
    #Employee
    path('employeelogin/', EmployeeView.EmployeeLogin),
    path('employeedashboard/', EmployeeView.EmployeeDashboard),
    path('CheckEmployeeLogin', EmployeeView.CheckEmployeeLogin),
    path('EmployeeLogout/',EmployeeView.EmployeeLogout),

    path('EmployeeDetails/',EmployeeView.EmployeeInterface),
    path('Employeesubmit', EmployeeView.Employeesubmit),
    path('displayall/', EmployeeView.DisplayAll),
path('GETEmployeeJSON',EmployeeView.GETEmployeeJSON),
    path('displayemployeeid/', EmployeeView.displayemployeeid),
    path('editdeleterecordE/', EmployeeView.EditDeleteRecord),
    path('editemployeepicture/', EmployeeView.EditEmployeePicture),
    path('saveeditpicture', EmployeeView.saveeditpicture),


    #Categories
    path('categoriesdetail/',categoriesview.categoriesInterface),

path('dashboard/',categoriesview.DashboardInterface),
     path('categoriessubmit',categoriesview.categoriessubmit),
    path('displaycategoriesid/', categoriesview.displaycategoriesid),
    path('DisplayAllCategories/', categoriesview.DisplayAllCategories),
    path('GETCategoriesJSON',categoriesview.GETCategoriesJSON),
    path('EditDeleteRecord/', categoriesview.EditDeleteRecord),
    path('EditCategoryPicture/', categoriesview.EditCategoryPicture),
    path('SaveEditCategoryIcon', categoriesview.SaveEditCategoryIcon),

    #subcategories
    path('subcategoriesdetails/', subcategoriesview.subcategoriesInterface),
    path('subcategoriessubmit', subcategoriesview.subcategoriessubmit),
    path('DisplayAllSUBCategories/', subcategoriesview.DisplayAllSUBCategories),
    path('GETSUBCategoriesJSON',subcategoriesview.GETSUBCategoriesJSON),
    path('displaysubcategoriesid/', subcategoriesview.displaysubcategoriesid),
    path('EditDeleteRecordS/', subcategoriesview.EditDeleteRecordS),
    path('EditCategoryPictureS/', subcategoriesview.EditCategoryPictureS),
    path('SaveEditCategoryIconS', subcategoriesview.SaveEditCategoryIconS),



    #products
    path('products/', productview.productInterface),
    path('productssubmit', productview.productssubmit),
    path('DisplayAllProducts/', productview.DisplayAllProducts),
    path('displayproductid/',productview.displayproductid),
    path('GETProductJSON',productview.GETProductJSON),
    path('EditDeleteRecordP/', productview.EditDeleteRecordP),
    path('EditProductPictureP/', productview.EditProductPictureP),
    path('SaveEditCategoryIconP', productview.SaveEditCategoryIconP),

    #Final Products
    path('Final Product/', FinalProductView.finalproductInterface),
    path('finalproductssubmit', FinalProductView.finalproductssubmit),
    path('DisplayAllFinalProducts/', FinalProductView.DisplayAllFinalProducts),
    path('displayFinalproductid/', FinalProductView.displayFinalproductid),
    path('GETFinalProductJSON',FinalProductView.GETFinalProductJSON),
    path('DisplayFinalProductByIdJSON/', FinalProductView.DisplayFinalProductByIdJSON),
    path('DisplayFinalProductByAllJSON/', FinalProductView.DisplayFinalProductByAllJSON),
    path('DisplayStock/', FinalProductView.DisplayStock),


    path('EditDeleteRecordPF/', FinalProductView.EditDeleteRecordPF),
    path('EditProductPicturePF/', FinalProductView.EditProductPicturePF),
    path('SaveEditCategoryIconPF', FinalProductView.SaveEditCategoryIconPF),


#Supplier
    path('supplier/', supplierView.SupplierInterface),
    path('suppliersubmit', supplierView.suppliersubmit),
    path('DisplayAllSupplier/',supplierView.DisplayAllSupplier),
    path('GETSupplierJSON', supplierView.GETSupplierJSON),

#purchase
    path('purchase/', purchaseView.purchaseInterface),
    path('purchasesubmit', purchaseView.purchasesubmit),
    path('DisplayAllPurchase/', purchaseView.DisplayAllPurchase),

#issue
    path('issue/', issueView.IssueInterface),
    path('Issuesubmit', issueView.Issuesubmit),
    path('DisplayAllIssue/', issueView.DisplayAllIssue),
    path('displayissueid/', issueView.displayissueid),
    path('EditDeleteRecordI/', issueView.EditDeleteRecordI),







    path('fetchallstates/',statecity.FetchAllStates),
    path('fetchallcity/',statecity.FetchAllcity)

]
