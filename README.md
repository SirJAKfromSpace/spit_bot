# SPIT - Spotipy Playlist Import Tool

```
     _____ _____  __ _____ 
    |   __|     ||  |_   _|
    |__   |   __||  | | |
    |_____|__|   |__| |_|
        
```

## Description

SPIT (Spotify Playlist Import Tool) is a command-line interface (CLI) tool designed to interact with the Spotify Web API to manage and analyze your Spotify music data. It allows users to fetch their most listened songs, liked songs, followed artists, and playlists directly from their Spotify accounts.

## What It Does

- **Fetch Data**: Retrieves data such as liked songs, followed artists, and user playlists using the Spotify Web API.
- **Data Analysis**: Provides basic analysis and display of fetched data, such as listing the most listened and liked songs.
- **Data Export**: Allows users to save fetched data into JSON or CSV formats for further use or analysis.

## Built With

- **Python**: The core programming language used.
- **Spotipy**: A lightweight Python library for the Spotify Web API.
- **Pandas**: For data manipulation and analysis.
- **Seaborn**: Used for data visualization (though not directly utilized in the main functionality).

## Setup & Requirements

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SPIT.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd SPIT
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start using SPIT, follow these steps:

1. Set up your Spotify API credentials in a `.env` file (client ID, client secret, and redirect URI).
2. Run the script:
   ```bash
   python main_runner.py
   ```
3. Follow the on-screen prompts to fetch and manage your Spotify data.

### Example Commands

- Fetch and save all liked songs:
  ```bash
  1  # Select option 1 from the menu
  ```

___

## Potential Roadmap

- **Extended Data Analysis Features**: Incorporate more complex data analysis capabilities.
- **Social Sharing Features**: Add options to share playlists and favorite tracks on social media.
- **GUI Implementation**: Develop a graphical user interface for easier interaction.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/) - Spotify Web API Python library
- [Pandas](https://pandas.pydata.org/) - Data analysis library
- [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization

Thank you to all the contributors who spend time and effort making SPIT better!

___