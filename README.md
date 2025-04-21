# caitbot

a discord bot that converts measurements, weight, and time across timezones with comprehensive city and country support.

## features

- convert measurements (cm, meter, feet, inches, etc.)
- convert weights (kg, lbs, stone, etc.)
- convert time with city/country selection and format choice
- automatically detects and converts time mentions in messages
- automatically handles daylight saving time transitions
- smart country detection: only asks for city when needed
- all responses in light pink embeds with dynamic discord timestamps
- slash commands only
- can be added to both user profiles and servers

## setup

1. create a `.env` file based on `.env.example`
2. add your discord bot token
3. add your discord user id for bossman commands
4. add your mongodb uri (or keep the default)
5. install requirements: `pip install -r requirements.txt`
6. run the bot: `python bot.py`

## commands

### conversion commands
- `/convert` - convert between units (length/weight)

### time commands
- `/settimezone` - set your timezone
- `/mytimezone` - show your current timezone
- `/time` - convert time with options:
  - `time`: e.g., "7pm", "19:00", "14"
  - `city`: select from 100+ cities (optional)
  - `country`: select from 80+ countries (optional)
  - `format`: choose 12-hour or 24-hour format (default: 24h)
  - `direction`: convert "to destination" or "from destination" (default: to destination)

### bossman's commands
- `/deploy` - deploy commands with different scopes (bossman only):
  - `current server` - deploy to the current server you're in
  - `specific server` - deploy to a specific server by ID
  - `global` - deploy commands globally to all servers
- `/undeploy` - remove commands with different scopes (bossman only):
  - `current server` - remove from current server
  - `specific server` - remove from a specific server by ID
  - `global` - remove globally from all servers

## features

### smart timezone handling
- countries with single timezone: direct conversion
- countries with multiple timezones: asks for city selection
- support for all major cities across different timezones
- automatic daylight saving time (summertime) transitions

### extensive coverage
- 80+ countries supported
- 100+ cities with precise timezone data
- handles edge cases like arizona (no dst), china (single timezone), and territories

### quality of life
- automatically detects time mentions in messages and converts them
- city and country autocomplete for easier selection
- persistent storage of user timezones in mongodb
- discord's dynamic timestamps show local time for everyone
- help command showing all supported conversions

### status rotation
the bot rotates between these statuses every 5 minutes:
- listening to caitlin
- watching banjer
- listening to lana del ray w caitlin
- watching taylor swift on tt
- playing with banjer
- listening to arctic monkeys w bossman

## deployment

the bot is set up for deployment on railway with a procfile included.

programmed by @bossmannn
