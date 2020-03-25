import re

class Sniffer:

    crack_re = None
    karma_re = None

    def __init__(self):
        self.crack_re = re.compile(r".*crack.*")
        self.karma_re = re.compile(r"(^<@![0-9]*>\+\+$)|(^<@![0-9]*>\-\-$)|(^<@[0-9]*>\+\+$)|(^<@[0-9]*>\-\-$)")

    async def sniff(self, ctx):
        msg = ctx.message.content.lower()

        if self.crack_re.match(msg):
            return "crack", "https://www.youtube.com/watch?v=Dp7iveA5CRs"        
        elif self.karma_re.match(msg):
            return "karma", None

        return False, None
