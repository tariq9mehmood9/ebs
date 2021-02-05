from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from baseApp.models import tblFeeders, tblTariffs
from userApp.models import tblMeters, tblBills
from django.contrib.auth.models import User
from datetime import datetime, timedelta

@login_required(login_url='/accounts/')
def home_view(request):
    context = {}
    currUser = request.user
    
    if not currUser.is_superuser:
        messages.add_message(request, messages.ERROR, 'Admin credentials are Wrong!')
        return redirect('accounts:login')
    
    tariffData = tblTariffs.objects.all()
    feederData = tblFeeders.objects.all()
    context.update({
        'tariffData' : tariffData,
        'feederData' : feederData
    })

    return render(request, 'admin/home.html', context=context)

@login_required(login_url='/accounts/')
def editUser_view(request):
    context = {}
    currUser = request.user

    if not currUser.is_superuser:
        messages.add_message(request, messages.ERROR, 'Admin credentials are Wrong!')
        return redirect('accounts:login')

    if request.method == 'POST':
        source = request.POST.get('source')
        if source == 'home':
            userEmail = request.POST.get('email')
            userEmail = User.objects.filter(username = userEmail)
            if len(userEmail) == 0:
                messages.add_message(request, messages.ERROR, 'user does not exist!')
                return redirect('admin:home')
            context.update({
                'userEmail' : userEmail,
            })
        elif source == 'editUser':
            email = request.POST.get('email')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            isAdmin = request.POST.get('isAdmin')
            isActive = request.POST.get('isActive')
            
            try:
                user = User.objects.get(username = email)
                user.first_name = fname
                user.last_name = lname
                user.is_staff = isAdmin
                user.is_superuser = isAdmin
                user.is_active = isActive
                user.save()
                messages.add_message(request, messages.SUCCESS, 'User updated successfully')
                return redirect('admin:home')
            except :
                messages.add_message(request, messages.ERROR, 'Something went wrong!')
                return redirect('admin:home')
            
    return render(request, 'admin/editUser.html', context=context)

@login_required(login_url='/accounts/')
def editTariff_view(request):
    context = {}
    currUser = request.user

    if not currUser.is_superuser:
        messages.add_message(request, messages.ERROR, 'Admin credentials are Wrong!')
        return redirect('accounts:login')

    if request.method == 'POST':
        source = request.POST.get('source')
        if source == 'home':
            tariffID = request.POST.get('tariffID')
            tariffID = tblTariffs.objects.filter(tariffID = tariffID)
            if len(tariffID) == 0:
                messages.add_message(request, messages.ERROR, 'tariff data does not exist!')
                return redirect('admin:home')
            context.update({
                'tariffID' : tariffID,
            })
        elif source == 'editTariff':
            tariffID = request.POST.get('tariffID')
            slab1 = request.POST.get('slab1')
            slab2 = request.POST.get('slab2')
            slab3 = request.POST.get('slab3')
            singlePhMeterRent = request.POST.get('singlePhMeterRent')
            threePhMeterRent = request.POST.get('threePhMeterRent')
            TVFee = request.POST.get('TVFee')
            EDuty = request.POST.get('EDuty')
            GST = request.POST.get('GST')
            NJS = request.POST.get('NJS')
            FCS = request.POST.get('FCS')

            try:
                tariff = tblTariffs.objects.get(tariffID = tariffID)
                tariff.slab1Rate = slab1
                tariff.slab2Rate = slab2
                tariff.slab3Rate = slab3
                tariff.singlePhMeterRent = singlePhMeterRent
                tariff.threePhMeterRent = threePhMeterRent
                tariff.TVFee = TVFee
                tariff.EDuty = EDuty
                tariff.GST = GST
                tariff.NJS = NJS
                tariff.FCS = FCS
                tariff.save()
                messages.add_message(request, messages.SUCCESS, 'Tariff updated successfully')
                return redirect('admin:home')
            except :
                messages.add_message(request, messages.ERROR, 'Something went wrong!')
                return redirect('admin:home')

    return render(request, 'admin/editTariff.html', context=context)

@login_required(login_url='/accounts/')
def editFeeder_view(request):
    context = {}
    currUser = request.user
    fmt = "%Y-%m-%d"
    if not currUser.is_superuser:
        messages.add_message(request, messages.ERROR, 'Admin credentials are Wrong!')
        return redirect('accounts:login')

    if request.method == 'POST':
        source = request.POST.get('source')
        if source == 'home' or source == 'bill':
            name = request.POST.get('name')
            name = tblFeeders.objects.filter(name = name)
            if len(name) == 0:
                messages.add_message(request, messages.ERROR, 'feeder data does not exist!')
                return redirect('admin:home')
            context.update({
                'name' : name,
            })
        elif source == 'editFeeder':
            name = request.POST.get('name')
            div = request.POST.get('div')
            subDiv = request.POST.get('subDiv')
            readingDate = request.POST.get('readingDate')
            issueDate = request.POST.get('issueDate')

            readingDateValue = datetime.strptime(readingDate, fmt)
            issueDateValue = datetime.strptime(issueDate, fmt)
     
            try:
                feeder = tblFeeders.objects.get(name = name)
                feeder.div = div
                feeder.subDiv = subDiv
                feeder.readingDate = readingDate
                feeder.issueDate = issueDate
                feeder.save()
                messages.add_message(request, messages.SUCCESS, 'Feeder data updated successfully')
                return redirect('admin:home')
            except :
                messages.add_message(request, messages.ERROR, 'Something went wrong!')
                return redirect('admin:home')
    return render(request, 'admin/editFeeder.html', context=context)

