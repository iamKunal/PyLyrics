# PyLyrics

Downloads and plays lyrics of the currently playing song, synced with elapsed time.

Uses the currently playing song by quering `mpd` or `cmus`, download the lyrics and syncs with the currently playing song.


## Requirements:

1. For `mpd` : `playerctl`
2. For `cmus` : `cmus-remote` (pre-installed with `cmus`).


## Usage

Copy pylyrics.py to a directory, run by either `python2 pylyrics.py` or mark executable and run `./pylyrics.py` or by `pylyrics.py` after adding to path (for `mpd`).

`cmus` users, add `cmus` as an argument, i.e., run `pylyrics.py cmus`.

Works on most English songs. Tried and tested with `mpsyt` and `cmus`. If lyrics are out of sync (lagging or running, try a different youtube song verson/mp3.)
