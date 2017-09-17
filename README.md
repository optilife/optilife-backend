# optilife-backend

The backend delivers all the neccessary calculations and REST endpoints to run OptiLife.

## REST endpoints

* *GET /api/users/\<id\>*
```
{
  "actual_budget": 582.0,
  "weight": 72.2,
  "mail": "axel@mail.com",
  "vegeterian": false,
  "username": "Axel",
  "height": 2.01,
  "password_hash": "password",
  "gender": "m",
  "age": 25,
  "id": 4,
  "monthly_budget": 675.0
}
```

* *GET /api/users/health-index/\<id\>*
```
{
 {
  "calories_today": 1000.0,
  "calories_today_percentage": 50.0,
  "challenges_won": 22,
  "daily_goal": 0,
  "health-index": 84.7
 }
}
```

etc....
