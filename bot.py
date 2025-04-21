import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime, timedelta
import re
from typing import Dict, List, Optional
import asyncio
import motor.motor_asyncio
from pymongo import MongoClient
import itertools

load_dotenv()

LIGHT_PINK = 0xFFB6C1
FOOTER_TEXT = "programmed by **@bossmannn**"
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://caitbotdiscord:1ngyZvapJEBl6KOh@caitbot.cs5ao4g.mongodb.net/?retryWrites=true&w=majority&appName=caitbot')

# Status rotation list
STATUS_LIST = [
    ("listening", "caitlin"),
    ("watching", "banjer"),
    ("listening", "lana del ray w caitlin"),
    ("watching", "taylor swift on tt"),
    ("playing", "with banjer"),
    ("listening", "arctic monkeys w bossman")

]

# Countries with single timezone
COUNTRY_SINGLE_TIMEZONE = {
    "Argentina": "America/Argentina/Buenos_Aires",
    "Austria": "Europe/Vienna",
    "Bangladesh": "Asia/Dhaka",
    "Belgium": "Europe/Brussels",
    "Bulgaria": "Europe/Sofia",
    "Cambodia": "Asia/Phnom_Penh",
    "Chile": "America/Santiago",
    "Colombia": "America/Bogota",
    "Costa Rica": "America/Costa_Rica",
    "Croatia": "Europe/Zagreb",
    "Cuba": "America/Havana",
    "Czech Republic": "Europe/Prague",
    "Denmark": "Europe/Copenhagen",
    "Egypt": "Africa/Cairo",
    "El Salvador": "America/El_Salvador",
    "Ethiopia": "Africa/Addis_Ababa",
    "Finland": "Europe/Helsinki",
    "Germany": "Europe/Berlin",
    "Greece": "Europe/Athens",
    "Guatemala": "America/Guatemala",
    "Honduras": "America/Tegucigalpa",
    "Hong Kong": "Asia/Hong_Kong",
    "Hungary": "Europe/Budapest",
    "Iceland": "Atlantic/Reykjavik",
    "India": "Asia/Kolkata",
    "Iran": "Asia/Tehran",
    "Iraq": "Asia/Baghdad",
    "Ireland": "Europe/Dublin",
    "Israel": "Asia/Jerusalem",
    "Italy": "Europe/Rome",
    "Jamaica": "America/Jamaica",
    "Japan": "Asia/Tokyo",
    "Jordan": "Asia/Amman",
    "Kenya": "Africa/Nairobi",
    "Kuwait": "Asia/Kuwait",
    "Lebanon": "Asia/Beirut",
    "Luxembourg": "Europe/Luxembourg",
    "Malaysia": "Asia/Kuala_Lumpur",
    "Malta": "Europe/Malta",
    "Morocco": "Africa/Casablanca",
    "Myanmar": "Asia/Yangon",
    "Nepal": "Asia/Kathmandu",
    "Netherlands": "Europe/Amsterdam",
    "New Zealand": "Pacific/Auckland",
    "Nigeria": "Africa/Lagos",
    "Norway": "Europe/Oslo",
    "Oman": "Asia/Muscat",
    "Pakistan": "Asia/Karachi",
    "Panama": "America/Panama",
    "Paraguay": "America/Asuncion",
    "Peru": "America/Lima",
    "Philippines": "Asia/Manila",
    "Poland": "Europe/Warsaw",
    "Qatar": "Asia/Qatar",
    "Romania": "Europe/Bucharest",
    "Saudi Arabia": "Asia/Riyadh",
    "Serbia": "Europe/Belgrade",
    "Singapore": "Asia/Singapore",
    "Slovakia": "Europe/Bratislava",
    "Slovenia": "Europe/Ljubljana",
    "South Africa": "Africa/Johannesburg",
    "South Korea": "Asia/Seoul",
    "Sri Lanka": "Asia/Colombo",
    "Sweden": "Europe/Stockholm",
    "Switzerland": "Europe/Zurich",
    "Syria": "Asia/Damascus",
    "Taiwan": "Asia/Taipei",
    "Thailand": "Asia/Bangkok",
    "Tunisia": "Africa/Tunis",
    "Turkey": "Europe/Istanbul",
    "Uganda": "Africa/Kampala",
    "Ukraine": "Europe/Kiev",
    "United Arab Emirates": "Asia/Dubai",
    "Uruguay": "America/Montevideo",
    "Venezuela": "America/Caracas",
    "Vietnam": "Asia/Ho_Chi_Minh",
    "Yemen": "Asia/Aden",
    "Zimbabwe": "Africa/Harare",
}

