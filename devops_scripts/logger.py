from datetime import datetime

class logger:
    def __init__(self):
        """
        Logging levels 
        Level		:: 	Meaning				::  	Use for
        --------------------------------------------------------------------------------------------
        DEBUG 	= 4  	:: Detailed information 		:: Debugging during development
        INFO 	= 3	:: Normal operation messages		:: Startup, shutdown, normal status
        WARN	= 2	:: Something unexpected but running	:: Potential issues, recoverable errors
        ERROR 	= 1	:: Serious problem, needs action	:: Failed operations, component failure
        CRITICAL= 0	:: System is unusable or unsafe		:: Full shutdown, fatal crashes
        """
        # Define level blocks
        self.levels = {
            0 : "CRITICAL",
            1 : "ERROR",
            2 : "WARN",
            3 : "INFO",
            4 : "DEBUG"
        }
        for level in self.levels:
            setattr(self, self.levels[level], level)
        # Reference
        self.taskid = ""
        self.appname = ""
        self.logginglevel = 4
        self.appnamesource = "id" # Can be "id"

    def log(self, level = 4, message = ""):
        # Data validation
        if not type(self.appname) == str or len(self.appname) == 0:
            self.appname = "invalid"
        if not type(self.taskid) == int:
	        self.taskid = 000
        if not type(level) == int or not level in self.levels:
            level = 4 # Debug if the level is not valid
        if level > self.logginglevel:
            return # Do not continue if log level is below allowed
        if not type(message) == str or len(message) == 0:
            message = "Invalid message len or type"
        # Add here invalid characters or regex for message
        if '\n' in message:
            message = "Invalid characters in message"
        if not self.appnamesource in ["name", "id"]:
            self.appnamesource = "id" # Default ID
        # Get identification data
        formatteddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.appnamesource == "name":
            app = self.appname
        elif self.appnamesource == "id":
            app = self.taskid
        loglevel = self.levels[level]
        # Create log string
        logstring = f"[{formatteddate}] [{app}] [{loglevel}] {message}"
        print(logstring)
