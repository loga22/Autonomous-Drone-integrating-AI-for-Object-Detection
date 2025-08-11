# MAVLink Connection
CONNECTION_STRING = 'COM8'      # SITL: 'tcp:127.0.0.1:5760'
TARGET_MODE = 'GUIDED'          # Required for scripted control via RC overrides

# Mission Parameters
TAKEOFF_ALTITUDE = 5            # meters
MIN_BATTERY_LEVEL = 20          # % level to trigger a safety RTL
SEARCH_TIMEOUT = 60             # Abort search and RTL after x seconds
TARGET_LOST_GRACE_PERIOD = 3    # x seconds to wait before starting search

# Proportional Controller Gains (PID-like)
YAW_KP = 0.005                  # Controls turn rate based on horizontal error
PITCH_KP = 0.008                # Controls fwd/back speed based on bbox size error
THROTTLE_KP = 0.006             # Controls altitude based on vertical error in frame

# RC Channel Values
NEUTRAL_PWM = 1500              # Standard PWM for neutral/hover
SEARCH_YAW_PWM = 1550           # PWM for a slow, controlled yaw during search

# Vision System Configuration
CONFIDENCE_THRESHOLD = 0.50     # Minimum detection confidence from YOLO model
CONFIRMATION_FRAMES = 5         # Require x consecutive frames to confirm a target
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_BBOX_HEIGHT_PX = 150     # Desired size of target for distance control
TARGET_VERTICAL_CENTER = FRAME_HEIGHT / 2 # Ideal vertical position of target in frame