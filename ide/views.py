from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import registerform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from .models import *
from .decorators import allowed_users
import csv,io
from datetime import date 
import pandas as pd


def lockout(request, credentials, *args, **kwargs):
    return render(request, "ide/lockout.html")
    
def home(request):
    return render(request, "ide/index.html")

def about(request):
    return render(request, "ide/about.html")

def contact(request):
    return render(request, "ide/contact.html")

@login_required(login_url='/alogin')
def allocate(request):
    if request.method=="POST":
        file1=request.FILES['file1']
        file2=request.FILES['file2']
        file3=request.FILES['file3']
        schedule=pd.read_csv(file2)
        faculty_table=pd.read_csv(file3)
        room=pd.read_csv(file1)
        
        exam_name=schedule.iloc[:,-1]
        exam_name=exam_name[0]
        schedule=schedule.drop('exam_name',axis=1)

        faculty_room=pd.DataFrame()
        faculty_room['Faculty']=0
        faculty_room['date']=""
        faculty_room['slot1']="Free"
        faculty_room['slot2']="Free"
        faculty_room['slot3']="Free"
        faculty_room['slot4']="Free"
        faculty_room['slot5']="Free"
        faculty_room['slot6']="Free"
        faculty_room['slot7']="Free"
        faculty_room['slot8']="Free"

        faculty_table['slot1']="Free"
        faculty_table['slot2']="Free"
        faculty_table['slot3']="Free"
        faculty_table['slot4']="Free"
        faculty_table['slot5']="Free"
        faculty_table['slot6']="Free"
        faculty_table['slot7']="Free"
        faculty_table['slot8']="Free"

        faculty_table=faculty_table.sort_values('remaining_work_hour',ascending=False).reset_index().drop('index',axis=1)
        group_schedule=schedule.groupby('date')
        itr_fac=0
        itr_facroom=0
        flag_possible=0
        zero_ptr=0
        round_robin=3
        room_size=len(room)
        fac_size=len(faculty_table)
        for i in (group_schedule.groups.keys()):
            df=group_schedule.get_group(i)
            itr_room=0
            flag_possible=0
            flag_count=0
            flag_free=0
            room['slot1']="Free"
            room['slot2']="Free"
            room['slot3']="Free"
            room['slot4']="Free"
            room['slot5']="Free"
            room['slot6']="Free"
            room['slot7']="Free"
            room['slot8']="Free"
            for j in range(len(df)):
                itr_fac=0
                for k in range(df.iloc[j,3]):
                    itr_room=0
                    flag_count=0
                    start_l=df.iloc[j,1]
                    end_l=df.iloc[j,2]+1
                    if(start_l>=1 and end_l<=8):
                        while(flag_count<room_size):
                            flag_free=0
                            for l in range(start_l,end_l):
                                if(room.iloc[itr_room,l]!='Free'):
                                    flag_free=1
                                    break
                            if(flag_free==0):
                                break
                            flag_count+=1
                            itr_room=(itr_room+1)%room_size
                        if(flag_count<room_size and flag_free==0):
                            new_row=[]
                            new_row.append(-1)
                            new_row.append(i)
                            for l in range(1,9):
                                if(l>=start_l and l<end_l):
                                    room.iloc[itr_room,l]='Exam'
                                    new_row.append(room.iloc[itr_room,0])
                                else:
                                    new_row.append('Free')
                            faculty_room.loc[len(faculty_room.index)]=new_row
                        else:
                            flag_possible=1
                    else:
                        flag_possible=1
                if(flag_possible==1):
                    break
                else:
                    faculty_table['slot1']="Free"
                    faculty_table['slot2']="Free"
                    faculty_table['slot3']="Free"
                    faculty_table['slot4']="Free"
                    faculty_table['slot5']="Free"
                    faculty_table['slot6']="Free"
                    faculty_table['slot7']="Free"
                    faculty_table['slot8']="Free"
                    while(itr_facroom<len(faculty_room)):
                        flag_count=0
                        while(flag_count<fac_size):
                            flag_alloted=0
                            start_slot=0
                            end_slot=0
                            count_slot=0
                            flag_slot=0
                            for itr_slot in range(2,10):
                                if(faculty_room.iloc[itr_facroom,itr_slot]!='Free'):
                                    if(start_slot==0):
                                        start_slot=itr_slot
                                    end_slot=itr_slot
                                    count_slot+=1
                            end_slot+=1
                            #print(itr_fac,faculty_table.iloc[itr_fac,3],count_slot)
                            if(faculty_table.iloc[itr_fac,3]>=count_slot):
                                for itr_slot in range(start_slot+2,end_slot+2):
                                    if(faculty_table.iloc[itr_fac,itr_slot]!='Free'):
                                        flag_slot=1
                                        break
                                if(flag_slot==0):
                                    faculty_table.iloc[itr_fac,3]-=count_slot
                                    faculty_room.iloc[itr_facroom,0]=faculty_table.iloc[itr_fac,1]
                                    for itr_slot in range(start_slot,end_slot):
                                        if(faculty_room.iloc[itr_facroom,itr_slot]!='Free'):
                                            faculty_table.iloc[itr_fac,itr_slot+2]=faculty_room.iloc[itr_facroom,itr_slot]
                                            flag_alloted=1
                                #print(pd.DataFrame(faculty_table),pd.DataFrame(faculty_room))
                            flag_count+=1
                            itr_fac=(itr_fac+1)%fac_size
                            if(flag_alloted==1):
                                break
                        if(faculty_room.iloc[itr_facroom,itr_slot]==-1):
                            flag_id=1
                            break
                        itr_facroom+=1

        #faculty_room

        dict_final_schedule={"Faculty":[0],"class_room":['A101'],"date":['19-02-2001'],"start_slot":[1],"end_slot":[3],"exam_name":['P1'],"request_status":['']}
        final_schedule=pd.DataFrame(dict_final_schedule)
        for i in range(len(faculty_room)):
            new_row=[]
            start_slot=0
            end_slot=0
            new_row.append(faculty_room.iloc[i,0])
            room=""
            for j in range(2,len(faculty_room.columns)):
                if(faculty_room.iloc[i,j]!='Free'):
                    if(start_slot==0):
                        room=faculty_room.iloc[i,j]
                        start_slot=j-1
                    end_slot=j-1
            new_row.append(room)
            new_row.append(faculty_room.iloc[i,1])
            new_row.append(start_slot)
            new_row.append(end_slot)
            new_row.append(exam_name)
            new_row.append("Request")
            final_schedule.loc[len(final_schedule.index)]=new_row
        final_schedule=final_schedule.drop(0)
        final_schedule.to_csv('final_schedule.csv',index=False)
        faculty_room.to_csv('faculty_room.csv',index=False)
        if flag_possible == 1:
            messages.info(request, 'Rejected')
        else:
            messages.info(request, 'Allocated Successfully')
        return render(request, "ide/adminhomepage-allocate.html")
    else:
        return render(request, "ide/adminhomepage-allocate.html")

