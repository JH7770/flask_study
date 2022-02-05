from . import router_front
from . import router_user
from . import router_tweet
from . import router_index

blueprints = [
    router_front.bp,
    router_user.bp,
    router_tweet.bp,
    router_index.bp
]