<div align="center">
<h1>Django Job Portal Project using Django Form</h1>
</div>

# Context

- [Context](#context)
  - [Question](#question)
  - [Solution](#solution)
    - [Virtual Environment Setup](#virtual-environment-setup)
    - [Project \& App Setup](#project--app-setup)
    - [Create Models](#create-models)
    - [Register Models in Admin](#register-models-in-admin)
    - [Database Migrations](#database-migrations)
    - [Superuser Create](#superuser-create)
    - [Create Django Forms](#create-django-forms)
    - [Templates Setup](#templates-setup)
    - [User Authentication](#user-authentication)
    - [Dashboard](#dashboard)
    - [Profile](#profile)
      - [Profile Page](#profile-page)
      - [Update Profile](#update-profile)
    - [Job Post](#job-post)
      - [Show All Added Job](#show-all-added-job)
      - [Add and Update Job](#add-and-update-job)
      - [Delete Added Job](#delete-added-job)
    - [Job Apply](#job-apply)
      - [Seeker job apply](#seeker-job-apply)
      - [Show All Applied Job](#show-all-applied-job)
    - [Candidate List](#candidate-list)
    - [Search jobs](#search-jobs)
    - [Skill Match Jobs](#skill-match-jobs)

## Question

- Job : Develop a job Portal

  > Develop a job portal using Django. In this project you have to incorporate multiple recruiters and multiple job seekers from different domains on one platform. A single recruiter can post multiple job openings using his/her account. A single job seeker can apply for multiple openings based on his skills. Both recruiters and job seekers are able to manage their account using a profile manager.

- Job Specification information
  - Create a project named Name_ID_JobPortal.
  - Develop a registration page using the following fields (`Username`, `Display name`, `Email`, `Password`, `Confirm Password`, `User type`)
  - Develop a login page using the following fields (`Username` and `Password`)
  - Develop a profile creation page based on user type
    - `Recruiters` (Company information)
    - `Jobseekers` (`Skills set` and `resume upload option`)
  - Develop a `job posting` page for `recruiters` (`Title`, `Number of openings`, `Category`, `Job description`, `Skills set`)
  - Develop a `job applying` page for `jobseeker` (`Search`)
  - Develop a `skill matching page` for both `recruiters` and `jobseeker` (`Dashboard` for `skill matched job`)

> [!IMPORTANT]
>
> 1. Create a Django Project. (Naming Convention: `Name_ID_Project`)
>
> 2. Create a Database.
>
> 3. Store the Database.

## Solution

### Virtual Environment Setup

- Create virtual environment

  ```sh
  py -m venv .venv
  ```

- Activate virtual environment

  ```sh
  .venv\Scripts\activate.bat
  ```

- Install required packages

  ```sh
  pip install django pillow crispy-bootstrap5
  ```

---
[⬆️ Go to Context](#context)

### Project & App Setup

- Project

  ```sh
  django-admin startproject Tansen_101_JobPortalProject
  ```

- App

  ```sh
  py manage.py startapp JobPortalApp
  ```

- Add app name in [settings.py](./Tansen_101_JobPortalProject/settings.py) `INSTALLED_APPS`

  ```py
  INSTALLED_APPS = [
      ...
      # my apps
      'JobPortalApp'
  ]
  ```

---
[⬆️ Go to Context](#context)

### Create Models

- Open [models.py](./JobPortalApp/models.py) and create models

  - User authentication model

    ```py
    class CustomUserModel(AbstractUser):
      USER_TYPES = [
        ('Recruiter', 'Recruiter'),
        ('Seeker', 'Seeker'),
      ]

      user_type = models.CharField(choices=USER_TYPES, max_length=100, null=True)
      displa_name = models.CharField(max_length=100, null=True)

      def __str__(self):
          return f'{self.username}'
    ```

    - We will use this model for registration (`username`, `email`, `password`, `confirm password` and other two field mentioned are `user type` and `display name`)
    - We need to add a variable `AUTH_USER_MODEL` in [settings.py](./Tansen_101_JobPortalProject/settings.py)

      ```py
      # auth model (app_name.model_name)
      AUTH_USER_MODEL='JobPortalApp.CustomUserModel'
      ```

  - Now that we have registration model and our website will have two types of user so we will create those user profile model which is `RecruiterProfileModel` and `SeekerProfileModel`

  - `RecruiterProfileModel` model

    ```py
    class RecruiterProfileModel(models.Model):
      # relation field
      recruiter = models.OneToOneField(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='recruiter_info',
        null=True
      )

      address = models.TextField(null=True)
      contact = models.CharField(max_length=20, null=True)
      logo = models.ImageField(upload_to='company_logo', null=True)

      created_at = models.DateField(auto_now_add=True, null=True)
      updated_at = models.DateField(auto_now=True, null=True)

      def __str__(self):
          return f'{self.recruiter}'
    ```

    - We will use this model for storing recruiter profile data
    - In relationship we made `one-to-one (OneToOneField)` cause one recruiter user can have only one profile

  - `SeekerProfileModel` model

    ```py
    class SeekerProfileModel(models.Model):
      # relation field
      seeker = models.OneToOneField(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name='recruiter_info',
        null=True
      )

      address = models.TextField(null=True)
      contact = models.CharField(max_length=20, null=True)
      profile_image = models.ImageField(upload_to='seeker_image', null=True)
      skills_set = models.TextField(null=True)

      created_at = models.DateField(auto_now_add=True, null=True)
      updated_at = models.DateField(auto_now=True, null=True)

      def __str__(self):
          return f'{self.seeker}'
    ```

    - We will use this model to store seeker profile data
    - In relationship we made `one-to-one (OneToOneField)` cause one seeker user can have only one profile

  - We have stored user profile now there should be `job post` by `recruiter` and then `job apply` for `seeker`
  - `CategoryModel` and `JobPostModel` model

    ```py
    # (Title, Number of openings, Category, Job description, Skills set
    class CategoryModel(models.Model):
      name = models.CharField(max_length=200, null=True)

      def __str__(self):
          return f'{self.name}'


    class JobPostModel(models.Model):
      # relation field
      posted_by = models.ForeignKey(
        RecruiterProfileModel,
        on_delete=models.CASCADE,
        related_name='job_post_info',
        null=True
      )
      category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        null=True
      )

      title = models.CharField(max_length=200, null=True)
      number_of_openings = models.PositiveIntegerField(null=True)
      description = models.TextField(null=True)
      skills_set = models.TextField(null=True)
      deadline = models.DateField(null=True)
      salary = models.FloatField(null=True)

      created_at = models.DateField(auto_now_add=True, null=True)
      updated_at = models.DateField(auto_now=True, null=True)

      def __str__(self):
          return f'{self.title}'
    ```

    - We created separate model for catefory so that recruiter can add multiple category or we could use the choices to use fixed values
    - In `JobPostModel` there is two relationship field where one is who is posting the job and another is category

  - `ApplyJobModel` model

    ```py
    class ApplyJobModel(models.Model):
      # relation field
      applied_by = models.ForeignKey(
        SeekerProfileModel,
        on_delete=models.CASCADE,
        related_name='applied_by_info',
        null=True
      )
      applied_job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name='applied_job_info',
        null=True
      )
      STATUS_CHOICES = [
            ('Pending', 'Pending'),
            ('Reviewing', 'Reviewing'),
            ('Interview', 'Interview'),
            ('Rejected', 'Rejected'),
            ('Accepted', 'Accepted'),
        ]
      status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', null=True)
      resume = models.FileField(upload_to='seeker_resume', null=True)
      applied_at = models.DateField(auto_now_add=True, null=True)

      def __str__(self):
          return f'{self.applied_by}-{self.applied_job}'
    ```

    - In `ApplyJobModel` model also have two relationship field where one is who is applying for the job and another is which job is applying to

---
[⬆️ Go to Context](#context)

### Register Models in Admin

- Register all models in [admin.py](./JobPortalApp/admin.py)

  ```py
  from django.contrib import admin
  from JobPortalApp.models import *

  # Register your models here.
  admin.site.register([
    CustomUserModel,
    RecruiterProfileModel,
    SeekerProfileModel,
    CategoryModel,
    JobPostModel,
    ApplyJobModel,
  ])
  ```

---
[⬆️ Go to Context](#context)

### Database Migrations

- Project Level Migrations

  ```sh
  py manage.py makemigrations
  ```

  ```sh
  py manage.py migrate
  ```

- App Level Migrations

  ```sh
  py manage.py makemigrations JobPortalApp
  ```

  ```sh
  py manage.py migrate JobPortalApp
  ```

---
[⬆️ Go to Context](#context)

### Superuser Create

- Create superuser

  ```sh
  py manage.py createsuperuser
  ```

---
[⬆️ Go to Context](#context)

### Create Django Forms

- Create a file [forms.py](./JobPortalApp/forms.py) and create django forms in it

  - `RegisterForm`, `LoginForm` and `UserModifyForm`

    ```py
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

    # user creation form
    class RegisterForm(UserCreationForm):
      class Meta:
        model = CustomUserModel
        fields = ['username','display_name', 'email','user_type', 'password1','password2']

    # authentication form
    class LoginForm(AuthenticationForm):
        pass
    ```

    - Both form is based on our custom user model which we named `CustomUserModel` in [models.py](./JobPortalApp/models.py)
    - Here `password1` and `password2` in register page one is password and another is confirm password
    - We can skip the `AuthenticationForm` here and directly use it in [views.py](./JobPortalApp/views.py)
    - Comment this part in [settings.py](./Tansen_101_JobPortalProject/settings.py) to skip default validation

      ```py
      # AUTH_PASSWORD_VALIDATORS = [
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
      #     },
      # ]
      ```

  - `RecruiterProfileUpdateForm` form

    ```py
    class RecruiterProfileUpdateForm(forms.ModelForm):
      class Meta:
        model = RecruiterProfileModel
        fields = '__all__'
        exclude = ['recruiter']
    ```

    - The excluded one field will be handle in [views.py](./JobPortalApp/views.py)

  - `SeekerProfileUpdateForm` form

    ```py
    class SeekerProfileUpdateForm(forms.ModelForm):
      class Meta:
        model = SeekerProfileModel
        fields = '__all__'
        exclude = ['seeker']
    ```

    - The excluded one field will be handle in [views.py](./JobPortalApp/views.py)

  - `JobPostForm` form

    ```py
    class JobPostForm(forms.ModelForm):
      class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['posted_by']

        widgets = {
            'deadline': forms.DateInput(attrs={
                'type': 'date'
            })
        }
    ```

  - `ApplyJobForm` form

    ```py
    class ApplyJobForm(forms.ModelForm):
      class Meta:
        model = ApplyJobModel
        fields = ['resume']
    ```

> [!IMPORTANT]
>
> - For each model we will have form in `forms.py`
> - Some model are created to extend the fields so they might not present in `forms.py` like `CategoryModel`
> - Everytime create a form ask yourself `Do I need this model data to be filled by user?` then make the form for that, so user could fill it

---
[⬆️ Go to Context](#context)

### Templates Setup

- Create all the HTML files

  ```txt
  📁 templates
  ├── 📁 master
  │   ├── 🌐 base-form.html
  │   ├── 🌐 base.html
  │   ├── 🌐 messages.html
  │   └── 🌐 nav.html
  ├── 🌐 browse-jobs.html
  ├── 🌐 candidate-list.html
  ├── 🌐 dashboard.html
  ├── 🌐 my-applications.html
  └── 🌐 profile.html
  ```

  - We are using single [base-form.html](./JobPortalApp/templates/master/base-form.html) for every form we defined in [forms.py](./JobPortalApp/forms.py)

- Make sure to use crispy form in the [base-form.html](./JobPortalApp/templates/master/base-form.html)

---
[⬆️ Go to Context](#context)

### User Authentication

- For registration
  - Create function in [views.py](./JobPortalApp/views.py)

    ```py
    def register_view(request):
        if request.method == 'POST':
            form_data = RegisterForm(request.POST)
            if form_data.is_valid():
                form_data.save()
                messages.success(request, 'User Creation Successfully.')
                return redirect('login_view')

        form_data = RegisterForm()
        context = {
            'form_data': form_data,
            'title': 'Register Page',
            'form_title': 'User Registration Form',
            'form_btn': 'Register',
        }
        return render(request, 'master/base-form.html', context)
    ```

    - Make sure [base-form.html](./JobPortalApp/templates/master/base-form.html) has `csrf torken` and `method="POST" enctype="multipart/form-data"`

  - Add URL pattern in [urls.py](./JobPortalApp/urls.py)

- For login
  - Create function in [views.py](./JobPortalApp/views.py)

    ```py
    def login_view(request):
        if request.method == 'POST':
            form_data = AuthenticationForm(request, request.POST)
            if form_data.is_valid():
                user = form_data.get_user()
                if user:
                    login(request, user)
                    messages.success(request, 'User Login Successfully.')
                    return redirect('dashboard_view')
            messages.error(request, 'Invalid Credentials.')

        form_data = AuthenticationForm()
        context = {
            'form_data': form_data,
            'title': 'Login Page',
            'form_title': 'User Login Form',
            'form_btn': 'Login',
        }
        return render(request, 'master/base-form.html', context)
    ```

    - In here we used `get_user()` from the form data

  - Add URL pattern in [urls.py](./JobPortalApp/urls.py)

- Do the same for `logout_view` function

---
[⬆️ Go to Context](#context)

### Dashboard

- Just render it for first time, later we will update (first user need to update profile and job post or apply then we will update this dashboard)

  ```py
  @login_required
  def dashboard_view(request):

      return render(request, 'dashboard.html')
  ```

---
[⬆️ Go to Context](#context)

### Profile

#### Profile Page

- Just render this page
- We will access all data using `related_name`

---
[⬆️ Go to Context](#context)

#### Update Profile

- We can update the current user data using this view

  ```py
  @login_required
  def update_profile_view(request):
      current_user = request.user
      if current_user.user_type == 'Recruiter':
          try:
              profile_data = RecruiterProfileModel.objects.get(recruiter= current_user)
          except:
              profile_data = None
          if request.method == 'POST':
              form_data = RecruiterProfileUpdateForm(request.POST, request.FILES, instance=profile_data)
              if form_data.is_valid():
                  data = form_data.save(commit=False)
                  data.recruiter = current_user
                  data.save()
                  messages.success(request, 'Profile Updated Successfully.')
                  return redirect('profile_view')
          form_data = RecruiterProfileUpdateForm(instance=profile_data)
      else:
          try:
              profile_data = SeekerProfileModel.objects.get(seeker = current_user)
          except:
              profile_data = None
          if request.method == 'POST':
              form_data = SeekerProfileUpdateForm(request.POST, request.FILES, instance=profile_data)
              if form_data.is_valid():
                  data = form_data.save(commit=False)
                  data.seeker = current_user
                  data.save()
                  messages.success(request, 'Profile Updated Successfully.')
                  return redirect('profile_view')
          form_data = SeekerProfileUpdateForm(instance=profile_data)

      context = {
          'form_data': form_data,
          'title': 'Update Profile Info Page',
          'form_title': 'Update Profile Info Form',
          'form_btn': 'Update Profile',
      }
      return render(request, 'master/base-form.html', context)
  ```

  - In here we have a condition for two type of user
  - Based on user type profile is being updated

---
[⬆️ Go to Context](#context)

### Job Post

#### Show All Added Job

```py
def browse_job_view(request):
    current_user = request.user
    print(current_user)
    if not current_user:
        if current_user.user_type == 'Recruiter':
            job_data = JobPostModel.objects.filter(posted_by = current_user.recruiter_profile)

    job_data = JobPostModel.objects.all()
    context = {
        'job_data': job_data
    }
    return render(request,'browse-jobs.html', context)
```

- Why we're first showing the job post list and not doing the `job post` first, reason is simple, we need the `add job post` button which we planned to put in the list page

---
[⬆️ Go to Context](#context)

#### Add and Update Job

- Both are using same HTML base form

  ```py
  @login_required
  def post_job_view(request):
      try:
          recruiter_data = request.user.recruiter_profile
      except:
          messages.error(request, 'Please, Update your profile first.')
          return redirect('update_profile_view')

      if request.method == 'POST':
          form_data = JobPostForm(request.POST, request.FILES)
          if form_data.is_valid():
              data = form_data.save(commit=False)
              data.posted_by = recruiter_data
              data.save()
              messages.success(request, 'Job Posted Successfully.')
              return redirect('browse_job_view')

      form_data = JobPostForm()
      context = {
          'form_data': form_data,
          'title': 'Post Job Page',
          'form_title': 'Post Job Info Form',
          'form_btn': 'Post',
      }
      return render(request, 'master/base-form.html', context)


  @login_required
  def update_job_view(request, id):
      try:
          recruiter_data = request.user.recruiter_profile
          job = JobPostModel.objects.get(id = id)
      except:
          messages.error(request, 'Please, Update your profile first.')
          return redirect('update_profile_view')

      if request.method == 'POST':
          form_data = JobPostForm(request.POST, request.FILES, instance=job)
          if form_data.is_valid():
              data = form_data.save(commit=False)
              data.posted_by = recruiter_data
              data.save()
              messages.success(request, 'Job Updated Successfully.')
              return redirect('browse_job_view')

      form_data = JobPostForm(instance=job)
      context = {
          'form_data': form_data,
          'title': 'Update Job Page',
          'form_title': 'Update Job Info Form',
          'form_btn': 'Update',
      }
      return render(request, 'master/base-form.html', context)
  ```

  - As we have mentioned before user must update their profile first before anything else so if user profile not found it will redirect to profile update page
  - After that user can `add`/`update` job

---
[⬆️ Go to Context](#context)

#### Delete Added Job

  ```py
  @login_required
  def delete_job_view(request, id):
      try:
          JobPostModel.objects.get(id = id).delete()
          messages.error(request, 'Job Deleted successfully.')
          return redirect('browse_job_view')
      except:
          messages.error(request, 'Job Not Found.')
          return redirect('browse_job_view')
  ```

---
[⬆️ Go to Context](#context)

### Job Apply

#### Seeker job apply

```py
@login_required
def apply_job_view(request, id):
    try:
        seeker_profile = request.user.seeker_profile
        job = JobPostModel.objects.get(id=id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile_view')
    if request.method == 'POST':
        form_data = ApplyJobForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by = seeker_profile
            data.applied_job = job
            data.save()
            messages.success(request, 'Application submit successfully.')
            return redirect('browse_job_view')

    form_data = ApplyJobForm()
    context = {
        'form_data': form_data,
        'title': 'Apply Job Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply',
    }
    return render(request, 'master/base-form.html', context)
```

- Same thing goes here user must update profile first then apply job

#### Show All Applied Job

  ```py
  def my_application(request):
      try:
          my_application = ApplyJobModel.objects.filter(applied_by = request.user.seeker_profile)
      except:
          messages.error(request, 'Please, Update your profile first.')
          return redirect('update_profile_view')
      context = {
          'application_list': my_application,
          'title': 'My Application Page',
          'form_title': 'Apply Job Info Form',
          'form_btn': 'Apply',
      }
      return render(request, 'my-applications.html',context)
  ```

---
[⬆️ Go to Context](#context)

---
[⬆️ Go to Context](#context)

### Candidate List

- Recruiter can see who applied to the job

  ```py
  def candidate_list_view(request, id):

      job_data = JobPostModel.objects.get(id=id)
      candidate_data = ApplyJobModel.objects.filter(applied_job=job_data)

      # status update
      if request.method == "POST":
          candidate_id = request.POST.get('candidate_id')
          status = request.POST.get('status')
          candidate = ApplyJobModel.objects.get(id=candidate_id)
          candidate.status = status
          candidate.save()
          return redirect('candidate_list_view', id=id)

      context = {
          'candidate_data': candidate_data,
          'job_data': job_data,
          'title': 'Candidate List Page',
      }
      return render(request,'candidate-list.html',context)
  ```

  - In here we have process the status of the candidate also
  - We have to update the HTML page status section table data as below

    ```jinja
    <td>
        <form method="POST">
            {% csrf_token %}

            <input type="hidden" name="candidate_id" value="{{candidate.id}}">

            <select name="status"
                    class="form-select"
                    onchange="this.form.submit()">

                <option value="Pending"
                {% if candidate.status == 'Pending' %}selected{% endif %}>
                Pending
                </option>

                <option value="Reviewing"
                {% if candidate.status == 'Reviewing' %}selected{% endif %}>
                Reviewing
                </option>

                <option value="Interview"
                {% if candidate.status == 'Interview' %}selected{% endif %}>
                Interview
                </option>

                <option value="Rejected"
                {% if candidate.status == 'Rejected' %}selected{% endif %}>
                Rejected
                </option>

            </select>
        </form>
    </td>
    ```


---
[⬆️ Go to Context](#context)

### Search jobs

- We need to update `browse_job_view` function

  ```py
  def browse_job_view(request):
      current_user = request.user
      print(current_user)
      search_query = request.GET.get('search_query')

      job_data = JobPostModel.objects.all()
      print("browse job: ", job_data)

      if  current_user.is_authenticated:
          if current_user.user_type == 'Recruiter':
              try:
                  job_data = JobPostModel.objects.filter(posted_by = current_user.recruiter_profile)
              except:
                  messages.error(request, 'Please, Update your profile first.')
                  return redirect('update_profile_view')
      if search_query:
          job_data = JobPostModel.objects.filter(
              Q(title__icontains = search_query) |
              Q(category__name__icontains = search_query) |
              Q(posted_by__company_name__icontains = search_query)
          )
      context = {
          'job_data': job_data
      }
      return render(request,'browse-jobs.html', context)
  ```

  - In here `Q` is used for search and `__icontains` is like finding similar
  - We imported `Q` by `from django.db.models import Q`

---
[⬆️ Go to Context](#context)

### Skill Match Jobs

- Finally, we will update the `dashboard_view` function to show the skill match jobs

  ```py
  @login_required
  def dashboard_view(request):
      try:
          seeker_data = request.user.seeker_profile
      except:
          messages.error(request, 'Please, Update your profile first.')
          return redirect('update_profile_view')
      job_data = JobPostModel.objects.none()
      if request.user.user_type == 'Seeker':
          seeker_skill = request.user.seeker_profile.skills_set

          for skill in seeker_skill.split(','):
              cleaned_skill = skill.strip()
              job_data |= JobPostModel.objects.filter(skills_set__icontains = cleaned_skill)

      context = {
          "job_data": job_data
      }

      return render(request, 'dashboard.html',context)
  ```

  - We use split cause skill set are separated by `,` and `strip()` used to remove whitespace
  - In here we are showing match skill which is being union by using `|=` so that duplicate data not shown

---
[⬆️ Go to Context](#context)
