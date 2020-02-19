from flask import Flask, render_template, redirect, request, url_for, session, flash

from database import data_handler
import password_handler
import user_verification
import data_format_utils as utils
import musicals_logic
import songs_logic

app = Flask(__name__)
app.secret_key = "secretkey"


@app.route('/')
def list_all_musicals():
    musicals = data_handler.list_all_musicals()
    return render_template('list_all_musicals.html',
                           musicals=musicals,
                           page_title='Musical Theatre library')


@app.route('/sort_all', methods=['POST'])
def sort_all_musicals():
    value = request.form.get('condition')
    musicals = musicals_logic.get_column_to_sort_by(value)

    return render_template('list_all_musicals.html',
                           musicals=musicals,
                           page_title='Musical Theatre library')


@app.route('/add_new_musical', methods=['POST'])
def add_new_musical():
    title = request.form.get('title')
    year = request.form.get('year')
    book = request.form.get('book')
    music = request.form.get('music')
    genre = request.form.get('genre')
    username = session['username']
    user = data_handler.select_user_by_username(username)
    user_id = user['id']
    musical = {
        'title': title,
        'year': year,
        'book': book,
        'music': music,
        'genre': genre,
        'user_id': user_id
    }

    data_handler.add_new_musical(musical)
    return redirect('/',
                    session['username'])


@app.route('/add_new_musical', methods=['GET'])
def show_add_musical_form():
    genres = data_handler.GENRES
    return render_template('add_new_musical.html',
                           form_url=url_for('add_new_musical'),
                           page_title='Add new musical to database',
                           genres=genres)


@app.route('/songs_from_musical/<musical_title>', methods=['GET'])
def show_songs_from_musical(musical_title):
    songs = data_handler.show_all_songs_from_musical(musical_title)
    return render_template('list_songs_musical.html',
                           songs=songs,
                           page_title='List of songs',
                           musical_title=musical_title)


@app.route("/sort_songs/<musical_title>", methods=['GET', 'POST'])
def sort_songs_from_musical(musical_title):
    value = request.form.get('value')
    songs = songs_logic.get_column_to_sort_by(value, musical_title)
    return render_template('list_songs_musical.html',
                           songs=songs,
                           page_title='List of songs',
                           musical_title=musical_title, )


# weryfikacja typu danych w urlu <>
# wyjątki - stworzyć klasę

@app.route('/songs_from_musical/add_song/<musical_title>', methods=['POST'])
def add_new_song(musical_title):
    title = request.form.get('title')
    length = request.form.get('length')
    performer = request.form.get('performer')
    lyrics = request.form.get('lyrics')
    video = request.form.get('lyrics')
    username = session['username']
    user = data_handler.select_user_by_username(username)
    user_id = user['id']
    song = {
        'show': musical_title,
        'title': title,
        'length': length,
        'performer': performer,
        'lyrics': lyrics,
        'video': video,
        'user_id': user_id
    }
    data_handler.add_new_song(song)
    return redirect('/songs_from_musical/{}'.format(musical_title))


@app.route('/songs_from_musical/add_song/<musical_title>', methods=['GET'])
def show_add_new_song_form(musical_title):
    return render_template('add_new_song.html',
                           form_url=url_for('add_new_song',
                                            musical_title=musical_title,
                                            page_title='Add new song to musical'))


@app.route('/songs_from_musical/delete/<song_id>', methods=['GET'])
def delete_song_given_id(song_id):
    song = data_handler.get_song_by_id(song_id)
    musical_title = song['show']
    data_handler.delete_song(song_id)
    return redirect('/songs_from_musical/{}'.format(musical_title))


@app.route('/songs_from_musical/edit/<song_id>', methods=['GET', 'POST'])
def edit_song_given_id(song_id):
    song = data_handler.get_song_by_id(song_id)
    musical_title = song['show']
    if request.method == 'POST':
        title = request.form.get('title')
        length = request.form.get('length')
        performer = request.form.get('performer')
        lyrics = request.form.get('lyrics')
        video = request.form.get('video')
        updated_song = {
            'id': song_id,
            'show': musical_title,
            'title': title,
            'length': length,
            'performer': performer,
            'lyrics': lyrics,
            'video': video
        }
        data_handler.edit_song(updated_song)
        return redirect('/songs_from_musical/{}'.format(musical_title))

    elif request.method == 'GET':
        title = song['title']
        length = song['length']
        performer = song['performer']
        lyrics = song['lyrics']
        video = song['video']
        return render_template('add_new_song.html',
                               title=title,
                               length=length,
                               performer=performer,
                               lyrics=lyrics,
                               video=video,
                               page_title='Edit song')


