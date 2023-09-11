from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from django.utils import timezone
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
import uuid
from django.conf import settings
from django.core.mail import send_mail

def send_email_after_reg(email, token):
    subject = "TaskPedia, Verify Your Email"
    messages = f'click this link to verify your email address http://127.0.0.1:8000/account-verify/{token}'
    from_mail = settings.EMAIL_HOST_USER
    reciepent_list = [email]
    print(messages)
    send_mail(subject, messages, from_mail, reciepent_list)

def account_verify(request, token):
    email_verify = EmailVerify.objects.filter(token=token).first()
    email_verify.is_verified = True
    email_verify.save()
    messages.success(request, 'Your Account Verified Succefully, You Can Login Now')
    return redirect('sign-in')

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'dashboard/registration.html', {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
    
            new_user = User(username=username,  email=email, is_student=True )
            new_user.set_password(password1)
            new_user.save()
            token = uuid.uuid4()
            email_verify = EmailVerify(user=new_user, token=token)
            email_verify.save()
            send_email_after_reg(new_user.email, token)
            messages.success(request, 'Your Account Created Succefully, To Verify Your Account Please Check Your Email (please check spam folder also)' )
            return redirect('registration')

        return render(request, 'dashboard/registration.html', {'form':form})
    

class LectureRegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'dashboard/registration.html', {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
    
            new_user = User(username=username,  email=email, is_lecture=True )
            new_user.set_password(password1)
            new_user.save()
            token = uuid.uuid4()
            email_verify = EmailVerify(user=new_user, token=token)
            email_verify.save()
            send_email_after_reg(new_user.email, token)
            messages.success(request, 'Your Account Created Succefully, To Verify Your Account Please Check Your Email (please check spam folder also)' )
            return redirect('registration')

        return render(request, 'dashboard/registration.html', {'form':form})
    

class SignInView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'dashboard/login.html', {'form':form})
    
    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request, username=username , password=password)
            print(user)
            if user is not None:
                email_verify = EmailVerify.objects.filter(user=user).first()
                if email_verify.is_verified:
                    if user.is_student:
                        login(request, user)
                        return redirect('home')
                    else:
                        login(request, user)
                        return redirect('lecture_home')
                else:
                    messages.warning(request, 'Your Account Not Verified Yet, Please Check Your Mail and Verify it (please check spam folder also).')

        return render(request, 'dashboard/login.html', {'form':form})



def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def home_work_details(request):
    hw = HomeWork.objects.filter(user=request.user).order_by('-start_date')
    current_time = timezone.now()
    if request.method == 'GET':
        form = HomeWorkForm()

    else:
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            user = request.user
            subject = form.cleaned_data['subject']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            completed = form.cleaned_data['completed']
            new_hw = HomeWork(user=user, subject=subject, title=title, description=description, start_date=timezone.now(), due_date=due_date, completed=completed)
            new_hw.save()
            messages.success(request, "Home work added Successfully")
            return redirect('home_work_details')

    return render(request, 'dashboard/home_work_details.html', {"hw":hw, "current_time":current_time, "form":form})


# class EditHomeWorkView(View):
#     def get(self, request, pk):
#         hw = get_object_or_404(HomeWork, pk=pk)
#         form = HomeWorkForm(instance=hw)
#         return render(request, "dashboard/edit_homework.html", {"form":form})
    
#     def post(self, request, pk):
#         form = HomeWorkForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home_work_details')
#         return render(request, "dashboard/edit_homework.html", {"form":form})

@login_required
def edit_home_work(request, pk):
    hw = get_object_or_404(HomeWork, pk=pk, user=request.user)

    if request.method == 'POST':
        form = HomeWorkForm(request.POST, instance=hw)
        if form.is_valid():
            form.save()
            messages.info(request, "Home work edited Successfully")
            return redirect('home_work_details')
    else:
        form = HomeWorkForm(instance=hw)
    
    return render(request, 'dashboard/edit_homework.html', {'form':form})


