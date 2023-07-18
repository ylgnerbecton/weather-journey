import logging
import telebot
from app.application.adapters.open_weather_map_api import OpenWeatherMapAPI

from app.config import Settings

settings = Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherForecastBot:
    def __init__(self):
        self.bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
        self.weather_api = OpenWeatherMapAPI()
        self.city_requested = False
        logger.info("WeatherForecastBot initialized.")

    def run(self) -> None:
        self.register_handlers()
        self.bot.polling()
        logger.info("WeatherForecastBot started polling.")

    def register_handlers(self) -> None:
        @self.bot.message_handler(commands=["start"])
        def handle_start_command(message: telebot.types.Message) -> None:
            self.bot.reply_to(
                message,
                "Welcome to the Weather Forecast Bot! Please enter the city name to get the weather forecast.",
            )
            self.city_requested = True
            logger.info(f"Start command received from user {message.from_user.id}.")

        @self.bot.message_handler(func=lambda message: True)
        def handle_city_input(message: telebot.types.Message) -> None:
            if self.city_requested:
                city = message.text
                logger.info(f"City received from user {message.from_user.id}: {city}")
                try:
                    forecast_text, weather_data = self.weather_api.get_forecast_and_data(city)
                except:
                    forecast_text = None
                if forecast_text:
                    self.bot.reply_to(message, forecast_text)
                    logger.info(f"Weather data sent to user {message.from_user.id}.")
                else:
                    self.bot.reply_to(
                        message,
                        "Sorry, I couldn't retrieve the weather information for the specified city.",
                    )
                    logger.info(f"No weather data found for city {city}.")
                self.bot.reply_to(
                    message,
                    "Would you like to know the weather for another city? Please enter the city name.",
                )
            else:
                self.bot.reply_to(
                    message,
                    "Sorry, I didn't understand that command. Please enter a city name to get the weather forecast.",
                )
                self.city_requested = True
                logger.info(f"Unrecognized command from user {message.from_user.id}.")


weather_bot = WeatherForecastBot()
weather_bot.run()
