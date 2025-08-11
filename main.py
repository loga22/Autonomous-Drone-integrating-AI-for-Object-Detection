import cv2
import time
import numpy as np

# Import custom modules
import config
from states import State
import utils
import drone_controller
from vision import VisionSystem

def main():
    vehicle = None
    vision_sys = None
    
    # main try/finally block for cleanup.
    try:
        # System Initialization
        vehicle = drone_controller.connect_vehicle()
        vision_sys = VisionSystem()
        
        # Run pre-flight sequence.
        drone_controller.perform_pre_flight_checks(vehicle)
        drone_controller.takeoff(vehicle)
        
        # Initialize state machine and timers.
        current_state = State.TAKING_OFF
        target_lost_timer = 0
        search_start_time = 0
        confirmation_counter = 0

        # Core State Machine Loop
        while True:
            # Input Stage
            ret, frame = vision_sys.get_frame()
            if not ret:
                print("Frame acquisition failed. Triggering LAND.")
                current_state = State.LANDING
            
            target = vision_sys.find_target(frame) if frame is not None else None

            # High-Priority Safety Checks
            battery_level = vehicle.battery.level
            if battery_level < config.MIN_BATTERY_LEVEL and current_state != State.RETURNING_HOME:
                print(f"Safety override: Low battery ({battery_level}%). Triggering RTL.")
                current_state = State.RETURNING_HOME

            # Operator Input Handling
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): # Quit
                current_state = State.LANDING
            elif key == ord('p'): # Pause/Unpause
                current_state = State.PAUSED if current_state != State.PAUSED else State.SEARCHING
            elif key == ord('s'): # Force RTL
                current_state = State.RETURNING_HOME
            elif key == ord('n'): # New Target
                current_state = State.SEARCHING

            # State Logic
            target_info_text = None # Info to display on screen.

            if current_state == State.TAKING_OFF:
                alt = vehicle.location.global_relative_frame.alt
                target_info_text = f"Taking off... Alt: {alt:.1f}m"
                if alt >= config.TAKEOFF_ALTITUDE * 0.95:
                    current_state = State.SEARCHING
                    search_start_time = time.time()

            elif current_state == State.SEARCHING:
                target_info_text = "State: SEARCHING"
                drone_controller.search_turn(vehicle)
                if target is not None:
                    current_state = State.CONFIRMING_TARGET
                    confirmation_counter = 1
                elif time.time() - search_start_time > config.SEARCH_TIMEOUT:
                    current_state = State.RETURNING_HOME

            elif current_state == State.CONFIRMING_TARGET:
                # This state prevents locking onto false positives.
                target_info_text = f"State: CONFIRMING ({confirmation_counter}/{config.CONFIRMATION_FRAMES})"
                drone_controller.hover(vehicle)
                if target is not None:
                    confirmation_counter += 1
                    if confirmation_counter >= config.CONFIRMATION_FRAMES:
                        current_state = State.TRACKING
                else: # Target was lost during confirmation.
                    current_state = State.SEARCHING

            elif current_state == State.TRACKING:
                if target is not None:
                    # Deconstruct target data.
                    x1, y1, x2, y2 = map(int, [target['xmin'], target['ymin'], target['xmax'], target['ymax']])
                    center_x, center_y, height = (x1 + x2) / 2, (y1 + y2) / 2, y2 - y1
                    
                    # Calculate error terms for P-controllers.
                    yaw_error = center_x - (config.FRAME_WIDTH / 2)
                    pitch_error = config.TARGET_BBOX_HEIGHT_PX - height
                    throttle_error = config.TARGET_VERTICAL_CENTER - center_y
                    
                    # Calculate control outputs. Inverted for pitch/throttle due to camera/movement relation.
                    yaw_out = config.NEUTRAL_PWM + (config.YAW_KP * yaw_error)
                    pitch_out = config.NEUTRAL_PWM - (config.PITCH_KP * pitch_error)
                    throttle_out = config.NEUTRAL_PWM - (config.THROTTLE_KP * throttle_error)
                    
                    # Send commands to flight controller.
                    drone_controller.set_flight_controls(vehicle, pitch_out, yaw_out, throttle_out)
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    target_info_text = f"Tracking | H_err:{int(pitch_error)}px | Y_err:{int(yaw_error)}px"
                else:
                    # Target lost, enter grace period to handle brief occlusions.
                    current_state = State.GRACE_PERIOD
                    target_lost_timer = time.time()

            elif current_state == State.GRACE_PERIOD:
                target_info_text = "State: GRACE PERIOD (Target Lost)"
                drone_controller.hover(vehicle)
                if target is not None:
                    current_state = State.TRACKING # Re-acquired target.
                elif time.time() - target_lost_timer > config.TARGET_LOST_GRACE_PERIOD:
                    current_state = State.SEARCHING # Grace period expired.
                    search_start_time = time.time()

            elif current_state == State.PAUSED:
                target_info_text = "State: PAUSED"
                drone_controller.hover(vehicle)
            
            elif current_state == State.RETURNING_HOME:
                target_info_text = "State: RETURNING HOME"
                drone_controller.return_to_launch(vehicle)
                if vehicle.location.global_relative_frame.alt < 1:
                    current_state = State.LANDING
            
            if current_state == State.LANDING:
                drone_controller.land(vehicle)
                break # Exit main while loop.

            # Output Stage
            if frame is not None:
                frame = utils.display_status(frame, current_state, battery_level, target_info_text)
                cv2.imshow("Drone Person Tracking", frame)

    except Exception as e:
        print(f"\nFATAL ERROR: An unhandled exception occurred: {e}\n")
    finally:
        # Cleanup block.
        print("\n--- Initiating cleanup sequence ---")
        if vehicle:
            drone_controller.cleanup(vehicle)
        if vision_sys:
            vision_sys.release()
        cv2.destroyAllWindows()
        print("Cleanup complete. Exiting.")

# Start
if __name__ == "__main__":
    main()