@login_required
def delete_homework(request, pk):
    hw = get_object_or_404(HomeWork, pk=pk, user=request.user)
    hw.delete()
    messages.warning(request, "Home work deleted Successfully")

    return redirect('home_work_details')


@login_required
def add_new_homework(request):
    if request.method == 'GET':
        form = HomeWorkForm()

    else:
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            user = request.user
            subject = form.cleaned_data['subject']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            completed = form.cleaned_data['completed']
            new_hw = HomeWork(user=user,subject=subject, title=title, description=description, start_date=timezone.now(), due_date=due_date, completed=completed)
            new_hw.save()
            messages.success(request, "Home work added Successfully")
            return redirect('home_work_details')

    return render(request, 'dashboard/add_new_homework.html', {'form':form})

@login_required
def view_homework(request, pk):
    # homeworks = get_object_or_404(HomeWork, pk=pk, user=request.user)
    current_time = timezone.now()

    homeworks = HomeWork.objects.filter(pk=pk, user=request.user)
    return render(request, 'dashboard/view_homework.html', {'homeworks':homeworks, 'current_time':current_time})


@login_required
def notes_details(request):
    notes = Notes.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard/notes.html', {"notes":notes})


@login_required
def delete_notes(request, pk):
    notes = Notes.objects.filter(id=pk, user=request.user)
    notes.delete()
    messages.warning(request, "Notes deleted successfully")
    return redirect('notes_details')


@login_required
def edit_notes(request, pk):
    notes = get_object_or_404(Notes, user=request.user, id=pk)
    if request.method == 'GET':
        form = NotesForm(instance=notes)
        return render(request, 'dashboard/edit_notes.html', {"form":form})
    else:
        form = NotesForm(request.POST, instance=notes)
        if form.is_valid():
            form.save()
            messages.success(request, "Notes edited succefully")
            return redirect("notes_details")
        
    return render(request, 'dashboard/edit_notes.html', {"form":form})


@login_required
def create_notes(request):
    if request.method == 'GET':
        form = NotesForm()
        return render(request, 'dashboard/create_notes.html', {"form":form})
    else:
        form = NotesForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            new_note = Notes(user=user, title=title, description=description).save()
            messages.success(request, "Notes added successfully")
            return redirect("notes_details")
    return render(request, 'dashboard/create_notes.html', {"form":form})


from youtubesearchpython import VideosSearch

@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=50)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            
            result_dict['description'] = desc
            result_list.append(result_dict)
        return render(request, 'dashboard/youtube.html', {"form":form, "results":result_list})
    form = DashboardForm()
    return render(request, 'dashboard/youtube.html', {"form":form})


@login_required
def todo(request):
    todo = ToDo.objects.filter(user=request.user).order_by("-date_time")
    current_time = timezone.now()
    return render(request, 'dashboard/todo.html', {"todo":todo, 'current_time':current_time})


@login_required
def edit_todo(request, pk=None):
    todo = get_object_or_404(ToDo, id=pk)
    todo.finished = not todo.finished
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request, pk=None):
    todo = ToDo.objects.filter(id=pk).delete()
    return redirect('todo')

class AddNewTodoView(View):
    def get(self, request):
        form = ToDoForm()
        return render(request, 'dashboard/add_new_todo.html', {'form':form})
    def post(self, request):
        form = ToDoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            finished = form.cleaned_data['finished']
            ToDo(user=request.user, title=title, finished=finished).save()
            messages.success(request, "New ToDo Added Successfully")
            return redirect('todo')
        return render(request, 'dashboard/add_new_todo.html', {'form':form})


import requests

