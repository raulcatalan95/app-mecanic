from django.shortcuts import render


def renderBase(request):
    return render(request,'base.html')