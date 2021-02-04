from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
import math

from baseApp.models import tblFeeders
from .models import tblMeters

@login_required(login_url='/accounts/')
def home_view(request):
    context = {}
    currUser = request.user
    
    if currUser.is_superuser:
        return redirect('admin:home')

    # t1 = currUser.lastTime
    # bill = currUser.bill
    # consumedUnits = currUser.consumedUnits
    # currActiveLoad = currUser.currActiveLoad
    # cost = TblUnitprice.objects.values('cost')

    # unitPrice = []
    # for item in cost:
    #     unitPrice.append(item.get('cost'))

    # fmt = "%d:%H:%M"
    # if  t1 == '01:00:00':
    #     t1 = datetime.now().strftime(fmt)
    # t2 = datetime.now().strftime(fmt)
    # tDiff = datetime.strptime(t2, fmt) - datetime.strptime(t1, fmt)
    # totalMin = math.floor(tDiff.total_seconds()/60)
    # currHr = datetime.strptime(t2, fmt).strftime("%H")
    # index = int(currHr)

    # j = totalMin%60
    # for i in range(totalMin):
    #     bill += currActiveLoad*(unitPrice[index]/60)
    #     j -= 1
    #     if j < 0:
    #         j = 59
    #         index -= 1
    #         if index < 0:
    #             index = 23

    # currUser.bill = bill
    # currUser.consumedUnits += currActiveLoad*(totalMin/60)
    # currUser.lastTime = t2

    # if request.method == 'POST':
    #     action = request.POST.get('load_action')
    #     action = int(action)
    #     load = request.POST.getlist('load')

    #     total_load = 0
    #     for unit_load in load:
    #         unit_load = int(unit_load)
    #         total_load += unit_load
        
    #     if action:
    #         currUser.currActiveLoad += total_load
    #     elif not action:
    #         if (currActiveLoad - total_load) < 0:
    #             currUser.currActiveLoad = 0
    #         else:
    #             currUser.currActiveLoad -= total_load
    #     else:
    #         pass
    # else:
    #     pass

    # currUser.save()
    meterID = tblMeters.objects.values('id', 'isActive').filter(user = currUser)
    context.update({
        'meterID' : meterID,
    })

    return render(request, 'userApp/home.html', context=context)
    
@login_required(login_url='/accounts/')
def profile_view(request):
    return render(request, 'userApp/profile.html')

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

            # This Quesry returns the total number of connections a user has.
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
            
            return render(request, 'userApp/home.html', context=context)
        else:
            pass
    else:
        pass
    return render(request, 'userApp/meter.html', context=context)