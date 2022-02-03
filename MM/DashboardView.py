from django.shortcuts import render

def DashboardInterface(request):
    return render(request,"dashboardview.html")