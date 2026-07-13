import csv
import requests
from bs4 import BeautifulSoup

def access_weather_api():
    METEO = ("https://api.open-meteo.com/v1/forecast?latitude=51.75&longitude=-1.26"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
            "&timezone=Europe/London&forecast_days=7")
    daily = requests.get(METEO, timeout=30).json()["daily"]
    with open("oxford_weather.csv", "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows([["Date", "Max temp C", "Min temp C", "Rain chance %"],
                                *zip(daily["time"], daily["temperature_2m_max"],
                                    daily["temperature_2m_min"], daily["precipitation_probability_max"])])
    print("Saved oxford_weather.csv")


def scrape_oxuni_events():
    html = requests.get("https://events.ox.ac.uk/events?tab=nextweek",
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
    rows = [["Title", "Date", "Time", "Venue", "Department", "Format"]]
    for event in BeautifulSoup(html, "html.parser").select("#nextweek .listing-item-oxford-event"):
        start = event.select_one("[itemprop=startDate]")["content"]  # e.g. 2026-07-13T09:00:00
        venue = event.select_one(".event-venues [itemprop=venue]")
        dept = event.select_one(".event-department span")
        fmt = [b.get_text(strip=True) for b in event.select(".badge") if "Format:" in b.text]
        rows.append([event.h2.get_text(strip=True), start[:10], start[11:16],
                    venue.get_text(strip=True) if venue else "Online / no venue",
                    dept.get_text(strip=True) if dept else "",
                    fmt[0].removeprefix("Format: ") if fmt else ""])

    with open("oxford_events.csv", "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows(rows)
    print(f"Saved oxford_events.csv ({len(rows) - 1} events)")


access_weather_api()
scrape_oxuni_events()