@app.route('/show_song_details/<song_id>', methods=['GET'])
def show_song_details(song_id):
    song = data_handler.get_song_by_id(song_id)
    tags_listofdict = data_handler.get_tags_for_song(song_id)
    tags = [x['tag'] for x in tags_listofdict]

    return render_template('song_details.html',
                           song=song,
                           tags=tags,
                           page_title='Song details')


@app.route('/tag_song/<song_id>', methods=['GET', 'POST'])
def tag_song(song_id):
    if request.method == 'POST':
        tag_val = request.form.get('tag')
        username = session['username']
        user = data_handler.select_user_by_username(username)
        user_id = user['id']
        tag = {'tag_val': tag_val,
               'user_id': user_id,
               'song_id': song_id}
        data_handler.tag_song(tag)
        return redirect('/show_song_details/{}'.format(song_id))

    elif request.method == 'GET':
        tags1 = data_handler.TAGS1
        tags2 = data_handler.TAGS2
        tags3 = data_handler.TAGS3
        tags4 = data_handler.TAGS4
        tags5 = data_handler.TAGS5
        tags6 = data_handler.TAGS6
        tags7 = data_handler.TAGS7
    return render_template('add_tag.html',
                           tags1=tags1,
                           tags3=tags3,
                           tags2=tags2,
                           tags4=tags4,
                           tags5=tags5,
                           tags6=tags6,
                           tags7=tags7,
                           form_url=url_for('tag_song', song_id=song_id),
                           page_title='Tag song')


@app.route('/search', methods=['POST'])
def search_songs_by_expression():
    search = request.form.get('search')
    songs = data_handler.search_songs_by_expression(search)
    return render_template('list_search_songs.html',
                           songs=songs,
                           page_title='Search results')


@app.route('/register', methods=['POST'])
def register_new_user():
    username = request.form.get('username')
    plain_password = request.form.get('password')

    if utils.validate_data(username) and utils.validate_data(plain_password):
        if user_verification.check_user_in_database(username):
            flash('User already in database. Please pick another username.')
            return render_template('form_registration.html',
                                   form_url=url_for('register_new_user'),
                                   page_title='Registration',
                                   password=plain_password)
        else:
            hashed_password = password_handler.hash_password(plain_password)

            user = {
                'username': username,
                'password': hashed_password
            }
            data_handler.register_new_user(user)
            session['username'] = user['username']
            return redirect('/')
    elif utils.validate_data(username) and not utils.validate_data(plain_password):
        flash("Password can't be empty")
        return render_template('form_registration.html',
                               form_url=url_for('register_new_user'),
                               page_title='Registration',
                               username=username)

    elif utils.validate_data(plain_password) and not utils.validate_data(username):
        flash("Username can't be empty")
        return render_template('form_registration.html',
                               form_url=url_for('register_new_user'),
                               page_title='Registration',
                               password=plain_password)
    else:
        flash("Please fill in all the blank spaces")
        return redirect('/register')


@app.route('/register', methods=['GET'])
def show_registration_form():
    return render_template('form_registration.html',
                           form_url=url_for('register_new_user'),
                           page_title='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    login_user = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }
    if utils.validate_data(login_user['username']):

        if user_verification.check_user_in_database(login_user['username']):
            let_pass = user_verification.verify_user(login_user)
            if let_pass:
                session['username'] = login_user['username']
                return redirect('/')
            else:
                musicals = data_handler.list_all_musicals()
                username = login_user['username']
                flash('Wrong password. Please try again.')
                return render_template('list_all_musicals.html',
                                       musicals=musicals,
                                       page_title='Musical Theatre library',
                                       username=username)

        else:
            flash("User doesn't exist! Please register.")
            return redirect('/register')

    else:
        flash("Username can't be empty")
        return redirect('/')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )
