from database import data_handler

def get_column_to_sort_by(value, musical):
    if value == 'title':
        songs = data_handler.sort_all_songs_from_musical_by_title(musical)
    elif value == 'length':
        songs = data_handler.sort_all_songs_from_musical_by_length(musical)
    elif value == 'performer':
        songs = data_handler.sort_all_songs_from_musical_by_performer(musical)

    return songs
