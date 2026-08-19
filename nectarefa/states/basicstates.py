'''
INSTANCIAR OS ESTADOS BASICOS: INIT, TAKEOFF, LAND, END
'''
import rclpy

import yasmin
from yasmin import State
from yasmin import Blackboard
from yasmin_ros.basic_outcomes import SUCCEED, ABORT
from yasmin_ros.yasmin_node import YasminNode

from nectarefa.constants import (
    RTL_ALTITUDE,
    TAKEOFFHEIGHT,
    SIM_MODE,
)

from nectar.control import(
    DroneFactory,
    MavrosConfig,
    MavrosDrone,
    MavlinkDrone,
    PoseSource,
    MoveReference,
    RTLMethod,
    SITL_GAZEBO_CONFIG,
)

import time

class Initialize(State):
    
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])
        
    def execute(self, blackboard: Blackboard):
        try:
            node = YasminNode.get_instance()
            yasmin.YASMIN_LOG_INFO("Initializing drone...")

            config = (
                SITL_GAZEBO_CONFIG if SIM_MODE else MavlinkConfig()
            )
            drone = DroneFactory.create("mavlink", config, node._executor)
            blackboard["drone"] = drone
            drone.delay(1)
            
            return SUCCEED
        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Init error {e}")
            return ABORT
            
class Takeoff(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED,ABORT])
        
    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT

        drone: MavrosDrone = blackboard["drone"]

        try:
            yasmin.YASMIN_LOG_INFO(f"Taking off to {TAKEOFFHEIGHT}m...")
            drone.set_home()
            drone.arm()
            drone.takeoff(TAKEOFFHEIGHT)
            drone.delay(3)

            reached = drone.move_to(
                z=TAKEOFFHEIGHT,
                reference=MoveReference.TAKEOFF,
                timeout=30.0,
                precision=0.3,
            )

            if not reached:
                yasmin.YASMIN_LOG_WARN("Takeoff move_to timed out, continuing.")

            drone.delay(1)
            yasmin.YASMIN_LOG_INFO("Takeoff complete.")
            return SUCCEED

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Takeoff failed: {e}")
            return ABORT
        
class ReturnToLaunch(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT

        drone: MavrosDrone = blackboard["drone"]

        try:
            yasmin.YASMIN_LOG_INFO(f"Returning to launch at {RTL_ALTITUDE}m...")
            drone.rtl(
                altitude=RTL_ALTITUDE,
                method=RTLMethod.NAVIGATE,
                land=False,
            )
            drone.delay(2)
            return SUCCEED

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"RTL failed: {e}")
            return ABORT
        
class End(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT

        drone: MavrosDrone = blackboard["drone"]

        try:
            yasmin.YASMIN_LOG_INFO("Landing...")
            drone.land()
            drone.delay(3)
            yasmin.YASMIN_LOG_INFO("Landing complete.")
            return SUCCEED

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Landing failed: {e}")
            return ABORT

