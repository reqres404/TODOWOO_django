from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request,'todo/home.html')




def signupuser(request):
    if request.method == 'GET':    
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    #create a new user
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return  redirect('currenttodos')

            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Username has been already taken'})


        else:
        #password didn't matched
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'password didnt matched'})
        
def loginuser(request):
    if request.method == 'GET':    
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    #create a new user
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username and password did not matched'})
        else:
             login(request,user)
             return  redirect('currenttodos')

                

    


def currenttodos(request):
   
    todos =Todo.objects.filter(user = request.user,datecompleted__isnull =True)
    return render(request,'todo/currenttodos.html',{'todos':todos})


def createtodo(request):
    if request.method =='GET':
            return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        
        form = TodoForm(request.POST)
        newTodo = form.save(commit=False)
        newTodo.user = request.user
        newTodo.save()
        return redirect('currenttodos')
        
        



def logoutuser(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def viewtodo(request,todo_pk):
   
    todos =get_object_or_404(Todo,pk=todo_pk)
    return render(request,'todo/viewtodo.html',{'todos':todos})
