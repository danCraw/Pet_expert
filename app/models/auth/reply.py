from app.models.auth.base import Token
from app.models.reply import ReplyIn


class CreateReply(Token):
    reply: ReplyIn
    