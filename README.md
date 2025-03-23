<h1 align="center">Rukia Bot</h1>

<p align="center">
  <a href="https://www.codefactor.io/repository/github/75efb6/rukia-bot"><img src="https://www.codefactor.io/repository/github/75efb6/rukia-bot/badge" alt="CodeFactor"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

Rukia Bot is a Python-based bot designed for a private server for osu!droid, using a server based on [this codebase](https://github.com/unclem2/osudroid-rx-server).

## Required

Ensure you have the following:

- An osu!v1 API key
- An existing server running
- A Discord Server

## Dependencies

Ensure you have the following dependencies installed:

- Latest Python version
- Nextcord Python package
- Dotenv Python package

## Setup

Follow these steps to get started with Rukia Bot:

1. **Configure Environment Variables**
   - Rename `.env.example` to `.env`.
   - Fill out the required fields in the `.env` file.

2. **Modify Configuration**
   - Update the necessary fields in `config.py` (fields not covered by `.env`).
   - Update emojis on player object for rank emojis.

3. **Run the Bot**
   - Execute `main.py` to start the bot and enjoy!

## Contributing

If you would like to contribute to the development of Rukia Bot, feel free to fork the repository and submit a pull request. Contributions are always welcome!

## License

Rukia Bot is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute this software in accordance with the license.

## Acknowledgments

- [unclem2](https://github.com/unclem2) for the osu!droid-rx-server codebase.
