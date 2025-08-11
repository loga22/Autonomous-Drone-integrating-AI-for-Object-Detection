from dronekit import connect, VehicleMode
import time
import config

# Establishes and verifies MAVLink connection
def connect_vehicle():
    print(f"Connecting to vehicle on: {config.CONNECTION_STRING}")
    vehicle = connect(config.CONNECTION_STRING, wait_ready=True, timeout=60)
    print("Vehicle connection established.")
    return vehicle

# Ensures vehicle is armable, in GUIDED mode, then arms motors.
def perform_pre_flight_checks(vehicle):
    print("Executing pre-flight checks...")
    while not vehicle.is_armable:
        print("  - Waiting for vehicle to become armable...")
        time.sleep(1)
    
    print(f"Setting mode to {config.TARGET_MODE}...")
    vehicle.mode = VehicleMode(config.TARGET_MODE)
    while vehicle.mode.name != config.TARGET_MODE:
        print(f"  - Waiting for mode change... Current mode: {vehicle.mode.name}")
        time.sleep(1)
        
    print("Arming motors...")
    vehicle.armed = True
    while not vehicle.armed:
        print("  - Waiting for arming confirmation...")
        time.sleep(1)
    print("Pre-flight checks passed. Motors armed.")
    return True

# Issues simple_takeoff command to specified altitude.
def takeoff(vehicle):
    print(f"Commanding takeoff to {config.TAKEOFF_ALTITUDE}m...")
    vehicle.simple_takeoff(config.TAKEOFF_ALTITUDE)

# Sends RC override values for direct flight control.
# Channels: 2=Pitch, 3=Throttle, 4=Yaw
def set_flight_controls(vehicle, pitch, yaw, throttle):
    vehicle.channels.overrides = {'2': int(pitch), '3': int(throttle), '4': int(yaw)}

# Sets all flight controls to neutral PWM to command hover.
def hover(vehicle):
    set_flight_controls(vehicle, config.NEUTRAL_PWM, config.NEUTRAL_PWM, config.NEUTRAL_PWM)

# Commands slow yaw for searching.
def search_turn(vehicle):
    set_flight_controls(vehicle, config.NEUTRAL_PWM, config.SEARCH_YAW_PWM, config.NEUTRAL_PWM)

# Triggers vehicle's internal Return-to-Launch sequence.
def return_to_launch(vehicle):
    print("Setting mode to RTL.")
    vehicle.channels.overrides = {} # Critically, clear overrides to allow RTL to take control.
    vehicle.mode = VehicleMode("RTL")

# Triggers vehicle's internal Land sequence.
def land(vehicle):
    print("Setting mode to LAND.")
    vehicle.channels.overrides = {}
    vehicle.mode = VehicleMode("LAND")

# Final cleanup to ensure drone is in safe state.
def cleanup(vehicle):
    print("Executing cleanup procedure...")
    if vehicle.armed:
        vehicle.channels.overrides = {}
        vehicle.armed = False
        print("RC overrides cleared and vehicle disarmed.")
    vehicle.close()
    print("Vehicle connection closed.")