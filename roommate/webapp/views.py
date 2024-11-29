from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from .models import User_detail, Post, Favorites
from django.contrib import messages
import uuid
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models import Q

from django.utils.timezone import now
from django.http import JsonResponse
from datetime import timedelta
from datetime import date, datetime
import json
from django.core.files.base import ContentFile


# Create your views here.

#selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys

#webscraping
def scrape_accuweather(location):
    # Configure Selenium
    
    
    # Set up the driver
    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
    driver.set_window_size(200, 200)
    driver.get("https://www.accuweather.com/")

    try:
        # Locate the search bar and input the location
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-input')))
        search_box.clear()
        search_box.send_keys(location)
        search_box.send_keys(Keys.RETURN)

        # Wait for results page to load
        time.sleep(5)  # Adjust the delay as needed

        # Scrape Air Quality data
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/air-quality-index/28143")
        aqi = driver.find_element(By.ID, "air-quality-chart-legend-heading").text
        co2 = driver.find_element(By.ID, 'air-quality-chart-legend-overall').text

        # Scrape Health Activities data
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/sinus-weather/28143")
        sinus = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/asthma-weather/28143")
        asthma = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/allergies-weather/28143?name=dust-dander")
        allergies = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/mosquito-activity-weather/28143")
        mosquitoes = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/pest-weather/28143?name=indoor-pests")
        indoor_pests = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/pest-weather/28143?name=outdoor-pests")
        outdoor_pests = driver.find_element(By.ID, 'tooltipValueText').text
        
        driver.get(f"https://www.accuweather.com/en/bd/dhaka/{location}/cold-flu-weather/28143?name=flu")
        flu = driver.find_element(By.ID, 'tooltipValueText').text
        
       

        # Return the data
        data = {
            "aqi": aqi,
            "co2": co2,
            "sinus": sinus,
            "allergies": allergies,
            "mosquitoes": mosquitoes,
            "indoor_pests": indoor_pests,
            "outdoor_pests": outdoor_pests,
            "flu": flu,
            "asthma": asthma
        }
        #print(data)  # Check the data being returned
        return data

    except TimeoutException:
        return {"error": "Timeout while loading the page. Please try again."}

    finally:
        driver.quit()
        
def accu(request):
    data = {}
    if request.method == 'GET':
        location = request.GET.get('location')
        if location:
            data = scrape_accuweather(location)
            print(data)  # Check what data is being passed

    return render(request, "accu.html", {"data":data, "location":location})


def roommate(request):
    return render(request, 'roommate.html')

