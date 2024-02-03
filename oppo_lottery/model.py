class Person:
    def __init__(self, id, name, seat1, seat2, auth, check):
        self.id = id
        self.name = name
        self.seat1 = seat1
        self.seat2 = seat2
        self.auth = auth
        self.check = check
        self.lottery = 0
        self.desc = ""
        self.reward = ""

    def jsonformat(self):
        return {
            'id': self.id,
            'name': self.name,
            'seat1': self.seat1,
            'seat2': self.seat2,
            'auth': self.auth,
            'check': self.check,
            'lottery': self.lottery,
            'desc': self.desc,
            'reward': self.reward,
        }
