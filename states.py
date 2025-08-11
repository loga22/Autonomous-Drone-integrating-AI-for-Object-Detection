# Defines states for main control loop.
# Prevents chaotic behavior by ensuring drone does only one thing at a time.
class State:
    STARTUP = "STARTUP"
    TAKING_OFF = "TAKING_OFF"
    SEARCHING = "SEARCHING"
    CONFIRMING_TARGET = "CONFIRMING_TARGET"
    TRACKING = "TRACKING"
    GRACE_PERIOD = "GRACE_PERIOD"
    PAUSED = "PAUSED"
    RETURNING_HOME = "RETURNING_HOME"
    LANDING = "LANDING"