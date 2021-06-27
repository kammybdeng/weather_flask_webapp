# Weather Forecast Application
A weather forecast application that allows users to search a city's weather and save their favorite cities. The application performs API calls to a third party resource to fetch for weather data. The backend is built with Flask and the frontend is built with JavaScript, Bootstrap, HTML, and CSS.

## Live site
https://weather-app100.herokuapp.com/


## Main Features
- Usage of Flask **Template** to built User Registration, Login/Logout, and Account Views.
- Save and delete cities functionality built with **CRUD** operation.
- Usage of **Flask-SQLAlchemy** to built Database to store user information
- Implemented **AJAX** calls with jQuery to allow users to request for a different city weather without having to reload the page.
- Usage of **Flask-Bcrypt** for User Authentication and storage of Password
- Usage of **request library** to fetch third party's data through its API
- Package Structure and **Configuration** for deployment in Heroku

## Features in development
- Ability to modify cities in dashboard
- Ability to use Google map to select location

## Challenges
- First time adding AJAX to a flask application. This stack is uncommon, hence it was more difficult to find useful documentations.
- Some libraries mentioned in the tutorial were deprecated. I had to find solutions to replace the deprecated methods.
- First time deploying on Heroku, hence running into many unfamiliar challenges specifically related to deployment.

## Others
### Third Party API limitation
[OpenWeatherMap](https://openweathermap.org/) API only support up to 60 calls within an hour. If you see an error in the website, this could mean that you have reached the limitation of API calls.

### Heroku limitation
Heroku's free tier hosting server will sleep the server after 30 minutes of
inactivity, hence the website could take a couple minute to load up.

## Credit
- Flask Tutorial : https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=5&ab_channel=CoreySchafer
- Weather icon: https://github.com/erikflowers/weather-icons