@login_required(login_url='/alogin')
def adminreschedule(request):
    if request.method=="POST":
        file1=request.FILES['file1']
        file2=request.FILES['file2']
        file3=request.FILES['file3']
        requests=pd.read_csv(file1)
        faculty_table=pd.read_csv(file2)
        faculty_room=pd.read_csv(file3)

        requests['accept']='Accept'

        requests=requests.sort_values(['date','start_slot','end_slot']).reset_index().drop('index',axis=1)
        faculty_room['request_status']='Request'
        requests['length']=0
        for i in range(len(requests)):
            df=faculty_room.loc[faculty_room['date']==requests.iloc[i,2]]
            requests.iloc[i,-1]=df['Faculty'].nunique()
        requests=requests.sort_values(['length','start_slot','end_slot'],ascending=[False,True,True]).reset_index().drop(['index','length'],axis=1)

        itr_fac=0
        fac_size=len(faculty_table)
        group_faculty_room=faculty_room.groupby('Faculty')
        for i in range(len(requests)):
            flag_count=0
            flagger=0
            while(flag_count<fac_size):
                flagger=0
                if faculty_table.iloc[itr_fac,3]<requests.iloc[i,4]-requests.iloc[i,3]+1:
                    flag_count+=1
                    itr_fac=(itr_fac+1)%fac_size
                    continue
                if faculty_table.iloc[itr_fac,1] not in (group_faculty_room.groups.keys()):      
                    break  
                gdf=group_faculty_room.get_group(faculty_table.iloc[itr_fac,1])
                gdf=gdf.loc[gdf['date']==requests.iloc[i,2]]
                for j in range(len(gdf)):
                    if(gdf.iloc[j,3]>=requests.iloc[i,3] or gdf.iloc[j,4]<=requests.iloc[i,4]):
                        flagger=1
                        break
                if(flagger==0):
                    break    
                flag_count+=1
                itr_fac=(itr_fac+1)%fac_size
            if(flag_count<fac_size and flagger==0):
                for j in range(len(faculty_room)):
                    if((faculty_room.iloc[j,0]==requests.iloc[i,0] and faculty_room.iloc[j,1]==requests.iloc[i,1]) and (faculty_room.iloc[j,2]==requests.iloc[i,2] and faculty_room.iloc[j,3]==requests.iloc[i,3]) and (faculty_room.iloc[j,4]==requests.iloc[i,4] and faculty_room.iloc[j,5]==requests.iloc[i,5])):        
                        faculty_table.iloc[itr_fac,3]-=requests.iloc[i,4]-requests.iloc[i,3]+1
                        faculty_room.iloc[j,6]="Accept"
                        faculty_table.iloc[requests.iloc[i,0]-1,3]+=requests.iloc[i,4]-requests.iloc[i,3]+1
                        faculty_room.iloc[j,0]=faculty_table.iloc[itr_fac,1]
                        requests.iloc[i,0]=faculty_table.iloc[itr_fac,1]
                        requests.iloc[i,6]='Accept'
                        break
            elif(flag_count>=fac_size or flag_done!=1):
                requests.iloc[i,6]='Rejected'
                for j in range(len(faculty_room)):
                    if((faculty_room.iloc[j,0]==requests.iloc[i,0] and faculty_room.iloc[j,1]==requests.iloc[i,1]) and (faculty_room.iloc[j,2]==requests.iloc[i,2] and faculty_room.iloc[j,3]==requests.iloc[i,3]) and (faculty_room.iloc[j,4]==requests.iloc[i,4] and faculty_room.iloc[j,5]==requests.iloc[i,5])):        
                        faculty_room.iloc[j,6]="Rejected"
                        break
        dict_final_schedule={'Faculty':[0],'date':['11-06-2021'],'slot1':['Free'],'slot2':['Free'],'slot3':['Free'],'slot4':['Free'],'slot5':['Free'],'slot6':['Free'],'slot7':['Free'],'slot8':['Free']}
        final_schedule=pd.DataFrame(dict_final_schedule)
        for i in range(len(faculty_room)):
            new_row=[]
            new_row.append(faculty_room.iloc[i,0])
            new_row.append(faculty_room.iloc[i,2])
            status="Reschedule"
            for j in range(1,9):
                if j>=faculty_room.iloc[i,3] and j<=faculty_room.iloc[i,4]+1:
                    new_row.append(faculty_room.iloc[i,1])
                else:
                    new_row.append("Free")
        final_schedule.loc[len(final_schedule.index)]=new_row
        final_schedule=final_schedule.drop(0)
        final_schedule.to_csv('faculty_room.csv')
        faculty_room.to_csv('final_schedule.csv')
        messages.info(request, 'Successfully Rescheduled')
        return render(request, "ide/adminhomepage-reschedule.html") 
    else:
        context = {}
        nextday=str(date.today().year)+"-"+str(date.today().month)+"-"+str(date.today().day)
        nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
        context["data"] = Time_Table1.objects.all().filter(request_status='Accept').filter(date__range=[nextday,nextyear])
        return render(request, "ide/adminhomepage-reschedule.html")    

