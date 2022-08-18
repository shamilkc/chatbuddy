
from email.message import Message
from multiprocessing import context
from pydoc_data.topics import topics
import re
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import is_valid_path
from .models import Room ,Topic, Messege
from .forms import roomForm,UserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def loginPage(request):
    page= 'login'

    if request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user doesnot exist')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"username or password not matching")

    context ={
        'page':page
    }
    return render(request,'base/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def regUser(request):
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
             messages.error(request,"an error occured")
    context ={
        'form':form
    }
    return render(request,'base/login.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics =Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messeges = Messege.objects.filter(Q(room__topic__name__icontains=q))
    context ={
        'rooms':rooms,
        'topic':topics,
        'room_count':room_count,
        'room_messeges':room_messeges,
    }
    return render(request,'base/home.html',context)


def room (request,pk):
    room = Room.objects.get(id=pk)
    room_messeges = room.messege_set.all().order_by('-created')
    participents = room.participents.all()

    if request.method =="POST":
        messege = Messege.objects.create(
            user =request.user, 
            room = room,
            body = request.POST.get('body')
        )
        room.participents.add(request.user)
        return redirect('room',pk=room.id)
    context={
        'room':room,
        'room_messeges':room_messeges,
        'participents':participents,
    }
    
    return render(request,'base/room.html',context)



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messeges = user.messege_set.all()
    topic = Topic.objects.all()
    context={
        'user':user,
        'rooms':rooms,
        'room_messeges':room_messeges,
        'topic':topic
    }
    return render(request,'base/profile.html',context)



@login_required(login_url='login')
def createRoom(request):
    form = roomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) 
        Room.objects.create(
            host = request.user,
            topic = topic,
            name=request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {
        'form':form,
        'topics':topics
    }
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = roomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("you are not allowed here!!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context ={
        'form':form,
        'topics':topics,
        'room':room
    }
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not allowed here!!!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessege(request,pk):
    messege = Messege.objects.get(id=pk)

    if request.user != messege.user:
        return HttpResponse("you are not allowed here!!!")
    if request.method == 'POST':
        messege.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':messege})

@login_required(login_url='login')
def updateUser(request):
    user =request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context ={
        'form':form
    }
    return render(request,'base/update-user.html',context)


def topic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics= Topic.objects.filter(name__icontains=q)
    context={
        'topics':topics,
        }
    return render(request,'base/topics.html',context)


def activitiesPage(request):
    room_messeges = Messege.objects.all()

    context={
        'room_messeges':room_messeges
        }
    return render(request,'base/activity.html',context)