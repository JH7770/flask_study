from . import router_user
from . import router_tweet
from . import router_index

blueprints = [
    router_user.bp,
    router_tweet.bp,
    router_index.bp
]