# Countries with multiple timezones
COUNTRY_MULTI_TIMEZONE = {
    "United States": {
        # Eastern Time
        "New York": "America/New_York",
        "Washington DC": "America/New_York",
        "Boston": "America/New_York",
        "Philadelphia": "America/New_York",
        "Miami": "America/New_York",
        "Atlanta": "America/New_York",
        # Central Time
        "Chicago": "America/Chicago",
        "Houston": "America/Chicago",
        "Dallas": "America/Chicago",
        "Minneapolis": "America/Chicago",
        "New Orleans": "America/Chicago",
        # Mountain Time
        "Denver": "America/Denver",
        "Phoenix": "America/Phoenix",  # Note: Arizona doesn't observe DST
        "Salt Lake City": "America/Denver",
        # Pacific Time
        "Los Angeles": "America/Los_Angeles",
        "San Francisco": "America/Los_Angeles",
        "Seattle": "America/Los_Angeles",
        "Portland": "America/Los_Angeles",
        "Las Vegas": "America/Los_Angeles",
        # Alaska Time
        "Anchorage": "America/Anchorage",
        # Hawaii Time
        "Honolulu": "Pacific/Honolulu",
    },
    "Canada": {
        # Eastern Time
        "Toronto": "America/Toronto",
        "Ottawa": "America/Toronto",
        # Atlantic Time
        "Halifax": "America/Halifax",
        # Newfoundland Time
        "St. John's": "America/St_Johns",
        # Central Time
        "Winnipeg": "America/Winnipeg",
        # Mountain Time
        "Calgary": "America/Edmonton",
        "Edmonton": "America/Edmonton",
        # Pacific Time
        "Vancouver": "America/Vancouver",
    },
    "Russia": {
        "Moscow": "Europe/Moscow",
        "Saint Petersburg": "Europe/Moscow",
        "Kaliningrad": "Europe/Kaliningrad",
        "Samara": "Europe/Samara",
        "Yekaterinburg": "Asia/Yekaterinburg",
        "Omsk": "Asia/Omsk",
        "Novosibirsk": "Asia/Novosibirsk",
        "Krasnoyarsk": "Asia/Krasnoyarsk",
        "Irkutsk": "Asia/Irkutsk",
        "Yakutsk": "Asia/Yakutsk",
        "Vladivostok": "Asia/Vladivostok",
        "Magadan": "Asia/Magadan",
        "Kamchatka": "Asia/Kamchatka",
    },
    "Australia": {
        # Eastern Time
        "Sydney": "Australia/Sydney",
        "Melbourne": "Australia/Melbourne",
        "Canberra": "Australia/Sydney",
        "Tasmania": "Australia/Hobart",
        # Central Time
        "Adelaide": "Australia/Adelaide",
        "Darwin": "Australia/Darwin",
        # Western Time
        "Perth": "Australia/Perth",
        # Queensland (No DST)
        "Brisbane": "Australia/Brisbane",
    },
    "Brazil": {
        "São Paulo": "America/Sao_Paulo",
        "Rio de Janeiro": "America/Sao_Paulo",
        "Brasília": "America/Sao_Paulo",
        "Salvador": "America/Bahia",
        "Fortaleza": "America/Fortaleza",
        "Manaus": "America/Manaus",
        "Porto Alegre": "America/Sao_Paulo",
        "Recife": "America/Recife",
        "Belém": "America/Belem",
        "Campo Grande": "America/Campo_Grande",
        "Cuiabá": "America/Cuiaba",
        "Porto Velho": "America/Porto_Velho",
        "Rio Branco": "America/Rio_Branco",
        "Boa Vista": "America/Boa_Vista",
        "Macapá": "America/Macapa",
        "Palmas": "America/Araguaina",
        "Fernando de Noronha": "America/Noronha",
    },
    "Mexico": {
        "Mexico City": "America/Mexico_City",
        "Cancún": "America/Cancun",
        "Tijuana": "America/Tijuana",
        "Hermosillo": "America/Hermosillo",
        "Chihuahua": "America/Chihuahua",
        "Monterrey": "America/Monterrey",
    },
    "China": {
        "Beijing": "Asia/Shanghai",  # All of China uses one timezone
        "Shanghai": "Asia/Shanghai",
        "Guangzhou": "Asia/Shanghai",
        "Shenzhen": "Asia/Shanghai",
        "Chengdu": "Asia/Shanghai",
        "Hong Kong": "Asia/Hong_Kong",
        "Macau": "Asia/Macau",
    },
    "Indonesia": {
        "Jakarta": "Asia/Jakarta",
        "Bali": "Asia/Makassar",
        "Surabaya": "Asia/Jakarta",
        "Papua": "Asia/Jayapura",
    },
    "Kazakhstan": {
        "Astana": "Asia/Almaty",
        "Almaty": "Asia/Almaty",
        "Aktau": "Asia/Aqtau",
        "Aktobe": "Asia/Aqtobe",
        "Oral": "Asia/Oral",
    },
    "Mongolia": {
        "Ulaanbaatar": "Asia/Ulaanbaatar",
        "Hovd": "Asia/Hovd",
        "Choibalsan": "Asia/Choibalsan",
    },
    "Spain": {
        "Madrid": "Europe/Madrid",
        "Barcelona": "Europe/Madrid",
        "Canary Islands": "Atlantic/Canary",
    },
    "Portugal": {
        "Lisbon": "Europe/Lisbon",
        "Azores": "Atlantic/Azores",
    },
    "United Kingdom": {
        "London": "Europe/London",
        "Edinburgh": "Europe/London",
        "Cardiff": "Europe/London",
        "Belfast": "Europe/London",
    },
    "France": {
        "Paris": "Europe/Paris",
        "Tahiti": "Pacific/Tahiti",
        "Martinique": "America/Martinique",
        "Guadeloupe": "America/Guadeloupe",
        "Reunion": "Indian/Reunion",
        "New Caledonia": "Pacific/Noumea",
    },
    "Chile": {
        "Santiago": "America/Santiago",
        "Easter Island": "Pacific/Easter",
        "Punta Arenas": "America/Punta_Arenas",
    },
    "Antarctica": {
        "McMurdo": "Antarctica/McMurdo",
        "Casey": "Antarctica/Casey",
        "Davis": "Antarctica/Davis",
        "Mawson": "Antarctica/Mawson",
        "Palmer": "Antarctica/Palmer",
        "Rothera": "Antarctica/Rothera",
        "Syowa": "Antarctica/Syowa",
        "Troll": "Antarctica/Troll",
        "Vostok": "Antarctica/Vostok",
    },
    "Greenland": {
        "Nuuk": "America/Godthab",
        "Danmarkshavn": "America/Danmarkshavn",
        "Scoresbysund": "America/Scoresbysund",
        "Thule": "America/Thule",
    },
    "Micronesia": {
        "Pohnpei": "Pacific/Ponape",
        "Chuuk": "Pacific/Chuuk",
        "Kosrae": "Pacific/Kosrae",
    },
    "Ecuador": {
        "Quito": "America/Guayaquil",
        "Galapagos": "Pacific/Galapagos",
    },
    "Kiribati": {
        "Tarawa": "Pacific/Tarawa",
        "Enderbury": "Pacific/Enderbury",
        "Kiritimati": "Pacific/Kiritimati",
    },
    "Democratic Republic of the Congo": {
        "Kinshasa": "Africa/Kinshasa",
        "Lubumbashi": "Africa/Lubumbashi",
    },
}

class CaitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True  # Enable message events
        super().__init__(command_prefix='/', intents=intents, help_command=None)
        self.db = None
        self.timezones_collection = None
        self.status_cycle = itertools.cycle(STATUS_LIST)
        
    async def setup_mongodb(self):
        """Setup MongoDB connection"""
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.db = client.caitbot
        self.timezones_collection = self.db.timezones
        
    async def get_user_timezone(self, user_id: int) -> Optional[str]:
        """Get user timezone from MongoDB"""
        if self.db is None:
            await self.setup_mongodb()
        
        user_data = await self.timezones_collection.find_one({"user_id": user_id})
        return user_data.get("timezone") if user_data else None
    
    async def set_user_timezone(self, user_id: int, timezone: str):
        """Save user timezone to MongoDB"""
        if self.db is None:
            await self.setup_mongodb()
        
        await self.timezones_collection.update_one(
            {"user_id": user_id},
            {"$set": {"timezone": timezone}},
            upsert=True
        )
        
    async def setup_hook(self):
        # Setup MongoDB connection
        await self.setup_mongodb()
        # Deploy commands globally
        await self.tree.sync()
        # Start the status rotation task
        self.status_rotator.start()
        
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="caitlin"))
        print(f'logged in as {self.user}')
        print(f'deployed slash commands globally')
    
    @tasks.loop(minutes=5)
    async def status_rotator(self):
        status_type, name = next(self.status_cycle)
        
        if status_type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
        elif status_type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        elif status_type == "playing":
            activity = discord.Activity(type=discord.ActivityType.playing, name=name)
        
        await self.change_presence(activity=activity)
    
    @status_rotator.before_loop
    async def before_status_rotator(self):
        await self.wait_until_ready()
    
    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return
        
        # Don't respond to bots
        if message.author.bot:
            return
        
        # Check if user has timezone set
        user_timezone_str = await self.get_user_timezone(message.author.id)
        if not user_timezone_str:
            return
        
        # Look for time patterns in the message
        time_patterns = [
            # 24-hour format with colon
            r'\b(\d{1,2}):(\d{2})\b',
            # 12-hour format with AM/PM
            r'\b(\d{1,2}):(\d{2})\s*([aApP][mM])\b',
            # Single number (hours only, assumed 24-hour)
            r'\b(\d{1,2})\s*([aApP][mM])\b',
            # Single number between 0-23 (24-hour)
            r'\b(0?\d|1\d|2[0-3])\b(?![\d:])',
            # Single number 1-12 with AM/PM
            r'\b(1[0-2]|0?[1-9])\s*([aApP][mM])\b'
        ]
        
        times_found = []
        content = message.content
        
        # Check each pattern
        for pattern in time_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Parse the time from the match
                time_str = match.group(0)
                parsed_time = parse_time(time_str)
                
                if parsed_time:
                    # Create timezone objects
                    user_timezone = pytz.timezone(user_timezone_str)
                    
                    # Localize the time to user's timezone
                    local_time = user_timezone.localize(parsed_time)
                    
                    # Convert to UTC timestamp for Discord's dynamic time format
                    utc_time = local_time.astimezone(pytz.UTC)
                    timestamp = int(utc_time.timestamp())
                    
                    # Format the time
                    formatted_time = local_time.strftime("%H:%M")
                    timezone_abbr = local_time.strftime("%Z")
                    
                    times_found.append({
                        'original': time_str,
                        'formatted': formatted_time,
                        'timezone': timezone_abbr,
                        'timestamp': timestamp
                    })
        
        # If we found any times, respond with conversion
        if times_found:
            # Remove duplicates
            unique_times = []
            seen_timestamps = set()
            
            for time_info in times_found:
                if time_info['timestamp'] not in seen_timestamps:
                    seen_timestamps.add(time_info['timestamp'])
                    unique_times.append(time_info)
            
            # Create response embed
            embed = create_embed("time conversion", "")
            
            description = ""
            for time_info in unique_times:
                description += f"**above time ({time_info['formatted']} {time_info['timezone']}) in your local time** • <t:{time_info['timestamp']}:t>\n"
            
            embed.description = description.strip()
            
            # Reply to the original message
            await message.reply(embed=embed, mention_author=False)

