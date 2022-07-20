FACEBOOK = 'facebook'
TWITTER = 'twitter'
INSTAGRAM = 'instagram'
YOUTUBE = 'youtube'
REDDIT = 'reddit'
WHATSAPP = 'whatsapp'
LINKEDIN = 'linkedin'
PINTEREST = 'pinterest'
TUMBLR = 'tumblr'

SOCIAL_MEDIAS = [
    (FACEBOOK, 'Facebook'), 
    (TWITTER, 'Twitter'), 
    (REDDIT, 'Reddit'), 
    (WHATSAPP, 'Whatsapp'), 
    (LINKEDIN, 'Linkedin'), 
    (PINTEREST, 'Pinterest'), 
    (TUMBLR, 'Tumblr'),
    (YOUTUBE, 'Youtube'),
    (INSTAGRAM, 'Instagram')
]

MODEL_QUESTION = 1
MODEL_NEWS = 2
MODEL_TERM = 3
MODEL_BLOG = 4
MODEL_COMPANY = 5

FOR_MODEL = (
    (MODEL_QUESTION, 'Question'),
    (MODEL_NEWS, 'News'),
    (MODEL_TERM, 'Term'),
    (MODEL_BLOG, 'Blog'),
    (MODEL_COMPANY, 'Company')
)

POST_TYPE_VIDEO = 1
POST_TYPE_IMAGE = 2
POST_TYPE_TEXT = 3
POST_TYPE_REPOST = 4
POST_TYPE_TEXT_VIDEO = 5
POST_TYPE_TEXT_IMAGE = 6
POST_TYPE_SHORTS = 7
POST_TYPE_THREAD = 8

POST_TYPE = (
    (POST_TYPE_VIDEO, 'Video'), 
    (POST_TYPE_IMAGE, 'Image'), 
    (POST_TYPE_TEXT, 'Text'),
    (POST_TYPE_REPOST, 'Repost'), 
    (POST_TYPE_TEXT_VIDEO, 'Text and video'), 
    (POST_TYPE_TEXT_IMAGE, 'Text and image'), 
    (POST_TYPE_SHORTS, 'Shorts'),
    (POST_TYPE_THREAD, 'Thread'))

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'

FACEBOOK_GRAPH_VIDEO_URL = "https://graph-video.facebook.com/"

INSTAGRAM_GRAPH_URL = 'https://graph.instagram.com/'
