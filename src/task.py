class Task:
    def __init__(self, name):
        self.name = name

    def execute(self, data=None):
        raise NotImplementedError("")
