# Function Calling: Weather (OpenAI + OpenWeatherMap)

Small demo showing OpenAI **tool/function calling** that can fetch **current weather** from OpenWeatherMap by:

- **City name** (e.g. `q="Bengaluru"`)
- **ZIP/postal code + country code** using:
  `https://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={API key}`

## Setup

### 1) Create a virtualenv (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file (see `env.example`):

- `OPENAI_API_KEY`: your OpenAI API key
- `WEATHER_API_KEY`: your OpenWeatherMap API key
- `OPENAI_MODEL` (optional): model name (defaults to `gpt-4o-mini`)
- `DEBUG` (optional): set to `1` to print the raw assistant message (useful to see tool calls)

## Run

```bash
python3 main.py
```

Example prompts:

- “What’s the weather in Bengaluru in celsius?”
- “What’s the weather for zip 94040 in US in fahrenheit?”

## Notes

- The model may decide whether to call `get_weather` (city) or `get_weather_by_zip` (zip+country).
 

