import cv2
import config

# Overlays telemetry and state data onto video frame.
def display_status(frame, state, battery, target_info=None):
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Displays current state from state machine
    cv2.putText(frame, f"STATE: {state}", (10, 30), font, 0.8, (0, 255, 255), 2)
    
    # Display battery, color-coded for safety
    battery_color = (0, 255, 0) if battery > config.MIN_BATTERY_LEVEL else (0, 0, 255)
    cv2.putText(frame, f"BATT: {battery}%", (10, 60), font, 0.8, battery_color, 2)
    
    # Display context-specific info, like tracking errors
    if target_info:
        cv2.putText(frame, target_info, (10, 90), font, 0.6, (255, 255, 255), 1)

    # Display available keyboard commands
    controls_text = "Controls: P(Pause) | S(RTL) | N(New Target) | Q(Quit)"
    cv2.putText(frame, controls_text, (10, config.FRAME_HEIGHT - 20), font, 0.5, (255, 255, 0), 1)
    
    return frame