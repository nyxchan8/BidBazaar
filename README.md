# 🏷️ BidBazaar – E-commerce Auction Site

## 🛠️ Technologies Used

| Category       | Technology                |
| -------------- | ------------------------- |
| Framework      | Django 4.x                |
| Language       | Python 3.11               |
| Database       | SQLite (default)          |
| Authentication | Django Auth               |
| Frontend       | HTML, CSS, Bootstrap      |
| Deployment     | Local / Optional: Railway |

---

## 📂 Folder Structure

This project has the following directory structure:

```text
commerce/
├── auctions/
│   ├── migrations/
│   ├── templates/
│   │   └── auctions/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── commerce/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt

Open your browser and go to http://127.0.0.1:8000
Register a user and test features: listings, bids, comments, watchlist

## 🚀 Features

Create Listing: Users can create new auction listings with title, description, starting bid, optional image, and category
Active Listings: See all active listings on the homepage
Listing Page: View listing details, place bids, comment, close auction (if creator), add/remove from watchlist
Watchlist: View items added to your personal watchlist
Categories: Browse listings by category
Admin Panel: Full management of users, listings, bids, and comments

## ⚙️ Notes

The highest bid is calculated automatically
Only the listing creator can close the auction
CSRF protection and authentication are enabled
Pagination is used to display 10 listings per page
