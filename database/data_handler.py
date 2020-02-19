from database import database_connection as db_connection

GENRES = ['book musical', 'film musical', 'pop/rock musical', 'concept musical', 'sketch musical',
          'tribute/jukebox musical', 'pop opera']
TAGS1 = ['female', 'male', 'male & female']
TAGS2 = ['solo', 'duet', 'group', 'trio', 'quartet', 'choir']
TAGS3 = ['ballad', 'uptempo', 'pop', 'rap', 'legit', 'gospel', 'statement song', 'stand-alone song', 'cabaret']
TAGS4 = ['powerful', 'emotional', 'sad', 'joyous', 'comedy', 'lullaby', 'love song', 'controversial']
TAGS5 = ['popular', 'off-broadway', 'uncommon', 'modern', 'classic', 'audition FAUX PAS']
TAGS6 = ['soprano', 'mezzo', 'alto', 'belter', 'countertenor', 'tenor', 'baritone', 'bass']
TAGS7 = ['asian', 'white skin', 'dark skin', 'child', 'teen', '20s', '30s', 'mature']


@db_connection.connection_handler
def list_all_musicals(cursor):
    cursor.execute("""
                    SELECT * FROM musicals
                    ORDER BY id
                """),
    musicals = cursor.fetchall()
    return musicals


@db_connection.connection_handler
def sort_all_musicals_by_title(cursor):
    cursor.execute("""
                   SELECT * FROM musicals
                    ORDER BY title ASC
                    """,
                   )

    musicals = cursor.fetchall()
    return musicals

@db_connection.connection_handler
def sort_all_musicals_by_year(cursor):
    cursor.execute("""
                   SELECT * FROM musicals
                    ORDER BY year ASC
                    """,
                   )

    musicals = cursor.fetchall()
    return musicals

@db_connection.connection_handler
def sort_all_musicals_by_book(cursor):
    cursor.execute("""
                   SELECT * FROM musicals
                    ORDER BY book ASC
                    """,
                   )

    musicals = cursor.fetchall()
    return musicals

@db_connection.connection_handler
def sort_all_musicals_by_music(cursor):
    cursor.execute("""
                   SELECT * FROM musicals
                    ORDER BY music ASC
                    """,
                   )

    musicals = cursor.fetchall()
    return musicals

@db_connection.connection_handler
def sort_all_musicals_by_genre(cursor):
    cursor.execute("""
                   SELECT * FROM musicals
                    ORDER BY genre ASC
                    """,
                   )

    musicals = cursor.fetchall()
    return musicals


@db_connection.connection_handler
def add_new_musical(cursor, musical):
    cursor.execute("""
          INSERT INTO musicals (title, year, book, music, genre, creator_id)
                VALUES ( %(title)s, %(year)s, %(book)s, %(music)s, %(genre)s, %(user_id)s)  
                    """,
                   {'title': musical['title'],
                    'year': musical['year'],
                    'book': musical['book'],
                    'music': musical['music'],
                    'genre': musical['genre'],
                    'user_id': musical['user_id']})


@db_connection.connection_handler
def show_all_songs_from_musical(cursor, musical):
    cursor.execute("""
                    SELECT id, title,length,performer, show FROM songs
                    WHERE songs.show = %(musical)s
                    ORDER BY id
                    """,
                   {'musical': musical})
    songs = cursor.fetchall()
    return songs


@db_connection.connection_handler
def sort_all_songs_from_musical_by_title(cursor, musical):
    cursor.execute("""
                    SELECT id, title,length,performer, show FROM songs
                    WHERE songs.show = %(musical)s
                    ORDER BY title ASC
                    """,
                   {'musical': musical})
    songs = cursor.fetchall()
    return songs

@db_connection.connection_handler
def sort_all_songs_from_musical_by_length(cursor, musical):
    cursor.execute("""
                    SELECT id, title,length,performer, show FROM songs
                    WHERE songs.show = %(musical)s
                    ORDER BY length ASC
                    """,
                   {'musical': musical})
    songs = cursor.fetchall()
    return songs