def signup(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
         # Validation
        if  User.objects.filter(username=username):
            messages.error(request,"This user already exists!")
            return redirect("signup")
        if  User.objects.filter(email=email):
            messages.error(request,"Username already exists!")
            return redirect("signup")
        if len(password)<6:
            messages.error(request,"Password is too short!")
            return redirect("signup")
        
        # Create User instance
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Generate unique user_id
        user_id = str(uuid.uuid4().int)[:12]  # Adjusted to 12 characters as per model
        
        # Create User_detail instance
        user_detail = User_detail(
            user_id=user_id,
            username=user,  # Pass the User instance, not the string
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        user_detail.save()
        
        messages.success(request,"Your account has been successfully created")
        return redirect('signin') 
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user) #login success
            request.session['username'] = username  # Store username in session
            return render(request,'home.html') #User Dashboard e jabe
        
        else:
            messages.error(request,"Invalid username or Password") 
            return redirect('signin')
    return render(request, 'signin.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def home(request):
    return render(request, 'home.html')

def add_post(request):
    if request.method == 'POST':
        username = request.session.get('username', None)  # Retrieve username from session
        if username:
            # Extract form data
            duration = request.POST.get('duration')
            tenant_type = request.POST.get('tenant_type')
            location = request.POST.get('location')
            bed = request.POST.get('bed')
            resident_type = request.POST.get('resident_type')
            description = request.POST.get('description')
            address = request.POST.get('address')
            rent = request.POST.get('rent')
            area = request.POST.get('area')  # Optional
            furnished = request.POST.get('furnished')
            security_deposit = request.POST.get('security_deposit')
            lease_term = request.POST.get('lease_term')

            # Utilities and Non-Included Bills
            utilities_included = request.POST.getlist('utilities')
            non_included_bills = request.POST.getlist('nonIncludedBills')

            uploaded_files = request.FILES.getlist('images')  # Name should match form field

            # Directory where images will be stored
            media_dir = os.path.join(settings.MEDIA_ROOT, 'posts')

            # Ensure the directory exists
            os.makedirs(media_dir, exist_ok=True)

            # Initialize file paths list to store uploaded image file paths
            file_paths = []

            # Process each uploaded file and save it
            for i, file in enumerate(uploaded_files):
                if i >= 4:  # Limit to 4 images
                    break

                # Define the file path within 'posts' directory
                file_name = file.name
                file_path = os.path.join('posts', file_name)

                # Save the file to the 'media/posts/' directory
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                file_paths.append(file_path)

            unique_id = str(uuid.uuid4())[:8]  # Truncate to first 8 characters
            post_id = f"{username}-{unique_id}"  # Concatenate username with unique identifier
            # Now save the post data, including images
            post = Post(
                post_id=post_id,
                duration=duration,
                tenant_type=tenant_type,
                location=location,
                bed=bed,
                resident_type=resident_type,
                description=description,
                address=address,
                rent=rent,
                area=area,
                furnished=furnished,
                security_deposit=security_deposit,
                lease_term=lease_term,
                utilities_included=utilities_included,
                non_included_bills=non_included_bills,
            )

            # Assign the uploaded image paths to the respective image fields
            for i, file_path in enumerate(file_paths):
                if i == 0:
                    post.image1 = file_path
                elif i == 1:
                    post.image2 = file_path
                elif i == 2:
                    post.image3 = file_path
                elif i == 3:
                    post.image4 = file_path

            # Save the post instance to the database
            post.save()

            # Redirect or render response after saving
            return redirect('my_post')  # Redirect to the home page or wherever needed


    return render(request, 'add_post.html')

def my_post(request):
    username = request.session.get('username', None)  # Retrieve username from session
    if username:
            rent_ads = Post.objects.filter(post_id__icontains= username)
            
    else:
            # Handle case where username is not found in session
            return HttpResponse("You haven't posted any ads yet.")
    return render(request, 'my_post.html',{'rent_ads': rent_ads})

def edit_post(request):
    
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_query = Post.objects.filter(post_id=post_id).first()

        if not post_query:
            return HttpResponse("Post not found", status=404)

        # Retrieve data from the form
        tenant_type = request.POST.get("tenantType")
        location = request.POST.get("location")
        resident_type = request.POST.get("resident")
        description = request.POST.get("description")
        utilities_included = request.POST.getlist("utilities")
        non_included_bills = request.POST.getlist("nonIncludedBills")
        address = request.POST.get("address")
        rent = request.POST.get("rent")
        area = request.POST.get("area")
        furnished = request.POST.get("furnished")
        security_deposit = request.POST.get("securityDeposit")
        lease_term = request.POST.get("leaseTerm")
        images = request.FILES.getlist("images")

        # Update the Post object
        post_query.tenant_type = tenant_type
        post_query.location = location
        post_query.resident_type = resident_type
        post_query.description = description
        post_query.utilities_included = utilities_included
        post_query.non_included_bills = non_included_bills
        post_query.address = address
        post_query.rent = rent
        post_query.area = area
        post_query.furnished = furnished
        post_query.security_deposit = security_deposit
        post_query.lease_term = lease_term

        if images:
            for i, image in enumerate(images[:4]):  # Only save up to 4 images
                setattr(post_query, f"image{i + 1}", image)

        post_query.save()
        messages.success(request, "Post updated successfully!")
        return redirect("my_post")  # Redirect to the post detail page

    # Handle GET requests
    post_id = request.GET.get("post_id")
    if not post_id:
        return HttpResponse("Post ID not provided", status=400)

    post_query = Post.objects.filter(post_id=post_id).first()
    if not post_query:
        return HttpResponse("Post not found", status=404)
    
    return render(request, 'edit_post.html',{"post": post_query})

def remove_post(request):
    post_id = request.GET.get('post_id')  # Use GET to fetch the post_id from the URL
    if post_id:
        # Retrieve the post by post_id or return a 404 error if not found
        post = get_object_or_404(Post, post_id=post_id)
        post.delete()
    return redirect('my_post')


def view_post(request):
    username = request.session.get('username', None)  # Retrieve username from session
    if username:
    # Assuming 'username' is the current user's username
        exclude_filter = Q(post_id__icontains=username)

        # Exclude posts with the username in 'post_id'
        rent = Post.objects.exclude(exclude_filter).order_by('entry_date')

        if request.method == "POST":
            tenant_type = request.POST.get('tenant_type')
            location = request.POST.get('location')
            resident_type = request.POST.get('resident_type')
            bed = request.POST.get('bed')
            price = request.POST.get('rent')
            
            # Build Q objects for each filter condition
            filters = Q()
            if location:
                filters &= Q(location__icontains=location)
            if resident_type:
                filters &= Q(resident_type__icontains=resident_type)
            if bed:
                filters &= Q(bed=bed)
            if tenant_type:
                filters &= Q(tenant_type=tenant_type)
            if price:
                filters &= Q(price__lte=rent)
            
            else:
                rent = rent.filter(filters)  # Applying additional filters to the previous query
    else:
        return HttpResponse("You haven't posted any ads yet.")  
    return render(request, 'view_post.html', {'rent': rent})

def maleshared(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent = Post.objects.exclude(exclude_filter).filter(Q(tenant_type='Male') & Q(bed__icontains='Bed')).values()
    return render(request, 'view_post.html',{'rent':rent})

def femaleshared(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent = Post.objects.exclude(exclude_filter).filter(Q(tenant_type='Female') & Q(bed__icontains='Bed')).values()
    return render(request, 'view_post.html',{'rent':rent})

def twobhk(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent=Post.objects.exclude(exclude_filter).filter(bed__icontains='2 Rooms').values()
    return render(request, 'view_post.html',{'rent':rent})

def threebhk(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent=Post.objects.exclude(exclude_filter).filter(bed__icontains='3 Rooms').values()
    return render(request, 'view_post.html',{'rent':rent})

def malehostel(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent = Post.objects.exclude(exclude_filter).filter(resident_type='Male Hostel').values()
    return render(request, 'view_post.html',{'rent':rent})

def femalehostel(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent = Post.objects.exclude(exclude_filter).filter(resident_type='Female Hostel').values()
    return render(request, 'view_post.html',{'rent':rent})

def familysub(request): 
    username = request.session.get('username', None)  
    if username:
        exclude_filter = Q(post_id__icontains=username) 
        rent = Post.objects.exclude(exclude_filter).filter(Q(tenant_type='Family') & Q(bed__icontains='Room')).values()
    return render(request, 'view_post.html',{'rent':rent})

def view_details(request):
    post_id = request.GET.get('post_id')
    rent = Post.objects.filter(post_id=post_id)
    return render(request, 'view_details.html',{'rent': rent})

def favorites(request):
    username = request.session.get('username', None)  # Retrieve username from session
    if username:
        try:
            # Get the user object corresponding to the username
            user = User.objects.get(username=username)
            
            # Filter favorites for this user
            rent = Favorites.objects.select_related('post_id').filter(username=user) #select_related for the foreign key
        except User.DoesNotExist:
            return HttpResponse("Invalid user session. Please log in again.")
    else:
        return HttpResponse("You haven't posted any ads yet.") 
    
    return render(request, 'favorites.html', {'rent': rent} )

def add_fav(request):
    post_id = request.GET.get('post_id')  # Get the post_id from the request
    username = request.session.get('username', None)
    referer_url = request.META.get('HTTP_REFERER', '/')  # Get the previous page URL

    # Get the user instance based on the session username
    user_instance = User.objects.filter(username=username).first()
    if not user_instance:
        messages.error(request, 'User not found.')
        return redirect('login')  # Redirect to the login page if user doesn't exist

    # Try to get the post based on post_id
    rent = Post.objects.filter(post_id=post_id).first()
    if not rent:
        messages.error(request, 'Property not found.')
        return redirect(referer_url)  # If post doesn't exist, return to the previous page

    # Check if the property is already in the user's favorites
    if Favorites.objects.filter(username=user_instance, post_id=rent).exists():
        messages.warning(request, 'This property is already in your favorites.')
    else:
        # Add to favorites if not already added
        Favorites.objects.create(
            username=user_instance,  # Use user instance here
            post_id=rent,
            tenant_type=rent.tenant_type,
            location=rent.location,
            bed=rent.bed,
            resident_type=rent.resident_type,
            address=rent.address,
            rent=rent.rent,
            area=rent.area,
            furnished=rent.furnished,
            security_deposit=rent.security_deposit,
            lease_term=rent.lease_term,
            utilities_included=rent.utilities_included,
            non_included_bills=rent.non_included_bills,
            image1=rent.image1,
        )
        messages.success(request, 'Post added to your favorites!')

    return redirect(referer_url)  # Redirect back to the previous page

def remove_fav(request):
    post_id = request.GET.get('post_id')  # Use GET to fetch the post_id from the URL
    if post_id:
        # Retrieve all Favorites matching the post_id
        favorites = Favorites.objects.filter(post_id__post_id=post_id)
        if favorites.exists():
            favorites.delete()  # Delete all matching objects
        messages.success(request, 'Post successfully removed from your favorites!')        
    return redirect('favorites')  # Redirect to the favorites page

def profile(request):
    user_detail = User_detail.objects.filter(username=request.user).first()
        
    if not user_detail:
        return HttpResponse("User profile not found", status=404)

    if request.method == "POST":
        # Debugging: Log the POST data
        print("POST data:", request.POST)

        # Retrieve updated data from the form
        first_name = request.POST.get("first_name", user_detail.first_name)
        last_name = request.POST.get("last_name", user_detail.last_name)
        phone = request.POST.get("phone", user_detail.phone)
        address = request.POST.get("address", user_detail.address)
        gender = request.POST.get("gender", user_detail.gender)
        date_of_birth = request.POST.get("date_of_birth", user_detail.date_of_birth)

        # Debugging: Ensure values are being updated correctly
        print("Updating values:", first_name, last_name, phone, address, gender, date_of_birth)

        # Update the User_detail object
        user_detail.first_name = first_name
        user_detail.last_name = last_name
        user_detail.phone = phone
        user_detail.address = address
        user_detail.gender = gender
        user_detail.date_of_birth = date_of_birth

        # Save the updated profile details
        user_detail.save()

        # Show success message
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")  # Redirect back to the profile page

    # Render the profile page for GET requests
    return render(request, "profile.html", {"user_detail": user_detail})

def change_password(request):
    if request.method == "POST":
        # Get form data
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Get the logged-in user
        user = request.user

        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, "Current password is incorrect.")
            return redirect("profile")

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("profile")

        # Check the password length
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("profile")

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return redirect("profile")

    # If the request is not POST, return a 404 or redirect
    return redirect("profile")

def policy(request):
    return render(request, "policy.html")

def contribute(request):
    return render(request, "contribute.html")

def about_us(request):
    return render(request, "about_us.html")

