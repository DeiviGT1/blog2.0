# Song Recommender and Analyzer

Welcome to the **Song Recommender and Analyzer**, a dynamic Flask application that not only recommends songs similar to your favorite tracks but also provides a unique twist by analyzing and displaying real Spotify song data. This application seamlessly combines the power of the Spotify and OpenAI APIs for an immersive and personalized music exploration experience. Let's dive into the features and steps to get started.

## Features 🎶

- **User Authentication:** Log in securely with your Spotify account to access personalized song recommendations.

- **Song Recommendation Generation:** Utilizing the OpenAI API, the app generates a curated list of songs similar to your input, considering lyrics, genre, artist, and popularity.

- **Real Spotify Data Analysis:** After receiving song recommendations, the application fetches real Spotify data, including song name, artist, image, and URL, enhancing your exploration.

## Prerequisites 🛠️

Before embarking on your musical journey, make sure you have the following:

- **Python:** Install Python on your system to power the application.

- **Flask:** A simple command (`pip install Flask`) sets the stage for a seamless web framework experience.

- **OpenAI API Key:** Obtain your OpenAI API key by creating an account and following the provided instructions.

- **Spotify API Credentials:** Obtain your Spotify API credentials by creating a Spotify Developer account and registering a new application.

## Installation 🚀

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/song-recommender-analyzer.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd song-recommender-analyzer
   ```

3. **Set Up API Credentials:**
   - Open the `.env` file and replace `YOUR_OPENAI_API_KEY`, `YOUR_SPOTIFY_CLIENT_ID`, and `YOUR_SPOTIFY_CLIENT_SECRET` with your actual API credentials.

4. **Run the Application:**
   ```bash
   python app.py
   ```

5. **Access the Application:**
   Open your web browser and go to [http://localhost:5000](http://localhost:5000) to embark on a musical adventure.

## Usage 🎉

1. **Login:**
   - Click on the "Login" link to securely authenticate with your Spotify account.

2. **Input Song Details:**
   - Enter the name of a song and the corresponding artist to receive personalized song recommendations.

3. **Explore Recommendations:**
   - Explore the generated song recommendations presented in a visually appealing format.

4. **Real Spotify Data:**
   - Dive deeper into the recommended songs by viewing real Spotify data, including song name, artist, image, and URL.

## Contributors 🤝

- [David](https://github.com/deivigt1): Project Lead
