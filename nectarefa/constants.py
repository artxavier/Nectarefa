
import argparse
import os


TAKEOFFHEIGHT = 3.0
LINESIZE = 1.5
INITPOSX = 0.5
INITPOSY = -0.5
RTL_ALTITUDE = 3.0

SIM_MODE = os.environ.get("NECTAREFA_SIM", "0") == "1"


def configure_initpos(initposx: float, initposy: float, linesize: float) -> None:
    global INITPOSX, INITPOSY, LINESIZE
    INITPOSX = float(initposx)
    INITPOSY = float(initposy)
    LINESIZE = float(linesize)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the nectarefa state machine")
    parser.add_argument("--initposx", type=float, default=INITPOSX, help="Initial X position")
    parser.add_argument("--initposy", type=float, default=INITPOSY, help="Initial Y position")
    parser.add_argument("--linesize", type=float, default=LINESIZE, help="Size of the line")
    return parser


def parse_args(args=None):
    parser = build_parser()
    parsed, _ = parser.parse_known_args(args)
    return parsed