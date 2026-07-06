from nectarefa import constants


def test_configure_initpos_updates_values():
    constants.configure_initpos(12.3, 45.6)

    assert constants.INITPOSX == 12.3
    assert constants.INITPOSY == 45.6


def test_parse_args_accepts_initpos_arguments():
    args = constants.build_parser().parse_args(["--initposx", "1.5", "--initposy", "2.5"])

    assert args.initposx == 1.5
    assert args.initposy == 2.5
