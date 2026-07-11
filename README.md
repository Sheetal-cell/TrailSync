# Trekking-Management-Application

Adventure organizations require efficient systems to manage trekking activities involving trek organizers, staff, and participants. Currently, many trekking groups rely on spreadsheets, phone calls, or manual coordination, which makes it difficult to manage trek approvals, track bookings, avoid overbooking, and maintain trek history.**

> This project Trekking Management Application web application that allows Admin, Trek Staff, and Users (Trekkers) to interact with the system based on their roles.

---

# 📋 Prerequisites

Before running the project, ensure the following software is installed:

- Python 3.10 or above
- Git (optional)
- Visual Studio Code (recommended)
- DB Browser for SQLite (optional)

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
```

## 2. Navigate to the Project Directory

```bash
cd Trekking-Management-Application
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

## 4. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 5. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 6. Database Setup

If the project contains the **instance/trailsync.db** database file, no additional setup is required.(For this project this has been included)

If the database is not included, initialize it by running the seed/setup script.

Example:

```bash
python seed.py
```

---

## 7. Run the Application

```bash
python app.py
```

---

## 8. Open in Browser

Visit:

```
http://127.0.0.1:5000
```

The application should now be running successfully.

---

# 👥 User Roles

The application supports three different user roles:

- **Administrator**
  (admin credentials: ```email="admin@trailsync.com",
        password="admin123" ```)
  - Manage treks
  - Manage staff
  - View analytics
  - Approve users
  - Assign staff

- **Staff**
  - View assigned treks
  - Update trek progress
  - Manage attendance

- **Trekker**
  - Browse treks
  - Book treks
  - Make simulated payments
  - View booking history

---

# ✨ Features

- 🔐 User Authentication using Flask-Login
- 👤 Role-Based Access Control
- 🏔️ Trek Management
- 📅 Trek Booking System
- 👨‍💼 Staff Assignment
- 📊 Dashboard Analytics
- 🖼️ Cover & Gallery Image Uploads
- 💳 Simulated Payment System (GPay, PhonePe & UPI)
- 📜 Booking History
- 📱 Responsive User Interface
- 🔗 REST API Endpoints
- 🗄️ SQLite Database Integration

---

# 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- Jinja2 Templates

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF

### Database

- SQLite

---

# 📂 Project Structure

```
Trekking-Management-Application/
│
├── app/
│   ├── admin/
│   ├── staff/
│   ├── trekker/
│   ├── models/
│   ├── templates/
│   ├── static/
│   └── extensions.py
│
├── instance/
│   └── trailsync.db
│
├── requirements.txt
├── app.py
└── README.md
```

---

# 💳 Payment Module

This project uses a **simulated payment system** suitable for academic purposes.

Supported payment methods:

- Google Pay
- PhonePe
- UPI

After payment, the system automatically:

- Updates booking status
- Marks payment as **PAID**
- Generates a unique transaction ID

---

# 📌 Future Enhancements

- Razorpay Integration
- Email Notifications
- QR Code Payments
- GPS Tracking
- Online Reviews & Ratings
- AI-based Trek Recommendations

## Issues Encountered and Resolutions

### 1. Database Connection Error
**Issue:**
The Flask application failed to connect to the SQLite database due to an incorrect database path.

**Resolution:**
Updated the SQLAlchemy database URI to point to the correct database file in the `instance` folder and recreated the database.

---

### 2. User Dashboard Not Loading
**Issue:**
After login, the dashboard displayed a blank page because user session data was not being passed correctly.

**Resolution:**
Verified the login route, fixed session handling, and ensured the user information was available before rendering the dashboard.

---

### 3. Trek Booking Failed
**Issue:**
Users were unable to book a trek because the booking form was not validating required fields.

**Resolution:**
Added server-side validation and displayed appropriate error messages for missing inputs.

---

### 4. Git Commit History
**Issue:**
Some commits were associated with the another GitHub account I use for my projects apart from academics.

**Resolution:**
Updated Git configuration, rewrote the affected commit history, and force-pushed the corrected commits.

---

# 👩‍💻 Author

**Sheetal Bajaj**
---
