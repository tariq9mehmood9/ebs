from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
import math
from baseApp.models import tblFeeders, tblTariffs
from .models import tblMeters, tblBills

@login_required(login_url='/accounts/')
def home_view(request):
    context = {}
    currUser = request.user
    if currUser.is_superuser:
        return redirect('admin:home')
    meterID = tblMeters.objects.values('id', 'isActive', 'connectionType', 'meterType', 'feederName').filter(user = currUser)
    context.update({
        'meterID' : meterID,
    })
    return render(request, 'userApp/home.html', context=context)

@login_required(login_url='/accounts/')
def meter_view(request):
    context = {}
    currUser = request.user
    fmt = "%Y:%m:%d"
    if request.method == 'POST':
        source = request.POST.get('source')
        meterID = tblMeters.objects.values('id', 'isActive').filter(user = currUser)
        context.update({
            'meterID' : meterID,
        })
        if source == 'Single' or source == 'Three':
            context.update({
                'meterType' : source
            })
            return render(request, 'userApp/meter.html', context=context)
        elif source == 'Meter':
            totalConn = tblMeters.objects.filter(user = currUser).count()
            if totalConn >= 3:
                messages.add_message(request, messages.ERROR, 'Request failed. You already have ' + str(totalConn) + ' connections!')
                return render(request, 'userApp/home.html', context=context)
            address = request.POST.get('address')
            connectionType = request.POST.get('connectionType')
            meterType = request.POST.get('meterType')
            location = request.POST.get('location')
            installationDate = datetime.now().strftime(fmt)
            location = tblFeeders.objects.get(name = location)
            newMeterConnection = tblMeters(
                user = currUser,
                feederName = location,
                meterType = meterType,
                connectionType = connectionType,
                address = address,
                installationDate = installationDate,
                isActive = True
            )
            newMeterConnection.save()
            return redirect('userApp:home')
    return render(request, 'userApp/meter.html', context=context)

@login_required(login_url='/accounts/')
def viewBill_view(request):
    context = {}
    currUser = request.user
    if request.method == 'POST':
        meterID = request.POST.get('meterID')
        meter = tblMeters.objects.get(id = meterID)
        user = User.objects.get(username = currUser)
        feeder = tblFeeders.objects.get(name = meter.feederName)
        bills = tblBills.objects.filter(meterID = meter)
        if len(bills) == 0:
            messages.add_message(request, messages.ERROR, 'Bill Record Does Not Exist')
            return redirect('userApp:home')
        latestBill = bills.latest('id').id
        latestBill = tblBills.objects.get(id = latestBill)
        prevBills = bills[::-1][1:12]
        
        tariff = tblTariffs.objects.get(tariffID = meter.connectionType)
        units = latestBill.units
        slabs = {
            "R": [300, 700],
            "C": [500, 1000],
            "I": [1000, 3000]
        }
        slab1, slab2 = slabs[tariff.tariffID]
        if units <= slab1:
            eCost = units * tariff.slab1Rate
        elif units <= slab2:
            eCost = slab1 * tariff.slab1Rate + (units-slab1) * tariff.slab2Rate
        else:
            eCost = slab2 * tariff.slab2Rate + (units-slab2) * tariff.slab3Rate
        eDuty = tariff.EDuty * (eCost/100)
        NJS = tariff.NJS * units
        FCS = tariff.FCS * units
        GST = (eCost + NJS + FCS)/100
        if meter.meterType == 'Single':
            meterRent = tariff.singlePhMeterRent
        else:
            meterRent = tariff.threePhMeterRent
        tariff = {
            'eCost' : eCost,
            'meterRent' : meterRent,
            'TVFee' : tariff.TVFee,
            'eDuty' : eDuty,
            'NJS' : NJS,
            'FCS' : FCS,
            'GST' : GST
        }
        context.update({
            'user' : user,
            'meter' : meter,
            'tariff' : tariff,
            'feeder' : feeder,
            'bills' : bills,
            'latestBill' : latestBill,
            'prevBills' : prevBills
        })
    return render(request, 'userApp/viewBill.html', context=context)