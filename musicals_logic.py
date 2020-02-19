from database import data_handler


def get_column_to_sort_by(value):
    if value == 'title':
        musicals = data_handler.sort_all_musicals_by_title()
    elif value == 'year':
        musicals = data_handler.sort_all_musicals_by_year()
    elif value == 'book':
        musicals = data_handler.sort_all_musicals_by_book()
    elif value == 'music':
        musicals = data_handler.sort_all_musicals_by_music()
    elif value == 'genre':
        musicals = data_handler.sort_all_musicals_by_genre()

    return musicals
