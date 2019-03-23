import argparse 
import signal
import re
import os
from subprocess import check_call, Popen, call, PIPE
from jinja2 import Template


PRIVOXY_BASE_PORT = 8118
SOCKS_BASE_PORT = 9050
HAPROXY_CONFIG_PATH = '/etc/haproxy.conf'


def run_tor_process(tor_id, additional_args, host='127.0.0.1'):
    port = SOCKS_BASE_PORT + tor_id

    command = [
        'tor',
        '--SocksPort', '{}:{}'.format(host, port),
        '--DataDirectory', '/var/lib/tor/{}'.format(tor_id),
        '--PidFile', '/var/run/tor/{}.pid'.format(tor_id),

        '--RunAsDaemon', '1',
        '--ClientOnly', '1',
        '--ExitRelay', '0',
        '--MaxCircuitDirtiness', '30',
        '--NewCircuitPeriod', '30',
    ]
    if additional_args:
        command += additional_args

    process = Popen(command, shell=False)
    process.wait()


def prepare_privoxy_config(
        default_config_path, new_config_path, listen_port, socks_port,
        listen_host='0.0.0.0', socks_host='127.0.0.1'):

    with open(default_config_path, 'r') as in_file:
        content = in_file.read()

    new_address = 'listen-address {}:{}'.format(listen_host, listen_port)
    modified_content = re.sub('^listen-address.*$', new_address, content, flags=re.MULTILINE)

    modified_content += '\n' + 'forward-socks5 / {}:{} .'.format(socks_host, socks_port)

    with open(new_config_path, 'w') as out_file:
        out_file.write(modified_content)


def run_privoxy_process(tor_id):
    os.makedirs('/var/run/privoxy', exist_ok=True)

    default_config_path = '/etc/privoxy/config'
    new_config_path = '/etc/privoxy/config{}'.format(tor_id)
    prepare_privoxy_config(default_config_path, new_config_path, PRIVOXY_BASE_PORT+tor_id, SOCKS_BASE_PORT+tor_id)
    pidfile = '/var/run/privoxy/{}'.format(tor_id)

    privoxy_process = Popen(['privoxy', '--no-daemon', '--pidfile', pidfile, new_config_path])


def update_haproxy_config(config_path, n_processes):
    with open(config_path, 'r') as in_file:
        template = Template(in_file.read())

    config = template.render(
        http_ports=[PRIVOXY_BASE_PORT + i for i in range(n_processes)],
        socks_ports=[SOCKS_BASE_PORT + i for i in range(n_processes)])

    with open(config_path, 'w') as out_file:
        out_file.write(config)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--Tors', type=int, default=2)
    args = arg_parser.parse_known_args()

    parsed_args, additional_args = args
    print(parsed_args, additional_args)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # Start Tor processes
    for tor_id in range(parsed_args.Tors):
        run_tor_process(tor_id, additional_args)

    # Start privoxy for each Tor process
    for tor_id in range(parsed_args.Tors):
        run_privoxy_process(tor_id)

    update_haproxy_config(HAPROXY_CONFIG_PATH, parsed_args.Tors)

    check_call(['haproxy', '-f', HAPROXY_CONFIG_PATH, '-db'])
