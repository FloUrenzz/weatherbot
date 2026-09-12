import aiohttp
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL


async def get_current_weather(city: str, lang: str = "ru") -> str:
    """Запрашивает текущую погоду в городе."""
    url = f"{OPENWEATHER_BASE_URL}/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": lang
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                data = await response.json()
                if response.status != 200:
                    return f"⚠️ Ошибка: {data.get('message', 'Не удалось получить погоду')}"
                weather_desc = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                return (
                    f"🌤 Погода в городе *{city.title()}*:\n\n"
                    f"• {weather_desc}\n"
                    f"• Температура: {temp}°C\n"
                    f"• Ощущается как: {feels_like}°C\n"
                    f"• Влажность: {humidity}%\n"
                    f"• Ветер: {wind_speed} м/с\n"
                )
    except aiohttp.ClientError:
        return "⚠️ Ошибка при подключении к сервису погоды."


async def get_forecast_5days(city: str, lang: str = "ru") -> str:
    """Запрашивает 5-дневный прогноз погоды и группирует данные по дням."""
    url = f"{OPENWEATHER_BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": lang
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                data = await response.json()
                if response.status != 200:
                    return f"⚠️ Ошибка: {data.get('message', 'Не удалось получить прогноз')}"
                forecast_list = data.get("list", [])
                if not forecast_list:
                    return "⚠️ Нет данных прогноза."

                from collections import defaultdict
                grouped = defaultdict(list)
                for entry in forecast_list:
                    date = entry["dt_txt"].split(" ")[0]
                    grouped[date].append(entry)

                days = sorted(grouped.keys())
                from datetime import datetime
                lines = [f"📅 Прогноз погоды на 5 дней в *{city.title()}*:\n"]
                for day in days[:5]:
                    entries = grouped[day]
                    chosen = next((entry for entry in entries if "12:00:00" in entry["dt_txt"]), entries[0])
                    dt_obj = datetime.strptime(day, "%Y-%m-%d")
                    formatted_date = dt_obj.strftime("%d.%m.%Y")
                    desc = chosen["weather"][0]["description"].capitalize()
                    temp = chosen["main"]["temp"]
                    temp_min = chosen["main"]["temp_min"]
                    temp_max = chosen["main"]["temp_max"]
                    wind_speed = chosen["wind"]["speed"]
                    humidity = chosen["main"]["humidity"]
                    lines.append(
                        f"📍 *{formatted_date}*\n"
                        f"• {desc}\n"
                        f"• Температура: {temp}°C (мин: {temp_min}°C, макс: {temp_max}°C)\n"
                        f"• Влажность: {humidity}%\n"
                        f"• Ветер: {wind_speed} м/с\n"
                    )
                return "\n".join(lines)
    except aiohttp.ClientError:
        return "⚠️ Ошибка при подключении к сервису прогноза погоды."