@login_required(login_url='/alogin')
def ahome(request):
    return render(request, "ide/adminhomepage.html")

@login_required(login_url='/flogin')
def fhome(request):
    return render(request, "ide/facultyhomepage.html")

def registeruser(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        form = registerform()
        if request.method == 'POST':
            form = registerform(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                messages.success(request, 'Account Created Successfully')
                return HttpResponseRedirect('/login/')
        context = {'form': form,  'messages':messages}
        return render(request, "ide/register.html", context)


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/index')


def userlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/fhome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/fhome')
            else:
                messages.info(request, 'Username or Password is Incorrect')
        context = {}
        return render(request, "ide/facultylogin.html", context)

def adminlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/ahome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/ahome')
            else:
                messages.info(request, 'Username or Password is Incorrect')
        context = {}
        return render(request, "ide/adminlogin.html", context)

def exam_upload(request):
    if request.method=='GET':
        return render(request,"ide/exam_upload.html")
    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,"This is not a csv file")
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar='|'):
        _,created = Time_Table1.objects.update_or_create(
            Faculty=User.objects.get(id=column[0]),
            class_room=column[1],
            date=column[2],
            start_slot=column[3],
            end_slot=column[4],
            exam_name=column[5],
            request_status=column[6],
        )
    context = {}
    return render(request,"ide/exam_upload.html",context)

