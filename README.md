# Weather Flask Application
A flask application that shows weather forecast for any city at current time and in the next five days. The application performing API requests to a third party website, [OpenWeatherMap](https://openweathermap.org/).

The application was deployed with Heroku and hosted here:
https://weather-app100.herokuapp.com/

Features in development:
- Allow users to have their own account (feature-user-model branch)
- Allow users to save a list of favorite cities
- Allow users to modify the list of favorite cities

### Technologies Used
Flask, Bootstrap, HTML, CSS

### API limitation
OpenWeatherMap API supports 60 calls within an hour. 
If you see an error in the website, this could mean that you have 
reached the limitation of API calls.

### Heroku limitation
Heroku's free tier hosting server will sleep the server after 30 minutes of
inactivity. If it's your first time accessing the website please wait a 
couple minute for the server to load up.

## Credit
Weather icon: https://github.com/erikflowers/weather-icons