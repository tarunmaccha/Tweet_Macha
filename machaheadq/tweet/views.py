from django.shortcuts import get_object_or_404,redirect,render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import TweetForm, UserRegistrationForm
from django.http import JsonResponse
from django.db.models import Q  # For advanced filtering
from django.views.decorators.http import require_GET

# Create your views here.

def index(request):
    return render(request,'index.html') 
 
def tweet_list(request):
   tweets = Tweet.objects.all().order_by('-created_at')
   return render(request,'tweet_list.html', {'tweets':tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else :
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html',{'form':form}) 

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('tweet_list')
            else:
                print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def tweet_search(request):
    query = request.GET.get('q')
    if query:
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).values('id', 'text', 'user__username', 'photo')
    else:
        tweets = Tweet.objects.all().values('id', 'text', 'user__username', 'photo')
    
    # Build JSON response with photo URL handling
    tweets_list = []
    for tweet in tweets:
        tweets_list.append({
            'id': tweet['id'],
            'text': tweet['text'],
            'user': tweet['user__username'],
            'photo_url': tweet['photo'] if tweet['photo'] else None
        })

    return JsonResponse(tweets_list, safe=False)
from django.shortcuts import render

# Assuming you want to render a template for the tweet view
def tweet_view(request):
    # Your logic for handling the view (can be empty if just rendering a template)
    return render(request, 'index.html')  # Use the template you prefer