bot = CaitBot()

# Weight conversion factors with both directions
WEIGHT_CONVERSIONS = {
    'kg_to_lbs': 2.20462,
    'lbs_to_kg': 0.453592,
    'g_to_oz': 0.035274,
    'oz_to_g': 28.3495,
    'stone_to_kg': 6.35029,
    'kg_to_stone': 0.157473,
    'stone_to_lbs': 14,
    'lbs_to_stone': 0.0714286,
    'tonne_to_ton': 1.10231,
    'ton_to_tonne': 0.907185,
    'mg_to_g': 0.001,
    'g_to_mg': 1000,
    'kg_to_oz': 35.274,
    'oz_to_kg': 0.0283495,
    'g_to_kg': 0.001,
    'kg_to_g': 1000,
    'tonne_to_kg': 1000,
    'kg_to_tonne': 0.001,
    'ton_to_lbs': 2000,
    'lbs_to_ton': 0.0005,
    'tonne_to_lbs': 2204.62,
    'lbs_to_tonne': 0.000453592,
    'ton_to_kg': 907.185,
    'kg_to_ton': 0.00110231,
}

# Length conversion factors with both directions
LENGTH_CONVERSIONS = {
    'cm_to_inch': 0.393701,
    'inch_to_cm': 2.54,
    'm_to_ft': 3.28084,
    'ft_to_m': 0.3048,
    'km_to_mile': 0.621371,
    'mile_to_km': 1.60934,
    'mm_to_inch': 0.0393701,
    'inch_to_mm': 25.4,
    'yard_to_m': 0.9144,
    'm_to_yard': 1.09361,
    'ft_to_inch': 12,
    'inch_to_ft': 0.0833333,
    'cm_to_m': 0.01,
    'm_to_cm': 100,
    'mm_to_cm': 0.1,
    'cm_to_mm': 10,
    'nm_to_mile': 1.15078,
    'mile_to_nm': 0.868976,
    'km_to_m': 1000,
    'm_to_km': 0.001,
    'mm_to_m': 0.001,
    'm_to_mm': 1000,
    'yard_to_ft': 3,
    'ft_to_yard': 0.333333,
    'mile_to_ft': 5280,
    'ft_to_mile': 0.000189394,
    'km_to_ft': 3280.84,
    'ft_to_km': 0.0003048,
    'cm_to_ft': 0.0328084,
    'ft_to_cm': 30.48,
    'mm_to_ft': 0.00328084,
    'ft_to_mm': 304.8,
    'yard_to_inch': 36,
    'inch_to_yard': 0.0277778,
    'mile_to_yard': 1760,
    'yard_to_mile': 0.000568182,
    'km_to_yard': 1093.61,
    'yard_to_km': 0.0009144,
    'cm_to_yard': 0.0109361,
    'yard_to_cm': 91.44,
    'mm_to_yard': 0.00109361,
    'yard_to_mm': 914.4,
}

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=LIGHT_PINK)
    embed.set_footer(text=FOOTER_TEXT)
    return embed

def parse_time(time_str):
    """Parse various time formats and return datetime object"""
    # Remove any extra spaces
    time_str = time_str.strip()
    
    # Patterns for different time formats
    patterns = [
        # 24-hour format with colon
        (r'^(\d{1,2}):(\d{2})$', '%H:%M'),
        # 12-hour format with AM/PM
        (r'^(\d{1,2}):(\d{2})\s*([aApP][mM])$', '%I:%M %p'),
        # Single number (hours only, assumed 24-hour)
        (r'^(\d{1,2})$', '%H'),
        # Single number with AM/PM
        (r'^(\d{1,2})\s*([aApP][mM])$', '%I %p')
    ]
    
    now = datetime.now()
    
    # First, check if it's just a number between 0-23 (24-hour format)
    try:
        hour = int(time_str)
        if 0 <= hour <= 23:
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
    except ValueError:
        pass
    
    for pattern, time_format in patterns:
        match = re.match(pattern, time_str)
        if match:
            try:
                if pattern == r'^(\d{1,2})$':  # Hour only (24-hour)
                    hour = int(match.group(1))
                    if 0 <= hour <= 23:
                        return now.replace(hour=hour, minute=0, second=0, microsecond=0)
                elif pattern == r'^(\d{1,2})\s*([aApP][mM])$':  # Hour + AM/PM
                    parsed_time = datetime.strptime(time_str, time_format)
                    return now.replace(hour=parsed_time.hour, minute=0, second=0, microsecond=0)
                else:  # Full format with minutes
                    parsed_time = datetime.strptime(time_str, time_format)
                    return now.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0)
            except ValueError:
                continue
    
    return None

