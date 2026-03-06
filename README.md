# 📘 SnapBook – Social Media REST API

SnapBook is a Django REST Framework based social media backend where users can share posts, like/unlike them, comment, and manage their profiles.

This project is built as a practice assignment focusing on authentication, permissions, API design, and social media features.

---

## 🚀 Features

### 🔐 User Authentication
- User Registration with email verification  
- Login and Logout system  
- JWT Authentication  
- Secure profile management  

### 🧑‍💻 User Profile
- Users can update profile details  
- Additional fields:
  - Phone number  
  - Location (Dhaka, Chittagong, etc.)  
  - Address  

### 📰 Posts
- Users can create posts with:
  - Text caption  
  - Image (via Cloudinary)  
  - Optional YouTube video URL  
- Public post listing  
- Search posts by caption or email  
- Pagination support  

### 👍 Like / Unlike System
- Logged-in users can like a post  
- Can also unlike a post  
- Total likes and unlikes displayed  

### 💬 Comment System
- Users can comment on posts  
- Edit or delete own comments  
- Nested comments under posts  

### 📊 Dashboard
- User dashboard API  
- My Posts API  
- Profile API  
- Comment management under posts  

### 📖 API Documentation
- Swagger UI with drf-yasg  
- Interactive API testing  

---

## 🛠 Tech Stack

- Python  
- Django  
- Django REST Framework  
- JWT Authentication  
- PostgreSQL  
- Cloudinary  
- Swagger / drf-yasg  

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/sia72/snapbook.git
cd snapbook
```
2. Create Virtual Environment
```
python -m venv env
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows
```
3. Install Dependencies
```
pip install -r requirements.txt
```

4. Configure Environment Variables
```

Create a .env file in project root:

SECRET_KEY=your-secret-key

EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

CLOUDINARY_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

DATABASE_NAME=snapbook
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432

🗄 Database Setup
```
python manage.py makemigrations
python manage.py migrate
```

Create superuser:
```
python manage.py createsuperuser
```
▶ Run Project
python manage.py runserver
```
```
Access API:

http://127.0.0.1:8000/api/
```

## 🔗 API Endpoints

### 🔐 Authentication

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/auth/users/` | POST | Register new user |
| `/auth/jwt/create/` | POST | Login and get JWT token |
| `/auth/jwt/refresh/` | POST | Refresh access token |
| `/auth/jwt/verify/` | POST | Verify token |

---

### 📝 Posts

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/api/posts/` | GET | Get all public posts |
| `/api/posts/` | POST | Create a new post |
| `/api/posts/<id>/` | GET | View post details |
| `/api/posts/<id>/` | PUT / PATCH | Update own post |
| `/api/posts/<id>/` | DELETE | Delete own post |
| `/api/posts/<id>/like/` | POST | Like a post |
| `/api/posts/<id>/unlike/` | POST | Unlike a post |

---

### 💬 Comments

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/api/posts/<id>/comments/` | GET | View all comments for a post |
| `/api/posts/<id>/comments/` | POST | Add comment to a post |
| `/api/comments/<id>/` | PUT | Update own comment |
| `/api/comments/<id>/` | DELETE | Delete own comment |

---

### 📊 Dashboard

| Endpoint | Description |
|--------|-------------|
| `/api/profile/` | View and update logged-in user profile |
| `/api/my-posts/` | View, update, and delete own posts |
📄 API Documentation

Swagger UI:

http://127.0.0.1:8000/swagger/


ReDoc:

http://127.0.0.1:8000/redoc/

## 👤 Permissions

| Role | Access |
|------|--------|
| Guest | View public posts |
| Member | Create posts, like/unlike posts, comment on posts |
| Admin | Full control over all content |

---

## 🧪 Testing

You can test the APIs using:

- **Postman**
- **DRF Browsable API**
- **Swagger UI**

---

## 📌 Future Improvements

- Follow/Unfollow system  
- Real-time notifications  
- Direct messaging / chat  
- Post sharing functionality  
- User activity feed  
- Payment system

---

## 🤝 Contributing

Pull requests are welcome.  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.