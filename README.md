# 🐝 Nectarefa

A ROS 2 autonomous drone mission package built with [YASMIN](https://github.com/uleroboticsgroup/yasmin) state machines and [Nectar SDK](https://github.com/your-org/nectar-sdk) for drone control.

The drone initializes, takes off, navigates to a starting position, flies a square path, returns to launch, and lands — all orchestrated through a finite state machine.

## State Machine

```
INITIALIZE ──succeed──▶ TAKEOFF ──succeed──▶ GOTOFST ──succeed──▶ DOSQUARE
    │                      │                    │                    │
  abort                  abort                abort                abort
    │                      │                    │                    │
    ▼                      ▼                    ▼                    ▼
   END              RETURN_TO_LAUNCH ◀──────────┴────────────────────┘
                           │
                        succeed
                           │
                           ▼
                          END ──succeed──▶ (done)
```

| State | Description |
|---|---|
| **INITIALIZE** | Creates the drone instance via `DroneFactory` using MAVROS |
| **TAKEOFF** | Arms, sets home, and takes off to the configured altitude |
| **GOTOFST** | Navigates to the initial position (`INITPOSX`, `INITPOSY`) |
| **DOSQUARE** | Flies a square path with side length `LINESIZE` using relative moves |
| **RETURN_TO_LAUNCH** | Returns to the launch position at `RTL_ALTITUDE` |
| **END** | Lands the drone and finishes the mission |

## Dependencies

- [ROS 2](https://docs.ros.org/) (Humble / Jazzy)
- [YASMIN](https://github.com/uleroboticsgroup/yasmin) — state machine framework
- [Nectar SDK](https://github.com/your-org/nectar-sdk) — drone control abstraction over MAVROS

## Installation

Clone into your ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/your-user/nectarefa.git
git clone https://github.com/uleroboticsgroup/yasmin.git
# Also clone nectar-sdk if not already present
```

Build:

```bash
cd ~/ros2_ws
colcon build --packages-select nectarefa --symlink-install
source install/setup.bash
```

## Usage

### Default parameters

```bash
ros2 run nectarefa mangalarga
```

### Custom starting position and square size

```bash
ros2 run nectarefa mangalarga --initposx 1.0 --initposy -1.0 --linesize 3.0
```

### Simulation mode (SITL / Gazebo)

Set the `NECTAREFA_SIM` environment variable before launching:

```bash
NECTAREFA_SIM=1 ros2 run nectarefa mangalarga
```

### CLI Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `--initposx` | `float` | `0.5` | Initial X position for the square path |
| `--initposy` | `float` | `-0.5` | Initial Y position for the square path |
| `--linesize` | `float` | `1.5` | Side length of the square (meters) |

## Project Structure

```
nectarefa/
├── package.xml
├── setup.py
├── setup.cfg
└── nectarefa/
    ├── __init__.py
    ├── mangalarga.py        # Main entry point & state machine definition
    ├── constants.py          # Mission parameters & CLI argument parsing
    └── states/
        ├── __init__.py
        ├── basicstates.py    # Initialize, Takeoff, ReturnToLaunch, End
        └── navigation.py    # GoToFst, DoSquare
```

## License

Licensed under the [Apache License 2.0](LICENSE).

## Author

**Arthur Xavier** — [arthuraxribeiro@gmail.com](mailto:arthuraxribeiro@gmail.com)