def get_all_cities():
    """Get all cities from both single timezone and multi timezone countries"""
    cities = []
    
    # Add cities from multi-timezone countries
    for country_cities in COUNTRY_MULTI_TIMEZONE.values():
        cities.extend(country_cities.keys())
    
    return cities

def find_city_timezone(city_name):
    """Find timezone for a city from all available data"""
    # Check in multi-timezone countries
    for country_cities in COUNTRY_MULTI_TIMEZONE.values():
        if city_name in country_cities:
            return country_cities[city_name]
    
    return None

async def timezone_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    all_timezones = pytz.all_timezones
    
    if not current:
        # Show some common timezones when nothing is typed
        common_timezones = [
            'America/New_York',
            'America/Los_Angeles',
            'America/Chicago',
            'Europe/London',
            'Europe/Paris',
            'Europe/Berlin',
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Australia/Sydney',
            'UTC'
        ]
        return [
            app_commands.Choice(name=tz, value=tz)
            for tz in common_timezones
        ][:25]
    
    # Filter timezones based on current input
    matches = [tz for tz in all_timezones if current.lower() in tz.lower()]
    return [
        app_commands.Choice(name=tz, value=tz)
        for tz in matches
    ][:25]  # Discord limits to 25 choices

async def city_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    all_cities = get_all_cities()
    
    if not current:
        # Show some major cities when nothing is typed
        major_cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Dubai", "Singapore", "Toronto", "Berlin", "Rome"]
        return [
            app_commands.Choice(name=city, value=city)
            for city in major_cities
        ][:25]
    
    # Filter cities based on current input
    matches = [city for city in all_cities if current.lower() in city.lower()]
    return [
        app_commands.Choice(name=city, value=city)
        for city in matches
    ][:25]

async def country_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    all_countries = list(COUNTRY_SINGLE_TIMEZONE.keys()) + list(COUNTRY_MULTI_TIMEZONE.keys())
    
    if not current:
        # Show some common countries when nothing is typed
        common_countries = ["United States", "United Kingdom", "Canada", "Australia", "Japan", "Germany", "France", "China", "India", "Brazil"]
        return [
            app_commands.Choice(name=country, value=country)
            for country in common_countries
        ][:25]
    
    # Filter countries based on current input
    matches = [country for country in all_countries if current.lower() in country.lower()]
    return [
        app_commands.Choice(name=country, value=country)
        for country in matches
    ][:25]

@bot.tree.command(name="convert", description="convert between different units")
@app_commands.describe(
    category="the category of conversion (length/weight)", 
    value="the value to convert",
    from_unit="the unit you're converting from",
    to_unit="the unit you're converting to"
)
@app_commands.choices(
    category=[
        app_commands.Choice(name="length", value="length"),
        app_commands.Choice(name="weight", value="weight")
    ]
)
async def convert(interaction: discord.Interaction, category: app_commands.Choice[str], value: float, from_unit: str, to_unit: str):
    category_value = category.value.lower()
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Add support for variations of unit names
    unit_variations = {
        'meter': 'm',
        'meters': 'm',
        'metre': 'm',
        'metres': 'm',
        'centimeter': 'cm',
        'centimeters': 'cm',
        'centimetre': 'cm',
        'centimetres': 'cm',
        'millimeter': 'mm',
        'millimeters': 'mm',
        'millimetre': 'mm',
        'millimetres': 'mm',
        'kilometer': 'km',
        'kilometers': 'km',
        'kilometre': 'km',
        'kilometres': 'km',
        'inches': 'inch',
        'feet': 'ft',
        'foot': 'ft',
        'yards': 'yard',
        'miles': 'mile',
        'nmi': 'nm',
        'nautical mile': 'nm',
        'nautical miles': 'nm',
        'in': 'inch',
        'mi': 'mile',
        'yd': 'yard',
        'yds': 'yard',
        
        'kilogram': 'kg',
        'kilograms': 'kg',
        'kilo': 'kg',
        'kilos': 'kg',
        'gram': 'g',
        'grams': 'g',
        'milligram': 'mg',
        'milligrams': 'mg',
        'pound': 'lbs',
        'pounds': 'lbs',
        'lb': 'lbs',
        'ounce': 'oz',
        'ounces': 'oz',
        'stones': 'stone',
        'metric ton': 'tonne',
        'metric tons': 'tonne',
        'tonnes': 'tonne',
        'us ton': 'ton',
        'us tons': 'ton',
        'tons': 'ton',
        't': 'tonne',
        'st': 'stone',
    }
    
    # Convert unit variations to standard unit names
    from_unit = unit_variations.get(from_unit, from_unit)
    to_unit = unit_variations.get(to_unit, to_unit)
    
    # Handle same unit conversions
    if from_unit == to_unit:
        embed = create_embed("conversion result", f"{value} {from_unit} = {value} {to_unit}")
        await interaction.response.send_message(embed=embed)
        return
    
    if category_value == "length":
        conversion_key = f"{from_unit}_to_{to_unit}"
        
        # Try direct conversion
        if conversion_key in LENGTH_CONVERSIONS:
            result = value * LENGTH_CONVERSIONS[conversion_key]
        else:
            # Try finding an indirect conversion path through meters
            from_to_m = f"{from_unit}_to_m"
            m_to_target = f"m_to_{to_unit}"
            
            if from_to_m in LENGTH_CONVERSIONS and m_to_target in LENGTH_CONVERSIONS:
                result = value * LENGTH_CONVERSIONS[from_to_m] * LENGTH_CONVERSIONS[m_to_target]
            else:
                embed = create_embed("error", f"conversion from {from_unit} to {to_unit} not supported")
                await interaction.response.send_message(embed=embed)
                return
        
        # Format result based on magnitude
        if result < 0.01:
            formatted_result = f"{result:.6f}"
        elif result < 1:
            formatted_result = f"{result:.4f}"
        elif result < 100:
            formatted_result = f"{result:.2f}"
        else:
            formatted_result = f"{result:.1f}"
        embed = create_embed("conversion result", f"{value} {from_unit} = {formatted_result} {to_unit}")
    
    elif category_value == "weight":
        conversion_key = f"{from_unit}_to_{to_unit}"
        
        # Try direct conversion
        if conversion_key in WEIGHT_CONVERSIONS:
            result = value * WEIGHT_CONVERSIONS[conversion_key]
        else:
            # Try finding an indirect conversion path through kilograms
            from_to_kg = f"{from_unit}_to_kg"
            kg_to_target = f"kg_to_{to_unit}"
            
            if from_to_kg in WEIGHT_CONVERSIONS and kg_to_target in WEIGHT_CONVERSIONS:
                result = value * WEIGHT_CONVERSIONS[from_to_kg] * WEIGHT_CONVERSIONS[kg_to_target]
            else:
                embed = create_embed("error", f"conversion from {from_unit} to {to_unit} not supported")
                await interaction.response.send_message(embed=embed)
                return
        
        # Format result based on magnitude
        if result < 0.01:
            formatted_result = f"{result:.6f}"
        elif result < 1:
            formatted_result = f"{result:.4f}"
        elif result < 100:
            formatted_result = f"{result:.2f}"
        else:
            formatted_result = f"{result:.1f}"
        embed = create_embed("conversion result", f"{value} {from_unit} = {formatted_result} {to_unit}")
    
    else:
        embed = create_embed("error", "please specify 'length' or 'weight' as the category")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="settimezone", description="set your timezone for time conversions")
