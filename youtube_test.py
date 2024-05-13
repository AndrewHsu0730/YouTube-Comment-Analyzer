from analyzer import *

def test_urlToVid():
    assert urlToVid("https://www.youtube.com/watch?v=video_id_1") == "video_id_1"
    assert urlToVid("https://www.youtube.com/watch?v=video_id_2&feature=related") == "video_id_2"
    assert urlToVid("https://www.youtube.com/watch?v=video_id_3&list=playlist_id") == "video_id_3"

def test_processComment():
    assert processComment("This is a test comment!") == "this is a test comment"
    assert processComment("Hello123 World!") == "hello world"
    
