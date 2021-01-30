class ScraperException (Exception):
    pass

class InvalidFacebookUrl (ScraperException):
    pass
    
class ExceptionLoadingDriver (ScraperException):
    pass
