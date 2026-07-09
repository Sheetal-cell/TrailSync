# Trekking-Management-Application

Adventure organizations require efficient systems to manage trekking activities involving trek organizers, staff, and participants. Currently, many trekking groups rely on spreadsheets, phone calls, or manual coordination, which makes it difficult to manage trek approvals, track bookings, avoid overbooking, and maintain trek history.**

> This project Trekking Management Application web application that allows Admin, Trek Staff, and Users (Trekkers) to interact with the system based on their roles.

Features include:-


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
