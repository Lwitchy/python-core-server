#import stuff
from ByteStream.ByteStream import Reader
from Packets.Messages.Auth.LoginOkMessage import LoginOkMessage

class LoginMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client


    def decode(self):
        self.player.high_id = self.read_int()
        self.player.low_id = self.read_int()
        self.player.token = self.read_string()

        self.major = self.read_int()
        self.minor = self.read_int()
        self.build = self.read_int()

        self.fingerprint_sha = self.read_string()
        self.read_int()

  

    def process(self):
        LoginOkMessage(self.client, self.player).send()