@login_required
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            item = answer['items'][i]['volumeInfo']
            result_dict = {
                'title': item.get('title', 'N/A'),
                'subtitle': item.get('subtitle', ''),
                'description': item.get('description', ''),
                'count': item.get('pageCount', 'N/A'),
                'categories': item.get('categories', []),
                'rating': item.get('averageRating', 'N/A'),
                'thumbnail': item['imageLinks'].get('thumbnail', ''),
                'preview': item.get('previewLink', '')
            }
            
            result_list.append(result_dict)
        return render(request, 'dashboard/books.html', {"form":form, "results":result_list})
    else:
        form = DashboardForm()
    return render(request, 'dashboard/books.html', {"form":form})

def send_main_contact(name=None, email=None, subject=None, message=None):
    subjects = "Contact Us TaskPedia"
    messages = f'Name:{name}\n Email: {email}\n Subject:{subject}\n Message:{message}'
    from_mail = email
    recipent_list = [settings.EMAIL_HOST_USER]
    send_mail(subjects, messages, from_mail, recipent_list)


@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        send_main_contact(name, email, subject, message)
        messages.success(request, "Contact Mail Sent Successfully")
        return redirect('home')

    return render(request, 'dashboard/contact.html')


@login_required
def profile(request):
    pro = StudentProfile.objects.filter(user=request.user)
    if pro:
        return render(request, 'dashboard/profile.html', {"pro":pro})
    else:
        if request.method == "GET":
            form = StudentProfileForm()
        else:
            form = StudentProfileForm(request.POST, request.FILES)
            if form.is_valid():
                reg_no = request.POST['reg_no']
                cls = request.POST['cls']
                full_name = request.POST['full_name']
                phone = request.POST['phone']
                img = request.FILES['img']
                StudentProfile(user=request.user, reg_no=reg_no, cls=cls, full_name=full_name, email=request.user.email, phone=phone, img=img).save()
                messages.success(request, 'Profile Created Successfully')
                return redirect('profile')
    return render(request, 'dashboard/profile.html', {"form":form})


def delete_profile(request, pk):
    pro = StudentProfile.objects.filter(id=pk).delete()
    messages.warning(request, 'Profile Deleted Successfully')
    return redirect('profile')


def edit_profile(request, pk):
    prof = get_object_or_404(StudentProfile, user=request.user, id =pk)
    if request.method == 'GET':
        form = StudentProfileForm(instance=prof)
    else:
        form = StudentProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Edited Successfully")
            return redirect('profile')
    return render(request, 'dashboard/profile.html', {"form":form})


# @login_required
# def dictionary(request):
#     if request.method == 'POST':
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
#         r = requests.get(url)
#         answer = r.json()
#         try:
#             phonetics = answer[0]['phonetics'][0]['text']
#             audio = answer[0]['phonetics'][0]['audio']
#             definition = answer[0]['meanings'][0]['definitions'][0]['definition']
#             example = answer[0]['meanings'][0]['definitions'][0]['example']
#             synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
#             context = {
#                 'form' : form,
#                 'input' : text,
#                 'phonetics' : phonetics,
#                 'audio' : audio,
#                 'definition' : definition,
#                 'example' : example,
#                 'synonyms' : synonyms
#             }
#         except:
#             context = {
#                 'form' : form,
#                 'input' : ''
#             }
#         return render(request, 'dashboard/dictionary.html', context)
#     else:
#         form = DashboardForm()
#     return render(request, 'dashboard/dictionary.html', {'form':form})

from PyDictionary import PyDictionary

@login_required
def dictionary(request):
    # capturing the word from the form via the name search
    if request.method == 'POST':
        
        form = DashboardForm(request.POST)
        word = request.POST['text']
        # creating a dictionary object
        dictionary = PyDictionary()
        # passing a word to the dictionary object
        meanings = dictionary.meaning(word)
        # getting a synonym and antonym  
        synonyms = dictionary.synonym(word)
        antonyms = dictionary.antonym(word)
        # bundling all the variables in the context  
        context = {
                'form' : form,
                'word': word,
                'meanings':meanings,
                'synonyms':synonyms,
                'antonoyms':antonyms
            }
        return render(request, 'dashboard/dictionary_search.html', context)
    else:
        form = DashboardForm()
    return render(request, 'dashboard/dictionary_search.html', {'form':form})
    