@app_commands.describe(timezone="your timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')")
@app_commands.autocomplete(timezone=timezone_autocomplete)
async def settimezone(interaction: discord.Interaction, timezone: str):
    try:
        # Validate the timezone
        pytz.timezone(timezone)
        await bot.set_user_timezone(interaction.user.id, timezone)
        embed = create_embed("timezone set", f"your timezone has been set to {timezone}")
    except pytz.exceptions.UnknownTimeZoneError:
        embed = create_embed("error", f"'{timezone}' is not a valid timezone. please use a valid timezone like 'America/New_York' or 'Europe/London'")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mytimezone", description="show your currently set timezone")
async def mytimezone(interaction: discord.Interaction):
    user_timezone_str = await bot.get_user_timezone(interaction.user.id)
    
    if not user_timezone_str:
        embed = create_embed("timezone not set", "you haven't set your timezone yet. use /settimezone to set it.")
    else:
        embed = create_embed("your timezone", f"your current timezone is set to: **{user_timezone_str}**")
        
        # Show current time in user's timezone
        user_timezone = pytz.timezone(user_timezone_str)
        current_time = datetime.now(user_timezone)
        embed.add_field(
            name="current time",
            value=f"{current_time.strftime('%H:%M')} {current_time.strftime('%Z')}"
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="time", description="convert time between timezones with city/country selection")
@app_commands.describe(
    time="the time to convert (e.g., '7pm', '19:00', '14')",
    city="select a city (optional)",
    country="select a country (optional, will prompt for city if needed)",
    format="time format for output",
    direction="convert from your timezone to destination (to_destination) or vice versa (from_destination)"
)
@app_commands.choices(
    format=[
        app_commands.Choice(name="12-hour", value="12h"),
        app_commands.Choice(name="24-hour", value="24h")
    ],
    direction=[
        app_commands.Choice(name="to destination", value="to_destination"),
        app_commands.Choice(name="from destination", value="from_destination")
    ]
)
@app_commands.autocomplete(city=city_autocomplete, country=country_autocomplete)
async def time_convert(
    interaction: discord.Interaction, 
    time: str, 
    city: str = None,
    country: str = None,
    format: app_commands.Choice[str] = None,
    direction: app_commands.Choice[str] = None
):
    user_timezone_str = await bot.get_user_timezone(interaction.user.id)
    
    if not user_timezone_str:
        embed = create_embed("error", "please set your timezone first using /settimezone")
        await interaction.response.send_message(embed=embed)
        return
    
    parsed_time = parse_time(time)
    if not parsed_time:
        embed = create_embed("error", "invalid time format. please use formats like '7pm', '19:00', or '14'")
        await interaction.response.send_message(embed=embed)
        return
    
    # Default values
    time_format = format.value if format else "24h"
    conversion_direction = direction.value if direction else "to_destination"
    
    # Create timezone objects
    user_timezone = pytz.timezone(user_timezone_str)
    destination_name = None
    destination_timezone = None
    
    # Handle city selection
    if city:
        timezone_str = find_city_timezone(city)
        if timezone_str:
            destination_timezone = pytz.timezone(timezone_str)
            destination_name = city
        else:
            embed = create_embed("error", f"sorry, i don't have timezone information for {city}")
            await interaction.response.send_message(embed=embed)
            return
    
    # Handle country selection
    elif country:
        # Check if country has single timezone
        if country in COUNTRY_SINGLE_TIMEZONE:
            destination_timezone = pytz.timezone(COUNTRY_SINGLE_TIMEZONE[country])
            destination_name = country
        # Check if country has multiple timezones
        elif country in COUNTRY_MULTI_TIMEZONE:
            cities = list(COUNTRY_MULTI_TIMEZONE[country].keys())
            
            # If only one city for this country, use it directly
            if len(cities) == 1:
                city = cities[0]
                destination_timezone = pytz.timezone(COUNTRY_MULTI_TIMEZONE[country][city])
                destination_name = f"{city}, {country}"
            else:
                # Multiple cities, ask user to select one
                embed = create_embed(
                    "select a city",
                    f"{country} has multiple timezones. please select a city from the following:\n\n" +
                    ", ".join(cities) + 
                    "\n\nuse `/time` again with the city parameter filled in."
                )
                await interaction.response.send_message(embed=embed)
                return
        else:
            embed = create_embed("error", f"sorry, i don't have timezone information for {country}")
            await interaction.response.send_message(embed=embed)
            return
    
    # If no destination specified, use user's timezone
    if not destination_timezone:
        destination_timezone = user_timezone
        destination_name = "your time"
    
    # Handle conversion direction
    if conversion_direction == "from_destination" and destination_name != "your time":
        # Input time is in the destination timezone, convert to user's timezone
        source_timezone = destination_timezone
        target_timezone = user_timezone
        source_name = destination_name
        target_name = "your time"
    else:
        # Input time is in user's timezone, convert to destination timezone
        source_timezone = user_timezone
        target_timezone = destination_timezone
        source_name = "your time"
        target_name = destination_name
    
    # Properly handle DST by localizing the time
    source_time = source_timezone.localize(parsed_time)
    target_time = source_time.astimezone(target_timezone)
    
    # Convert to UTC timestamp for Discord's dynamic time format
    utc_time = source_time.astimezone(pytz.UTC)
    timestamp = int(utc_time.timestamp())
    
    # Format the time according to user preference
    if time_format == "12h":
        formatted_source = source_time.strftime("%I:%M %p")
        formatted_target = target_time.strftime("%I:%M %p")
    else:
        formatted_source = source_time.strftime("%H:%M")
        formatted_target = target_time.strftime("%H:%M")
    
    source_tz_abbr = source_time.strftime("%Z")
    target_tz_abbr = target_time.strftime("%Z")
    
    # Create the embed
    embed = create_embed(
        "time conversion",
        f"**{formatted_source} {source_tz_abbr} in {source_name}** is\n"
        f"**{formatted_target} {target_tz_abbr} in {target_name}**\n\n"
        f"Dynamic time: <t:{timestamp}:t>\n"
        f"Full date/time: <t:{timestamp}:F>"
    )
    
    # Add daylight saving time information
    if source_time.dst() != timedelta(0):
        embed.add_field(
            name="daylight saving time",
            value=f"{source_name} is currently observing daylight saving time",
            inline=False
        )
    
    if destination_name != "your time" and target_time.dst() != timedelta(0):
        embed.add_field(
            name="daylight saving time",
            value=f"{target_name} is currently observing daylight saving time",
            inline=False
        )
    
    # Add more timestamp formats
    embed.add_field(
        name="different formats",
        value=f"Short time: <t:{timestamp}:t>\n"
              f"Long time: <t:{timestamp}:T>\n"
              f"Short date: <t:{timestamp}:d>\n"
              f"Long date: <t:{timestamp}:D>\n"
              f"Short date/time: <t:{timestamp}:f>\n"
              f"Long date/time: <t:{timestamp}:F>\n"
              f"Relative: <t:{timestamp}:R>",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="deploy", description="deploy slash commands (bossman only)")
