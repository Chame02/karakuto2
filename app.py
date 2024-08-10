from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.playlist_all'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# プレイリストのデータベース
class AllPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(128), nullable=False)
    song = db.Column(db.String(128), nullable=False)
    playlist = db.Column(db.String(128), nullable=False)

# ユーザーのデータベース
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

# ホームページ
@app.route('/')
def index():
    playlists_name = db.session.query(AllPlaylist.playlist).group_by(AllPlaylist.playlist).all()
    playlists_name = [p[0] for p in playlists_name]
    return render_template('index.html', playlists_name=playlists_name)

# プレイリスト名が/playlist/の後に指定される
@app.route('/playlist/<name>')
def show_playlist(name):
    playlist_data = db.session.query(AllPlaylist).filter_by(playlist=name)
    return render_template('playlist.html', playlist=playlist_data, name=name)

# 編集ページ
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # POST
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        artist_names = request.form.getlist('artist')
        song_titles = request.form.getlist('song')

        # データベースへの追加
        for artist, song in zip(artist_names, song_titles):
            new_entry = AllPlaylist(artist=artist, song=song, playlist=playlist_name)
            db.session.add(new_entry)

        db.session.commit()

        return redirect(url_for('confirmation',title=playlist_name, artists=artist_names, songs=song_titles))
    # GET
    else:
        return render_template('edit.html')

# 編集ページでPOSTした後のリダイレクト先（完了画面を表示する）
@app.route('/confirmation')
def confirmation():
    title = request.args.get('title')
    print(title)
    artists = request.args.getlist('artists')
    songs = request.args.getlist('songs')
    playlists = [[artists[i], songs[i]] for i in range(len(artists))]
    return render_template('confirmation.html',title=title, playlists=playlists)

@app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run()