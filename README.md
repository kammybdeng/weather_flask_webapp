# Weather Forecast Application
A weather forecast application that allows users to search a city's weather and save their favorite cities. The application performs API calls to a third party resource to fetch for weather data. The backend is built with Flask and the frontend is built with JavaScript, Bootstrap, HTML, and CSS.

## Live site
https://weather-app100.herokuapp.com/


## Features
- User registration and login/logout
- Save and delete functionality
- User dashboard
- AJAX calls with jQuery

## Features in development:
- Ability to modify cities in dashboard
- Ability to use Google map to select location

## Others
### Third Party API limitation
[OpenWeatherMap](https://openweathermap.org/) API only support up to 60 calls within an hour. If you see an error in the website, this could mean that you have reached the limitation of API calls.

### Heroku limitation
Heroku's free tier hosting server will sleep the server after 30 minutes of
inactivity, hence the website could take a couple minute to load up.

## Credit
Weather icon: https://github.com/erikflowers/weather-icons
