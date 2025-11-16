from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegrestrationForm
from django.shortcuts import get_object_or_404,redirect # Fetches an object from the database or returns a 404 error if it doesn’t exist.
from django.contrib.auth.decorators import login_required #login_required is used to restrict access to a view so that only authenticated (logged-in) users can access it.
from django.contrib.auth import login
from django.http import Http404
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend

def logout(request):
    return render(request,"logged_out.html")

def index(request):
    return render(request,"index.html")

from django.contrib.auth.decorators import login_required

def tweet_list(request):
    if request.user.is_authenticated:
        # Show all tweets except the current user's tweets
        tweets = Tweet.objects.exclude(user=request.user).order_by('-updated_at')
    else:
        # Show all tweets for anonymous users
        tweets = Tweet.objects.all().order_by('-updated_at')
    
    return render(request, 'tweet_list.html', {'tweets': tweets, 'user': request.user})


@login_required
def tweet_create(request):
    if request.method=="POST":
        form =TweetForm(request.POST,request.FILES) #→ builds the form with submitted data (including uploaded images).
        if form.is_valid():                          #checks if the data respects the model rules (max_length, required fields, etc).
            tweet=form.save(commit=False)            #creates a Tweet object but doesn’t save to DB yet (lets you modify before saving).
            tweet.user=request.user                  #This way, the currently logged-in user is linked to the tweet.
            tweet.save()
            return redirect("tweet_list")              #→ sends the user to the list view after creation.
    else:
        form=TweetForm()
    return render(request,"tweet_form.html",{"form":form})




@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk= tweet_id,user=request.user)
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES,instance=tweet)  #tells the form that you’re editing an existing Tweet object, not creating a new one.
        if form.is_valid():                          #checks if the data respects the model rules (max_length, required fields, etc).
            tweet=form.save(commit=False)            #creates a Tweet object but doesn’t save to DB yet (lets you modify before saving).
            tweet.user=request.user                  #This way, the currently logged-in user is linked to the tweet.
            tweet.save()
            return redirect("tweet_list")   
    else:
        form=TweetForm(instance=tweet)
    return render(request,"tweet_form.html",{"form":form})





@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request,"tweet_confirm_delete.html",{"tweet":tweet})


from django.core.mail import send_mail
from .models import EmailVerificationToken, UserProfile
from django.urls import reverse

def register(request):
    if request.method == "POST":
        form = UserRegrestrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create empty profile
            UserProfile.objects.create(user=user)

            # Create verification token
            token_obj = EmailVerificationToken.objects.create(user=user)

           
            verification_link = request.build_absolute_uri(
                reverse("verify_email", args=[token_obj.token])
            )

            # Send verification mail
            send_mail(
                subject="Verify your Email - TweetShare",
                message=f"Click the link to verify your email:\n{verification_link}",
                from_email="yourgmail@gmail.com",
                recipient_list=[user.email],
            )

            return render(request, "email_sent.html", {"email": user.email})

    else:
        form = UserRegrestrationForm()

    return render(request, 'registration/register.html', {'form': form})



from django.shortcuts import render, redirect
from .models import EmailVerificationToken, UserProfile

