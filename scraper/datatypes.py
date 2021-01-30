class DataType:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)
    def __str__(self):
        return self.__class__.__name__

class FacebookPost(DataType):
    pass

class FacebookGroup(DataType):
    pass

class FacebookProfile(DataType):
    pass