@login_required
def assignment(request):
    # Get the StudentProfile instance associated with the logged-in user
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # Now, filter assignments by the StudentProfile instance
    assignment = Assignments.objects.filter(student=student_profile).order_by('-date')
    current_time = timezone.now()
    context = {
        'assignment': assignment,
        'current_time' : current_time
    }
    return render(request, 'dashboard/assignment.html', context) 


@login_required
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignments, id=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment Edited Successfully')
            return redirect('assignment')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'dashboard/edit_assignment.html', {'form':form})


@login_required
def delete_assignment(request, pk):
    Assignments.objects.filter(id=pk).delete()
    messages.warning(request, 'Assignment Deleted Successfully')
    return redirect('assignment')

@login_required
def add_assignment(request):
    if request.method=='POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            std_obj = get_object_or_404(StudentProfile, user=request.user)
            lecture = request.POST['lecture']
            lec_obj = get_object_or_404(LectureProfile, id=lecture)
            title = request.POST['title']
            description = request.POST['description']
            if 'document' in request.FILES:
                document = request.FILES['document']
            else:
                document = None
            Assignments(student=std_obj, lecture=lec_obj, title=title, description=description, document=document).save()
            messages.success(request, 'Assignment Added Successfully')
            return redirect('assignment')
    else:
        form = AssignmentForm()
    return render (request,'dashboard/add_assignment.html',{'form':form })


@login_required
def lecture_contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        send_main_contact(name, email, subject, message)
        messages.success(request, "Contact Mail Sent Successfully")
        return redirect('lecture_home')

    return render(request, 'dashboard/lecture_contact.html')

@login_required
def lecture_home(request):
    return render(request, 'dashboard/lecture_home.html')


@login_required
def lecture_profile(request):
    pro = LectureProfile.objects.filter(user=request.user)
    if pro:
        return render(request, 'dashboard/lecture_profile.html', {"pro":pro})
    else:
        if request.method == "GET":
            form = LectureProfileForm()
        else:
            form = LectureProfileForm(request.POST, request.FILES)
            if form.is_valid():
                full_name = request.POST['full_name']
                department = request.POST['department']
                phone = request.POST['phone']
                img = request.FILES['img']
                LectureProfile(user=request.user, full_name=full_name, department=department, email=request.user.email, phone=phone, img=img).save()
                messages.success(request, 'Profile Created Successfully')
                return redirect('lecture_profile')
    return render(request, 'dashboard/lecture_profile.html', {"form":form})


def edit_lec_profile(request, pk):
    prof = get_object_or_404(LectureProfile, user=request.user, id =pk)
    if request.method == 'GET':
        form = LectureProfileForm(instance=prof)
    else:
        form = LectureProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Edited Successfully")
            return redirect('lecture_profile')
    return render(request, 'dashboard/lecture_profile.html', {"form":form})



def delete_lec_profile(request, pk):
    pro = LectureProfile.objects.filter(id=pk).delete()
    messages.warning(request, 'Profile Deleted Successfully')
    return redirect('lecture_profile')


@login_required
def lecture_assignment(request):
    lf = get_object_or_404(LectureProfile, user=request.user)
    assignment = Assignments.objects.filter(lecture=lf)
    context = {
        'assignment':assignment
    }
    return render(request, 'dashboard/lecture_assignment.html', context)



@login_required
def edit_assignment_lec(request, pk):
    assignment = get_object_or_404(Assignments, id=pk)
    if request.method == 'POST':
        form = LectureAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment Edited Successfully')
            return redirect('lecture_assignment')
    else:
        form = LectureAssignmentForm(instance=assignment)
    return render(request, 'dashboard/edit_assignment_lec.html', {'form':form})

@login_required
def about(request):
    return render(request, 'dashboard/about.html')

@login_required
def lecture_about(request):
    return render(request, 'dashboard/lecture_about.html')