def verify_email(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        return render(request, "invalid_token.html")

    # Mark user as verified
    profile = UserProfile.objects.get(user=token_obj.user)
    profile.is_verified = True
    profile.save()

    # Delete token
    token_obj.delete()

    return render(request, "email_verified.html")


### Step-by-Step Flow of Django User Registration (Hinglish me samjha hua)

# 1.                                                       **User register page open karta hai (GET request hoti hai)**
#    * Jab user registration page open karta hai, tab browser Django server ko **GET request** bhejta hai.
#    * Django code check karta hai:
#      ```python
#      if request.method == "POST":
#      ```
#      Ye condition **False** hoti hai, kyunki abhi form submit nahi hua hai.

#2. **`else` block run hota hai**
#    * Django ek **empty form** banata hai:
#      ```python
#      form = UserRegrestrationForm()
#      ```
#    * Ye blank form user ko HTML page par dikhaya jata hai taaki wo apna data fill kare.

#3. **User form fill karke “Register” button dabata hai**

#    * Ab jab user form submit karta hai, to browser ek **POST request** bhejta hai Django ko, jisme user ka data hota hai (username, password, etc.).

# 4. **Django ko POST request milti hai**

#    * Ab ye condition **True** hoti hai:

#      ```python
#      if request.method == "POST":
#      ```
#    * Django user ke submit kiye hue data ko form me daal deta hai:

#      ```python
#      form = UserRegrestrationForm(request.POST)
#      ```

# 5. **Form validation hoti hai**

#    * Django check karta hai:

#      ```python
#      if form.is_valid():
#      ```
#    * Validation me ye sab check hota hai:
#      * Kya sab required fields fill hui hain?
#      * Password1 aur Password2 same hain ya nahi?
#      * Username already exist karta hai ya nahi?

# 6. **Agar form valid hai**

#    * To Django ek **naya user object** create karta hai:

#      ```python
#      user = form.save()
#      ```
#    * Ye user ab database me save ho jata hai.

# 7. **User ko login karaya jata hai**

#    * Form valid hone ke baad Django use turant login karata hai:

#      ```python
#      login(request, user)
#      ```
#    * `login()` ka kaam hai user session create karna taaki wo logged-in rahe.

# 8. **User ko kisi page par redirect kar diya jata hai (jaise home page)**

#    * Example:

#      ```python
#      return redirect('home')
#      ```
#    * Ab user successful registration ke baad home page par pahunch jata hai.

# 9. **Agar form invalid hai**

#    * Django wapas wahi form render karta hai, jisme error messages show hote hain (jaise “username already exists” ya “passwords don’t match”).

# **In short:**
# ➡️ GET → blank form dikhao
# ➡️ POST → form validate karo
# ➡️ Valid → user banao + login karao + redirect karo
# ➡️ Invalid → error ke sath form wapas dikhao




from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def create_profile(request):
    # Check if user already has a profile
    try:
        # If profile exists, redirect to profile detail
        existing_profile = UserProfile.objects.get(user=request.user)
        return redirect('profile_detail', username=request.user.username)
    except UserProfile.DoesNotExist:
        # If no profile exists, proceed with creation
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('profile_detail', username=request.user.username)
        else:
            form = UserProfileForm()
        
        return render(request, 'create_profile.html', {'form': form})
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def profile_detail(request, username):
    try:
        profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        # If profile doesn't exist and it's the current user, redirect to create profile
        if request.user.username == username:
            return redirect('create_profile')
        else:
            # If it's another user's profile that doesn't exist, show 404
            raise Http404("Profile does not exist")
    
    profile_user = profile.user
    following_profiles = UserProfile.objects.filter(followers=profile_user)
    following_users = [p.user for p in following_profiles]
    
    # Get all tweets from the profile user
    all_tweets = Tweet.objects.filter(user=profile_user).order_by('-updated_at')
    tweets_count = all_tweets.count()
    
    # Only show first 4 tweets initially
    tweets_display = all_tweets[:4]

    return render(request, 'profile_detail.html', {
        'profile': profile,
        'following': following_users,
        'profile_user': profile_user,
        'tweets': tweets_display,
        'all_tweets_count': tweets_count,
    })

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if tweet.user_has_liked(request.user):
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    
    # Return to the same page
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    user_profile = user_to_follow.userprofile

    if request.user != user_to_follow:
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
        else:
            user_profile.followers.add(request.user)

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = profile_user.userprofile.followers.all()  # all users who follow this person
    return render(request, 'followers_list.html', {
        'profile_user': profile_user,
        'followers': followers
    })
@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    
    # CORRECT: Get all users that this user is following
    # This means: find all UserProfiles where this user is in their followers list
    following_profiles = UserProfile.objects.filter(followers=user)
    following_users = [profile.user for profile in following_profiles]
    
    return render(request, 'following_list.html', {
        'following': following_users,
        'profile_user': user
    })







from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def edit_profile(request):
    # Get the profile of the logged-in user
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Bind form with POST data and files (image)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        # Display form pre-filled with current profile data
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Tweet, UserProfile

@login_required
def following_feed(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Get all profiles that the current user is following
    following_profiles = UserProfile.objects.filter(followers=request.user)

    # Extract actual User objects from those profiles
    following_users = [profile.user for profile in following_profiles]

    # Get tweets by users that the current user follows
    tweets = Tweet.objects.filter(user__in=following_users).order_by('-updated_at')

    return render(request, 'following_feed.html', {'tweets': tweets})



@login_required
def my_feed(request):
    # Fetch tweets created by the currently logged-in user
    tweets = Tweet.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'my_feed.html', {'tweets': tweets})


def search_user(request):
    query = request.GET.get("q")
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, "search.html", {"users": users, "query": query})



from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        auth_logout(request)   # log out first
        user.delete()          # delete the user account
        return redirect("home")  # redirect after deleting
    
    return render(request, "delete_account_confirm.html")
