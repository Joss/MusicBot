from requests import get


def get_json(request_url):
    json_data = None
    document = get(request_url)
    if document.status_code == 200:
        json_data = document.json()

    return json_data


def create_playlist(input_data):
    if 'playlist' not in input_data:
        return None
    else:
        input_data = input_data['playlist']['tracks']

    tracks = list()
    for track in input_data:
        singers = list()
        for artist in track['artists']:
            singers.append(artist['name'])

        title = track['title']

        version = None
        if 'version' in dict.keys(track):
            version = track['version']

        item = {'singers': singers, 'title': title, 'version': version}
        tracks.append(item)
    return tracks


def playlist_to_text(tracks):
    text_list = ""
    for line in tracks:
        track_string = ""
        for artist in line['singers']:
            track_string += f"{artist} "

        track_string += f"- {line['title']}"
        if line['version'] is not None:
            track_string += f" ({line['version']})"

        text_list += track_string + "\n"

    return text_list


def get_yandex_music_playlist(owner, kinds):
    url = "https://music.yandex.ru/handlers/playlist.jsx"
    request_url = f"{url}?owner={owner}&kinds={kinds}&light=false"
    data = get_json(request_url)

    play_list_text = None
    tracks_count = 0

    if data is not None:
        tracks = create_playlist(data)
        if tracks is not None:
            play_list_text = playlist_to_text(tracks)
            tracks_count = len(tracks)

    return play_list_text, tracks_count


