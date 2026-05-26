from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Item, Category, Conversation
from .forms import SignUpUser, NewItemForm, EditItemForm, ConversationMessageForm

# Create your views here.

def index(request):
    query = request.GET.get('query', '')

    items = Item.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)

    if query:
        items = items.filter(name__icontains=query)

    if category_id:
        items = items.filter(category_id=category_id)

    context = {'items': items, 'categories': categories, 'category_id': int(category_id), 'query': query}
    return render(request, 'app/index.html', context)


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    context = {"item": item, "related_items": related_items}
    return render(request, 'app/detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
            form = SignUpUser()
    return render(request, 'app/signup.html', {'form': form})

def login_page(request):
    # Agarda biz login dan qashqari yana qanaqadir qoshimcha funksiya bajarmoqchi bolsak views da login_view yaratamiz. Bomasa django ozini default loginini ishlatgan yaxshi (tip 1)
    page = 'login'
    users = User.objects.all()

    if request.user.is_authenticated:
         return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exits")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password is incorrect")
    context = {'page': page, 'users': users}
    return render(request, 'app/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('detail', pk=item.id)
    else:
        form  = NewItemForm()  

    return render(request, 'app/form.html', {'form': form})    

@login_required
def edit(request, pk):
    item  = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('detail', pk=item.id)
    else:
        form  = EditItemForm(instance=item)  

    return render(request, 'app/form.html', {'form': form})    

# def search(request):
#     query = request.GET.get('query')
#     items = Item.objects.filter(is_sold=False)

#     if query:
#         items = items.filter(name__icontains=query)

#     return render(request, 'app/index.html', {
#         "items": items,
#         "query": query
#     })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('index')

# dashboard

@login_required
def dashboard_index(request):
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'app/dashboard.html', )

# Conversation

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user])

    if conversations:
        return redirect('inbox_detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'app/new.html', {'form': form})

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user])

    return render(request, 'app/inbox.html', {'conversations': conversations})

def inbox_detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            return redirect('inbox_detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'app/inbox_detail.html', {'conversation': conversation, 'form': form})