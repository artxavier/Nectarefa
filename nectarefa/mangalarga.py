'''
MAQUINA DE ESTADOS PRINCIPAL COM INITIALIZE, TAKEOFF, NAVIGATION E LAND
'''

import rclpy
import yasmin
from yasmin import StateMachine
from yasmin_ros.basic_outcomes import SUCCEED, ABORT
from yasmin_ros import set_ros_loggers


from nectarefa.constants import configure_initpos, parse_args
from nectarefa.states import Initialize, Takeoff, ReturnToLaunch, End, GoToFst, DoSquare


class nectarefaSM(StateMachine):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

        self.add_state(
            "INITIALIZE",
            Initialize(),
            transitions={SUCCEED: "TAKEOFF", ABORT: "END"},
        )

        self.add_state(
            "TAKEOFF",
            Takeoff(),
            transitions={SUCCEED: "GOTOFST", ABORT: "RETURN_TO_LAUNCH"},
        )

        self.add_state(
            "GOTOFST",
            GoToFst(),
            transitions={SUCCEED: "DOSQUARE", ABORT: "RETURN_TO_LAUNCH"},
        )

        self.add_state(
            "DOSQUARE",
            DoSquare(),
            transitions={SUCCEED: "RETURN_TO_LAUNCH", ABORT: "RETURN_TO_LAUNCH"},
        )

        self.add_state(
            "RETURN_TO_LAUNCH",
            ReturnToLaunch(),
            transitions={SUCCEED: "END", ABORT: "END"},
        )

        self.add_state("END", End(), transitions={SUCCEED: SUCCEED})


def main(args=None):
    parsed_args = parse_args(args)
    configure_initpos(parsed_args.initposx, parsed_args.initposy, parsed_args.linesize)

    yasmin.YASMIN_LOG_INFO("Iniciando a máquina de estados principal...")
    rclpy.init(args=args)
    set_ros_loggers()

    mangalarga_sm = nectarefaSM()

    try:
        avante = mangalarga_sm()
        print(avante)

    except Exception as e:
        yasmin.YASMIN_LOG_ERROR(f"Erro na execução da máquina de estados: {e}")
        mangalarga_sm.cancel_state()

    finally:
        yasmin.YASMIN_LOG_INFO("Finalizando a máquina de estados principal...")
        rclpy.shutdown()


if __name__ == "__main__":
    main()
        
        
        
        