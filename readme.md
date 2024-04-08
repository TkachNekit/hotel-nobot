# Hotel Booking
---
The Hotel Booking System is a convenient application that allows users to easily and quickly book rooms in a hotel. With its help, you can find and book the perfect accommodation for your stay.

### Key features:

---
- View available rooms: users can easily find suitable rooms using filters and sorting by price and room's capacity.
- Search for vacant rooms: the system allows users to search for available rooms within a specified time interval.
- Room booking: book your desired room in just a few clicks. Booking is available only to registered users.
- Administrative panel: the superuser can manage rooms and bookings through the Django administrative panel.
- Registration and authentication: users can register to view their bookings and log in to the system to book rooms.


### Technological stack:

---
- Django.
- Django REST Framework: for API.
- Djoser for authorization.
- PostgreSQL.
- PyTest.
- Linters: _isort_ + _flake8_.
- drf-yasg for API docs.

## Installation

---
All actions should be executed from the source directory of the project and only after installing all requirements.
1. Firstly, create and activate a new virtual environment:
   ```
   python3.9 -m venv ../venv
   source ../venv/bin/activate
   ```
2. Install packages:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Run project dependencies, migrations, tests, fill the database with the fixture data etc.:
   ```
   python manage.py migrate
   python manage.py loaddata fixtures/data.json
   
   pytest
   python manage.py runserver 
   ```
   Run last 2 commands separately 

### Example of .env file

---
```text
DEBUG=bool
SECRET_KEY=django_secret_key

DATABASE_NAME=name
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=host
DATABASE_PORT=1234

```


## API

---

docs you can read on `http://127.0.0.1:8000/swagger/` <br>
Main endpoints: <br>
#### Auth
- POST http://127.0.0.1:8000/api-token-auth/  - for obtaining auth token for our superuser
- GET http://127.0.0.1:8000/api/auth/users/ - returns list of authorized users
- POST http://127.0.0.1:8000/api/auth/users/ - registers new user
- POST http://127.0.0.1:8000/api/auth/token/login/ - returns auth token which can be used by user for auth
- POST http://127.0.0.1:8000/api/auth/token/logout/ - deactivates auth token for user (should place auth token in header)
#### Rooms
- GET http://127.0.0.1:8000/api/rooms/ - returns list of rooms <br>
*Sort and filter with query params:*
  - Sort by = (price_asc, price_desc, capacity_asc, capacity_desc) http://127.0.0.1:8000/api/rooms/?sort_by=price_asc
  - Filter by min capacity of room capacity http://127.0.0.1:8000/api/rooms/?capacity=3
  - Filter by min and max cost http://127.0.0.1:8000/api/rooms/?max_price=200000&min_price=3000
  - Filter by rooms availability http://127.0.0.1:8000/api/rooms/?checkin=2024-10-9&checkout=2024-10-10
- GET http://127.0.0.1:8000/api/rooms/ - returns specific of room
- POST http://127.0.0.1:8000/api/rooms/ - creates room (Admin only)
- PATCH http://127.0.0.1:8000/api/rooms/&lt;pk:int&gt;/ - patch specific room (Admin only)
- DEL http://127.0.0.1:8000/api/rooms/&lt;pk:int&gt;/ - delete specific room (Admin only)
#### Bookings (with auth token only)
- GET http://127.0.0.1:8000/api/bookings/ - returns list of user's bookings (for admin returns all bookings)
- POST http://127.0.0.1:8000/api/bookings/ - creates booking (if this room is not already booked for these dates)
- PATCH http://127.0.0.1:8000/api/bookings/&lt;pk:int&gt;/cancel/ - cancels user's booking (Admin can cancel any booking)
- PATCH http://127.0.0.1:8000/api/bookings/&lt;pk:int&gt;/ - patch specific booking (Admin only)
- DEL http://127.0.0.1:8000/api/bookings/&lt;pk:int&gt;/ - delete specific booking (Admin only)



## [DataBase Schema](https://github.com/TkachNekit/hotel-booking/blob/master/images/Hotel%20booking%20database.pdf)
(If it doesn't open in preview you can always download it)
## [Activity Diagram](https://github.com/TkachNekit/hotel-booking/blob/master/images/Hotel%20Booking%2C%20activity%20diagram.png)