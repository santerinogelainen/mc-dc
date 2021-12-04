# MC-DC
MC-DC Discord music bot

Starting the bot:

```
python ./main.py
```

# Command reference

## !play [url, playlist url, or a search term]

- Starts playing a song if no song is playing or adds a song to the queue
- In the case of a playlist, it will add all the songs from the playlist to the queue
- In the case of a search term, it will search for a song and add the first result to the queue

## !skip

- Skips the currently playing song

## !song

- Displays the currently playing or last played song if no song is playing in chat

## !repeat

- Adds the currently playing or last played song if no song is playing to the queue

## !queue

- Displays what's in the queue in chat

## !clear-queue

- Clears the queue

## !pause

- Pauses the music

## !shuffle

- Shuffles the current queue

## !stop

- Stops music from playing and clears the queue

## !leave

- Forces the bot to leave the voice channel

## !join

- Forces the bot to join the current channel the user is in

## !volume [newVolume]

- Sets the volume of the music, for example 100 = 100%, 1 = 1%