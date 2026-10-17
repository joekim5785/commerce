# Commerce

**An online auction platform built with Django.**

Commerce is a web application that allows users to create auction listings, place bids, explore items by category, manage watchlists and interact through listing comments. It provides a centralised platform for discovering items and participating in online auctions.

## Features

### User Authentication
- User registration and login.
- Secure session-based authentication.
- Access controls for authenticated users.

### Auction Listings
- Create listings with a title, description, starting bid, category and image.
- Browse active listings from the home page.
- View detailed information about individual listings.
- Support for listing images.

### Bidding
- Place bids on active auction listings.
- Validate bids against the starting bid and current highest bid.
- Identify the winning bidder when an auction closes.

### Categories
- Browse listings by category.
- View items within a selected category.
- Navigate listings according to their classification.

### Watchlist
- Add listings to a personal watchlist.
- View saved listings.
- Remove listings from the watchlist.

### Comments
- Post comments on individual listings.
- Display comments with their authors on listing pages.
- Support interaction between users around listed items.

### Auction Outcomes
- Track listing status.
- Display the winner when an auction is completed, where implemented.
- Provide a congratulatory message for the winning bidder.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Django | Backend web framework |
| SQLite | Database management |
| HTML5 | Page structure |
| CSS3 | Custom styling |
| Bootstrap 5 | Responsive user interface |
| JavaScript | Client-side interactions |
| Django Templates | Dynamic page rendering |

## Project Structure

```text
commerce/
├── manage.py
├── commerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── auctions/
│   ├── migrations/
│   ├── static/
│   │   └── auctions/
│   │       └── styles.css
│   ├── templates/
│   │   └── auctions/
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── media/
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10 or later, compatible with the project's Django version.
- Git.
- pip, Python's package installer.

### 1. Clone the repository

```bash
git clone https://github.com/joekim5785/commerce.git
cd commerce
```


### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Development

The application follows Django's Model-View-Template (MVT) architecture:

- **Models** define the application's data structures and database relationships.
- **Views** process requests, execute application logic and return responses.
- **Templates** render dynamic HTML pages.
- **URLs** map incoming requests to the appropriate views.

Database schema changes are managed through Django migrations.

## Future Improvements

Potential enhancements include:

- Search and filtering across listings.
- Auction countdown timers and automatic closing.
- User profiles and bidding history.
- Notifications for outbid users and auction winners.
- Deployment to a production hosting platform.

## Licence

This project is available for personal and educational use. Add a formal licence if you intend to specify permissions for reuse or distribution.
