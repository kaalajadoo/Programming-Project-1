import json
import random

# Function to load data from JSON files
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save data to JSON files
def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# 1. Display songs in alphabetical order
def display_songs():
    songs = load_data('songs.json')
    songs_sorted = sorted(songs, key=lambda x: x['name'])
    for song in songs_sorted:
        print(f"name: {song['name']}, Artist: {song['artist']}, Length: {song['length']} minutes")

# 2. Create a user account
def create_account():
    users = load_data('users.json')
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    fav_artist = input("Enter your favorite artist: ")
    fav_genre = input("Enter your favorite genre: ")

    user = {
        "name": name,
        "dob": dob,
        "favorite_artist": fav_artist,
        "favorite_genre": fav_genre,
        "playlists": []
    }
    users.append(user)
    save_data('users.json', users)
    print(f"Account created for {name}!")

# 3. Edit favorite artist and favorite genre
def edit_user():
    users = load_data('users.json')
    name = input("Enter your name: ")

    for user in users:
        if user['name'] == name:
            print(f"Current favorite artist: {user['favorite_artist']}")
            new_artist = input("Enter new favorite artist: ")
            print(f"Current favorite genre: {user['favorite_genre']}")
            new_genre = input("Enter new favorite genre: ")

            user['favorite_artist'] = new_artist
            user['favorite_genre'] = new_genre
            save_data('users.json', users)
            print(f"Profile updated for {name}!")
            return

    print(f"No user found with name {name}.")

# 4. Create, save, and view playlists
def create_playlist():
    users = load_data('users.json')
    songs = load_data('songs.json')

    name = input("Enter your name: ")
    for user in users:
        if user['name'] == name:
            playlist_name = input("Enter the name of the playlist: ")
            playlist = []

            while True:
                display_songs()
                song_name = input("Enter the name of the song to add (or 'done' to finish): ").strip()

                if song_name.lower() == 'done':
                    break

                song = next((s for s in songs if s['name'].lower() == song_name.lower()), None)
                if song:
                    playlist.append(song)
                else:
                    print("Song not found. Please try again.")

            if playlist:
                user['playlists'].append({
                    "name": playlist_name,
                    "songs": playlist
                })
                save_data('users.json', users)
                print(f"Playlist '{playlist_name}' created and saved!")
            else:
                print("No songs in playlist, operation canceled.")
            return

    print(f"No user found with name {name}.")

def view_playlists():
    users = load_data('users.json')
    name = input("Enter your name: ")

    for user in users:
        if user['name'] == name:
            if user['playlists']:
                print(f"{name}'s Playlists:")
                for playlist in user['playlists']:
                    print(f"\nPlaylist: {playlist['name']}")
                    for song in playlist['songs']:
                        print(f" - {song['name']} by {song['artist']} ({song['length']} minutes)")
            else:
                print("No playlists found.")
            return

    print(f"No user found with name {name}.")

def generate_playlist_by_time():
  time_limit = int(input("Enter the time limit in seconds: "))  # Get time limit as integer
  songs = load_data('songs.json')
  playlist = []
  total_time = 0

  for song in songs:
      song_length = int(song['length'])  # Convert song length to integer
      if total_time + song_length <= time_limit:
          playlist.append(song)
          total_time += song_length

  if playlist:
      print("\nGenerated Playlist:")
      for song in playlist:
          print(f"Title: {song['name']}, Artist: {song['artist']}, Length: {song['length']} seconds")
  else:
      print("No songs fit the criteria for the given time limit.")



# 5b. Generate a playlist by genre
def generate_playlist_by_genre():
    songs = load_data('songs.json')
    genre = input("Enter the genre: ").capitalize()

    genre_songs = [song for song in songs if song['genre'].capitalize() == genre]
    if genre_songs:
        playlist = random.sample(genre_songs, min(5, len(genre_songs)))
        print(f"Generated Playlist for {genre} genre:")
        for song in playlist:
            print(f"{song['name']} by {song['artist']} ({song['length']} minutes)")
    else:
        print("No songs found for that genre.")

# 6. Save songs by an artist to a text file
def save_songs_by_artist():
    songs = load_data('songs.json')
    artist = input("Enter the artist's name: ").capitalize()

    artist_songs = [song for song in songs if song['artist'].capitalize() == artist]

    if artist_songs:
        with open(f"{artist}_songs.txt", "w") as file:
            for song in artist_songs:
                file.write(f"{song['name']} ({song['length']} minutes)\n")
                
        print(f"Songs by {artist} saved to {artist}_songs.txt")
    else:
        print("No songs found for that artist.")

#7
def display_genres_average_length():
    songs = load_data('songs.json')
    genres = {}

    for song in songs:
        genre = song['genre']
        song_length = int(song['length'])  # Convert song length to integer
        if genre in genres:
            genres[genre].append(song_length)
        else:
            genres[genre] = [song_length]

    print("\nAverage Length of Songs by Genre:")
    for genre, lengths in genres.items():
        avg_length = sum(lengths) / len(lengths)  # Calculate average
        print(f"Genre: {genre}, Average Length: {avg_length:.2f} seconds")


# Main menu
def main():
    while True:
        print("\n--- OCRtunes Menu ---")
        print("1. Display songs")
        print("2. Create account")
        print("3. Edit favorite artist/genre")
        print("4. Create playlist")
        print("5. View playlists")
        print("6. Generate playlist by time limit")
        print("7. Generate playlist by genre")
        print("8. Save songs by artist to file")
        print("9. Display genres and average track length")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_songs()
        elif choice == '2':
            create_account()
        elif choice == '3':
            edit_user()
        elif choice == '4':
            create_playlist()
        elif choice == '5':
            view_playlists()
        elif choice == '6':
            generate_playlist_by_time()
        elif choice == '7':
            generate_playlist_by_genre()
        elif choice == '8':
            save_songs_by_artist()
        elif choice == '9':
            display_genres_average_length()
        elif choice == '10':
            print("Exiting OCRtunes. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
main()