def timetable_upload(request):
    if request.method=='GET':
        return render(request,"ide/timetable_upload.html")
    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request,"This is not a csv file")
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar='|'):
        print(column[0])
        _,created = Faculty_Table.objects.update_or_create(
            Faculty=User.objects.get(id=column[0]),
            date=column[1],
            slot1=column[2],
            slot2=column[3],
            slot3=column[4],
            slot4=column[5],
            slot5=column[6],
            slot6=column[7],
            slot7=column[8],
            slot8=column[9],
        )
    context = {}
    return render(request,"ide/timetable_upload.html",context)
        
@login_required(login_url='/flogin')
def ptimetable(request):
    context = {}
    context["data"] = Faculty_Table.objects.all().filter(Faculty=request.user)
    return render(request, "ide/facultyhomepage-schedule.html", context)
    
@login_required(login_url='/flogin')
def pexam(request):
    context = {}
    nextday=str(date.today().year)+"-"+str(date.today().month)+"-"+str(date.today().day+2)
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(Faculty=request.user).filter(date__range=[nextday,nextyear]).filter(request_status='Request')
    return render(request, "ide/facultyhomepage-reschedule.html", context)

@login_required(login_url='/flogin')
def pexam1(request,id):
    context = {}
    nextday=str(date.today().year)+"-"+str(date.today().month)+"-"+str(date.today().day+2)
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(Faculty=request.user).filter(date__range=[nextday,nextyear]).filter(request_status='Request')
    data1= Time_Table1.objects.get(pk=id)
    data1.request_status='Accept'
    data1.save()
    return render(request, "ide/facultyhomepage-reschedule.html", context)

@login_required(login_url='/flogin')
def pnot(request):
    context = {}
    nextday=str(date.today().year)+"-"+str(date.today().month)+"-"+str(date.today().day+2)
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(request_status='Accept').filter(date__range=[nextday,nextyear])
    return render(request, "ide/facultyhomepage-notifications.html", context)

@login_required(login_url='/flogin')
def pnot1(request,id):
    context = {}
    nextday=str(date.today().year)+"-"+str(date.today().month)+"-"+str(date.today().day+2)
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(request_status='Accept').filter(date__range=[nextday,nextyear])
    data2=Time_Table1.objects.filter(Faculty=request.user)
    data1= Time_Table1.objects.get(pk=id)
    c=0
    if request.user == data1.Faculty:
        data1.Faculty=request.user
        data1.request_status='Request'
        data1.save()
    else:
        for i in data2:
            if(i.date==data1.date and i.start_slot==data1.start_slot):
                c+=1
    if(c==0):
        data1.Faculty=request.user
        data1.request_status='Request'
        data1.save()
    else:
        messages.info(request, 'You Already have an exam')
    return render(request, "ide/facultyhomepage-notifications.html", context)

@login_required(login_url='/alogin')
def apnot(request):
    context = {}
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(request_status='Accept').filter(date__range=[date.today(),nextyear])
    return render(request, "ide/adminhomepage-notifications.html", context)

@login_required(login_url='/alogin')
def apnot1(request,id):
    context = {}
    nextyear=str(date.today().year+1)+"-"+str(date.today().month)+"-"+str(date.today().day)
    context["data"] = Time_Table1.objects.all().filter(request_status='Accept').filter(date__range=[date.today(),nextyear])
    data1= Time_Table1.objects.get(pk=id)
    data1.request_status='Request'
    data1.save()
    return render(request, "ide/adminhomepage-notifications.html", context)