@db_connection.connection_handler
def sort_all_songs_from_musical_by_performer(cursor, musical):
    cursor.execute("""
                    SELECT id, title,length,performer, show FROM songs
                    WHERE songs.show = %(musical)s
                    ORDER BY performer ASC
                    """,
                   {'musical': musical})
    songs = cursor.fetchall()
    return songs


@db_connection.connection_handler
def add_new_song(cursor, song):
    cursor.execute("""
                    INSERT INTO songs (title, length, performer, show, lyrics, video, creator_id)
                     VALUES (%(title)s, %(length)s, %(performer)s, %(show)s, %(lyric)s, %(video)s, %(user_id)s)
                     """,
                   {'show': song['show'],
                    'title': song['title'],
                    'length': song['length'],
                    'performer': song['performer'],
                    'lyrics': song['lyrics'],
                    'video': song['video'],
                    'user_id': song['user_id']}
                   )


@db_connection.connection_handler
def delete_song(cursor, song_id):
    cursor.execute("""
                  DELETE FROM songs 
                  WHERE songs.id = %(song_id)s
                  RETURNING * 
                    """,

                   {'song_id': song_id})


@db_connection.connection_handler
def get_song_by_id(cursor, song_id):
    cursor.execute("""
                    SELECT id, title, length, performer, show, lyrics, sheet_music, video
                    FROM songs
                    WHERE id = %(song_id)s 
                    """,
                   {'song_id': song_id})

    song = cursor.fetchone()
    return song


@db_connection.connection_handler
def edit_song(cursor, song):
    cursor.execute("""
                   UPDATE songs SET (title, length, performer, lyrics, video)
                   = (%(title)s, %(length)s, %(performer)s, %(lyrics)s, %(video)s)
                   WHERE id = %(id)s  
                    """,
                   {'id': song['id'],
                    'title': song['title'],
                    'length': song['length'],
                    'performer': song['performer'],
                    'lyrics': song['lyrics'],
                    'video': song['video']})


@db_connection.connection_handler
def register_new_user(cursor, user):
    cursor.execute("""
                    INSERT INTO users (creation_date, username, password)
                    VALUES (NOW()::date, %(username)s, %(password)s)
                    """,
                   {'username': user['username'],
                    'password': user['password']})


@db_connection.connection_handler
def select_user_by_username(cursor, username):
    cursor.execute("""
                    SELECT id, creation_date, username, password
                    FROM users
                    WHERE username = %(username)s     
                    """,
                   {'username': username})

    user = cursor.fetchone()
    return user


@db_connection.connection_handler
def search_songs_by_expression(cursor, search):
    cursor.execute("""
                    SELECT DISTINCT songs.id, songs.title, show, performer, book, music FROM songs
                    LEFT JOIN musicals m on songs.show = m.title
                    LEFT JOIN tags t on songs.id = t.song_id
                    WHERE songs.title LIKE '%%'|| %(search)s || '%%'
                    OR show LIKE '%%'|| %(search)s || '%%'
                    OR performer LIKE '%%'|| %(search)s || '%%'
                    OR book LIKE '%%'|| %(search)s || '%%'
                    OR music LIKE '%%'|| %(search)s || '%%'
                    OR tag LIKE '%%'|| %(search)s || '%%'
                    ORDER BY title 
                    
                    """,
                   {'search': search})

    songs = cursor.fetchall()
    return songs


# lajki są nieefektywne

# wyszukiwanie pełnotekstowe z wagami sql


@db_connection.connection_handler
def get_tags_for_song(cursor, song_id):
    cursor.execute("""
                 SELECT tag FROM tags
                 INNER JOIN songs s on tags.song_id = s.id
                 WHERE song_id = %(song_id)s
    
                    """,
                   {'song_id': song_id})
    tags = cursor.fetchall()
    return tags


@db_connection.connection_handler
def tag_song(cursor, tag):
    cursor.execute("""
                    INSERT INTO tags (creation_date, creator_id, tag, song_id)
                    VALUES (NOW()::date, %(user_id)s, %(tag)s, %(song_id)s)
    
                    """,
                   {'user_id': tag['user_id'],
                    'tag': tag['tag_val'],
                    'song_id': tag['song_id']})