@login_required(login_url='/accounts/')
def bill_view(request):
    context = {}
    currUser = request.user
    fmt = "%Y-%m-%d"

    if not currUser.is_superuser:
        messages.add_message(request, messages.ERROR, 'Admin credentials are Wrong!')
        return redirect('accounts:login')

    source = request.POST.get('source')
    name = request.POST.get('name')
    feeder = tblFeeders.objects.get(name = name)
    issueDate = feeder.issueDate
    readingDate = feeder.readingDate

    if source == 'badRecord':
        allUsers = User.objects.filter(username__in = request.POST.getlist('userEmail'))
        userMeters = tblMeters.objects.filter(id__in = request.POST.getlist('meterID'))
    else:
        allUsers = User.objects.filter(is_staff = False)
        userMeters = tblMeters.objects.filter(user__in = allUsers, feederName = name)
    
    allMeters = []
    for meter in userMeters:
        try:
            previousBill = tblBills.objects.filter(meterID = meter.id).latest('id').id
            previousBill = tblBills.objects.get(id = previousBill)
            latestReading = previousBill.currentReading
        except:
            latestReading = 0

        allMeters.append({
            'user': meter.user,
            'id': meter.id,
            'tariffID': meter.connectionType,
            'latestReading': latestReading,
            'meterType' : meter.meterType
            })
    
    if source == 'home':
        context.update({
            'allMeters' : allMeters,
            'feeder' : name,
            'readingDate' : readingDate,
            'issueDate' : issueDate
        })
        return render(request, 'admin/bill.html', context=context)
    else:
        # check if billMonth exists already, delete first 
        billingMonth = request.POST.get('billingMonth')
        currentReadingList = request.POST.getlist('currentReadingList')
        tariffs = tblTariffs.objects.values_list()
        tariff = {
            "C" : tariffs[0][1:],
            "I" : tariffs[1][1:],
            "R" : tariffs[2][1:]
        }
        slabs = {
            "R": [300, 700],
            "C": [500, 1000],
            "I": [1000, 3000]
        }

        issueDateValue = datetime.strptime(issueDate, fmt)
        dueDateValue = issueDateValue + timedelta(days=7)
        dueDate = datetime.strftime(dueDateValue, fmt)
        badRecord = []
        i = 0
        for i, meter in enumerate(allMeters):
            previousReading = meter['latestReading']
            tariffID = meter['tariffID']
            
            currentReading = currentReadingList[i]
            units = int(currentReading) - int(previousReading)
            if units < 0:
                badRecord.append({
                    'user':meter['user'],
                    'id': meter['id'],
                    'tariffID': tariffID,
                    'latestReading': previousReading,
                })
                context.update({
                    'has_error' : True,
                })
            else:
                slab1Rate, slab2Rate, slab3Rate, sPhaseRent, ThPhaseRent, TVFee, eDuty, GST, NJS, FCS = tariff[tariffID]
                slab1, slab2 = slabs[tariffID]

                if units <= slab1:
                    eCost = units * slab1Rate
                elif units <= slab2:
                    eCost = slab1 * slab1Rate + (units-slab1) * slab2Rate
                else:
                    eCost = slab2 * slab2Rate + (units-slab2) * slab3Rate
                
                if meter['meterType'] == "Single":
                    bill = sPhaseRent
                else:
                    bill = ThPhaseRent

                eDuty *= eCost/100
                NJS *= units
                FCS *= units
                GST *= (eCost + NJS + FCS)/100

                bill += eCost+eDuty+GST+NJS+FCS+TVFee

                newBill = tblBills(
                    previousReading = previousReading,
                    currentReading = currentReading,
                    units = units,
                    amount = bill,
                    status = 'UNPAID',
                    billingMonth = billingMonth,
                    meterID = tblMeters.objects.get(id = meter['id']),
                    tariffID = tblTariffs.objects.get(tariffID = tariffID),
                    dueDate = dueDate
                )
                newBill.save()
            i += 1

        try:
            if context['has_error']:
                context.update({
                    'badRecord' : badRecord,
                    'feeder' : name,
                    'readingDate' : readingDate,
                    'issueDate' : issueDate
                })
                messages.add_message(request, messages.ERROR, 'Incorrect Data Detected. Re-Submit the following Else it will be Discarded')
                return render(request, 'admin/bill.html', context=context)
        except:
            pass

    messages.add_message(request, messages.SUCCESS, 'All Bills Have Been Generated Successfully')
    return redirect('admin:home')