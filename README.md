# Chord Progression Generator

**_A handy tool to automatically generate chord progressions based on a selected mood. Built with the Hooktheory API and Spotipy._**

## Dataset creation

1. Get an API key from https://www.hooktheory.com and add it to a file called `APIKey.txt`.

2. Obtain authentication to the Spotify API by creating the `SPOTIPY_CLIENT_ID` AND `SPOTIPY_CLIENT_SECRET` environment variables. They are availaible on the [Spotify for Developers Dashboard](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjt--viqqPtAhW8zDgGHWEcC2AQFjAAegQIARAD&url=https%3A%2F%2Fdeveloper.spotify.com%2Fdashboard%2F&usg=AOvVaw3zu9Io8tYd2ulT_6rKNkyc)

3. Run the dataset creation script:

   ```
   python3 fetch_progressions.py
   ```

   The dataset is created by first finding one chord progressions, discarding the progressions with low probability(< 0.05), finding two chord progressions from the previously obtained one chord progressions, discarding the low probability ones, and so on.

4. Run the database creation script with the following command:

   ```
   python3 mine_emotions.py
   ```

   > Note: only emotions for four chord progressions have been considered for ease of usage.

## Live Version

![Heroku](https://pyheroku-badge.herokuapp.com/?app=chord-progression-generator)

A simplified version with 50 chord progressions has been deployed to https://chord-progression-generator.herokuapp.com

## Resources

- [Hooktheory API](https://www.hooktheory.com/api/trends/docs) to fetch chord progression information
- [Spotify API](https://developer.spotify.com/documentation/web-api/) to get audio features of tracks
- [Spotipy Python Library](http://spotipy.readthedocs.io/) to simplify API access and functionality
