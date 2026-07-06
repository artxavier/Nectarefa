'''
MOVETOSTART, DOSQUARE
'''

import rclpy

import yasmin
from yasmin import State
from yasmin import Blackboard
from yasmin_ros.basic_outcomes import SUCCEED, ABORT
from yasmin_ros.yasmin_node import YasminNode

from nectarefa import constants

from nectar.control import(
    DroneFactory,
    MavrosConfig,
    MavrosDrone,
    PoseSource,
    MoveReference,
    RTLMethod,
)

class GoToFst(State):
    
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])
    
    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT

        drone = blackboard["drone"]
        
        
        reached = drone.move_to(
            x=constants.INITPOSX,
            y=constants.INITPOSY,
        )

        drone.delay(1.5)
        
        if reached:
            yasmin.YASMIN_LOG_INFO("Reached starting position for square.")
            return SUCCEED
        else:
            yasmin.YASMIN_LOG_ERROR("Failed to reach starting position for square.")
            return ABORT
        
class DoSquare(State):
    
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])
    
    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT

        drone = blackboard["drone"]
        
        # Define the square's corners based on INITPOSX, INITPOSY, and LINESIZE
        corners = [
            (constants.LINESIZE, 0),
            (0, constants.LINESIZE),
            (-constants.LINESIZE, 0),
            (0, -constants.LINESIZE),
        ]
        
        for corner in corners:
            x, y = corner
            yasmin.YASMIN_LOG_INFO(f"Moving to corner {x}, {y}.")
            reached = drone.move_to(
                x=x,
                y=y,
                z=0,
                precision=0.1,
            )

            drone.delay(1.5)
            
            if not reached:
                yasmin.YASMIN_LOG_ERROR(f"Failed to reach corner at ({x}, {y}).")
                return ABORT
        
        yasmin.YASMIN_LOG_INFO("Completed square path.")
        return SUCCEED