@app_commands.describe(
    scope="where to deploy commands",
    guild_id="guild ID for specific server deployment (required for 'specific' scope)"
)
@app_commands.choices(
    scope=[
        app_commands.Choice(name="current server", value="current"),
        app_commands.Choice(name="specific server", value="specific"),
        app_commands.Choice(name="global", value="global")
    ]
)
async def deploy(interaction: discord.Interaction, scope: app_commands.Choice[str], guild_id: str = None):
    if interaction.user.id != int(os.getenv('BOT_OWNER_ID', '0')):
        embed = create_embed("error", "only the bossman can use this command")
        await interaction.response.send_message(embed=embed)
        return
    
    # Defer the response immediately
    await interaction.response.defer()
    
    try:
        if scope.value == "current":
            # Deploy to current guild
            await bot.tree.sync(guild=interaction.guild)
            embed = create_embed("success", f"slash commands deployed to {interaction.guild.name}")
        
        elif scope.value == "specific":
            # Deploy to specific guild
            if not guild_id:
                embed = create_embed("error", "guild ID is required for specific server deployment")
                await interaction.followup.send(embed=embed)
                return
            
            try:
                guild = bot.get_guild(int(guild_id))
                if not guild:
                    embed = create_embed("error", f"could not find guild with ID {guild_id}")
                    await interaction.followup.send(embed=embed)
                    return
                
                await bot.tree.sync(guild=guild)
                embed = create_embed("success", f"slash commands deployed to {guild.name}")
            except ValueError:
                embed = create_embed("error", "invalid guild ID format")
                await interaction.followup.send(embed=embed)
                return
        
        elif scope.value == "global":
            # Deploy globally
            await bot.tree.sync()
            embed = create_embed("success", "slash commands deployed globally")
    
    except Exception as e:
        embed = create_embed("error", f"failed to deploy commands: {str(e)}")
    
    # Use followup.send since we deferred the response
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="undeploy", description="remove slash commands (bossman only)")
@app_commands.describe(
    scope="where to remove commands from",
    guild_id="guild ID for specific server undeployment (required for 'specific' scope)"
)
@app_commands.choices(
    scope=[
        app_commands.Choice(name="current server", value="current"),
        app_commands.Choice(name="specific server", value="specific"),
        app_commands.Choice(name="global", value="global")
    ]
)
async def undeploy(interaction: discord.Interaction, scope: app_commands.Choice[str], guild_id: str = None):
    if interaction.user.id != int(os.getenv('BOT_OWNER_ID', '0')):
        embed = create_embed("error", "only the bossman can use this command")
        await interaction.response.send_message(embed=embed)
        return
    
    # Defer the response immediately
    await interaction.response.defer()
    
    try:
        if scope.value == "current":
            # Remove from current guild
            bot.tree.clear_commands(guild=interaction.guild)
            await bot.tree.sync(guild=interaction.guild)
            embed = create_embed("success", f"slash commands removed from {interaction.guild.name}")
        
        elif scope.value == "specific":
            # Remove from specific guild
            if not guild_id:
                embed = create_embed("error", "guild ID is required for specific server undeployment")
                await interaction.followup.send(embed=embed)
                return
            
            try:
                guild = bot.get_guild(int(guild_id))
                if not guild:
                    embed = create_embed("error", f"could not find guild with ID {guild_id}")
                    await interaction.followup.send(embed=embed)
                    return
                
                bot.tree.clear_commands(guild=guild)
                await bot.tree.sync(guild=guild)
                embed = create_embed("success", f"slash commands removed from {guild.name}")
            except ValueError:
                embed = create_embed("error", "invalid guild ID format")
                await interaction.followup.send(embed=embed)
                return
        
        elif scope.value == "global":
            # Remove globally
            bot.tree.clear_commands(guild=None)
            await bot.tree.sync()
            embed = create_embed("success", "slash commands removed globally")
    
    except Exception as e:
        embed = create_embed("error", f"failed to remove commands: {str(e)}")
    
    # Use followup.send since we deferred the response
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="help", description="show available commands and conversions")
async def help_command(interaction: discord.Interaction):
    embed = create_embed("caitbot help", "all available commands and conversions")
    
    embed.add_field(
        name="🔄 conversion commands",
        value="`/convert length <value> <from_unit> <to_unit>` - convert lengths\n"
              "`/convert weight <value> <from_unit> <to_unit>` - convert weights\n\n",
        inline=False
    )
    
    embed.add_field(
        name="⏰ time commands",
        value="`/settimezone <timezone>` - set your timezone\n"
              "`/mytimezone` - show your current timezone\n"
              "`/time <time> [city] [country] [format] [direction]` - convert time\n"
              "→ time: e.g., '7pm', '19:00', '14'\n"
              "→ city: select specific city for conversion\n"
              "→ country: select country (will prompt for city if multiple timezones)\n"
              "→ format: '12h' or '24h' (default: 24h)\n"
              "→ direction: 'to destination' or 'from destination' (default: to destination)\n\n",
        inline=False
    )
    
    embed.add_field(
        name="🌍 timezone information",
        value="• Countries with single timezone: Direct conversion\n"
              "• Countries with multiple timezones: City selection required\n"
              "• Over 100 cities and 80+ countries supported",
        inline=False
    )
    
    embed.add_field(
        name="📏 supported length units",
        value="mm, cm, m, km, inch, ft, yard, mile, nm (nautical mile)",
        inline=False
    )
    
    embed.add_field(
        name="⚖️ supported weight units",
        value="mg, g, kg, oz, lbs, stone, ton, tonne",
        inline=False
    )
    
    embed.add_field(
        name="🕐 time formats",
        value="24-hour: '14', '14:00'\n"
              "12-hour: '2pm', '2:00 pm'",
        inline=False
    )
    
    if interaction.user.id == int(os.getenv('BOT_OWNER_ID', '0')):
        embed.add_field(
            name="👑 bossman's commands",
            value="`/deploy <scope> [guild_id]` - deploy commands to current/specific server or globally\n"
                  "`/undeploy <scope> [guild_id]` - remove commands from current/specific server or globally\n"
                  "scopes: 'current server', 'specific server', 'global'",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))