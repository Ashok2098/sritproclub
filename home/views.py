from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re,string
# Create your views here.
def home(request):
    return render(request, 'home/home.html')
def about(request):
    return HttpResponse('This is Contact Page') 
def contact(request):
    return HttpResponse('This is Contact Page') 
def search(request):
    query = request.GET['query']
    if len(query)>100:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthors = Post.objects.filter(author__icontains=query)
        allPosts1 = allPostsTitle.union(allPostsContent)
        allPosts = allPosts1.union(allPostsAuthors)
    if allPosts.count()==0:
        messages.warning(request,'No search results found in blog. Please refine your query')
    params = {'allPosts': allPosts, 'query':query}
    return render(request,'home/search.html', params)
    #return HttpResponse('This is search page')

# This is validating UserName which should contain letters, numbers and underscores in between.
def valid(name):
    for character in (name):
        if name[0].isdigit():
            name='F'
            break 
        else:
            if character.isalnum() or character is ('_'):
                name='T'
            else:
                name='F'
    return name

# Validating authorized srit.ac.in emails
def validemail(email):
    x=re.findall('@srit.ac.in',email)
    if(len(x)==0):
        return 1
        return redirect('home')
    for i in x:
        if(i=='@srit.ac.in'):
            return 0
def handleSignup(request):
    if request.method == 'POST':
        # Getting the Post Parameters
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        # Checking the errorneous inputs
        if len(uname)>15:
            messages.error(request,'Username should be less than or equal to 15 characters')
            return redirect('home')
        if valid(uname)=='F':
            messages.error(request,'Username should not start with a number and shoud only allow letters, numbers and underscores')
            return redirect('home')
        if validemail(email):
            messages.error(request,'Only authorized people can signup for this account.')
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,'Passwords do not match to each other')
            return redirect('home')

        #Creating the User
        user = User.objects.create_user(uname,email,pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request,'Your Programmers Club account has been Successfully created')
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Getting the Post Parameters
        luname = request.POST['luname']
        lpassword = request.POST['lpassword']
        user = authenticate(username=luname,password=lpassword)
        if user is not None:
            login(request, user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('home')

    return HttpResponse('404 - Not Found')
def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logged Out.')
    return redirect('home')
    return HttpResponse('404 - Not Found')