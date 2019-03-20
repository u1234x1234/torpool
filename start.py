import argparse 
import signal
import re
import os
from subprocess import check_call, Popen, call, PIPE


def run_tor_process(tor_id, additional_args, starting_port=9050):
    command = [
        'tor',
        '--SocksPort', '127.0.0.1:{}'.format(starting_port + tor_id),
        '--DataDirectory', '/var/lib/tor/{}'.format(tor_id),
        '--PidFile', '/var/run/tor/{}.pid'.format(tor_id),

        '--RunAsDaemon', '1',
        '--ClientOnly', '1',
        '--ExitRelay', '0',
    ]
    if additional_args:
        command += additional_args

    process = Popen(command, shell=False)
    process.wait()


def prepare_privoxy_config(filename, out_filename, port, host='127.0.0.1'):
    with open(filename, 'r') as in_file:
        content = in_file.read()

    new_address = 'listen-address {}:{}'.format(host, port)
    modified_content = re.sub('^listen-address.*$', new_address, content, flags=re.MULTILINE)

    with open(out_filename, 'w') as out_file:
        out_file.write(modified_content)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--Tors', type=int, default=2)
    args = arg_parser.parse_known_args()

    parsed_args, additional_args = args

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # Start Tor processes
    for tor_id in range(parsed_args.Tors):
        run_tor_process(tor_id, additional_args)

    # Start privoxy for each Tor process
    os.makedirs('/var/run/privoxy')
    for tor_id in range(parsed_args.Tors):

        new_config_path = '/etc/privoxy/config{}'.format(tor_id)
        prepare_privoxy_config('/etc/privoxy/config', new_config_path, 8118+tor_id)
        pidfile = '/var/run/privoxy/{}'.format(tor_id)

        privoxy_process = Popen(['privoxy', '--no-daemon', '--pidfile', pidfile, new_config_path])

    check_call(['haproxy', '-f', '/etc/haproxy.conf', '-db'])
    check_call(['bash'])
