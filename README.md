# 📚 Learning Management System (LMS) - Django

This project is a **feature-rich Learning Management System (LMS)** built with **Django**. It allows users to enroll in courses, track progress, and interact with instructors.

## 📌 Features
- **User Authentication**: Registration, Login, and Profile Management
- **Course Management**: Add, edit, and delete courses (Admin Feature)
- **Enrollments**: Students can enroll and track their progress
- **Quizzes & Assignments**: Interactive learning modules
- **Progress Tracking**: See completed courses and certificates
- **Instructor Dashboard**: Manage courses and students
- **Responsive UI**: Built with Bootstrap for a modern look

## 📁 Project Structure
``` 
LMS-Django/ 
│ 
└── lms_project/  
      │ 
      └─── courses/                # Course-related functionality  
      |
      ├── customer/               # Customer-related functionality 
      |
      ├── home/                   # Homepage and general pages 
      |
      ├── lms_project/            # Main Django project folder
      |
      ├── media/                  # Uploaded course images & files 
      |
      ├── static/                 # Static files (CSS, JavaScript, Images)
      | 
      ├── templates/              # HTML Templates 
      |
      ├── user/                   # User authentication and profiles app 
      |
      ├── db.sqlite3              # SQLite database 
      ├── manage.py               # Django management script 
      ├── README.md               # Project documentation 
      └── requirements.txt        # Dependencies
```


## 🛠️ Installation & Setup
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-repo/LMS-Django.git
   cd LMS-Django
   ```

2. **Create a virtual environment**  
   ```bash
   python -m venv env
   source env/bin/activate  # On macOS/Linux
   env\Scripts\activate   # On Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**  
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**  
   ```bash
   python manage.py runserver
   ```

## 🚀 Features Breakdown
- **Student Dashboard**: View enrolled courses, track progress.
- **Instructor Dashboard**: Create & manage courses.
- **Admin Panel**: Full control over users, courses, and content.
- **Search & Filters**: Easily find courses.
- **Secure & Scalable**: Django’s robust authentication system.

## 📜 License
This project is for educational and research purposes.

## 💡 Contributing
Feel free to submit PRs, open issues, and contribute! 😊

##  Contact 
For any queries or suggestions, reach out to: 

📞 **Phone**: +91-8971812177

📧 **Email**: manjupatat80@gmail.com

🐙 **GitHub**: [Manjunath L Patat](https://github.com/Manjupatat)

# 🚀 Happy Learning! 🎓
