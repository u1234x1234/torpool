import argparse 
from subprocess import check_call, Popen


def run_tor_process(tor_id, args, starting_port=9050):
    Popen([
        'tor',
        '--SocksPort', '{}'.format(starting_port + tor_id),
        '--DataDirectory', '/var/lib/tor/{}'.format(tor_id),
        '--PidFile', '/var/run/tor/{}.pid'.format(tor_id),

        '--RunAsDaemon', '1',
        '--ClientOnly', '1',
        '--ExitRelay', '0',
    ] + args
    )


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--Tors', type=int, default=2)
    args = arg_parser.parse_known_args()

    print(args)

    for tor_id in range(args[0].Tors):
        run_tor_process(tor_id, args[1])

    check_call('bash')
