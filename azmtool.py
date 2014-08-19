#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import argparse


parser = argparse.ArgumentParser(description='Antizapret manipulation tool. https://github.com/AntiZapret/antizapret')

parser.add_argument('-i',
                    help='input blacklist filename in json format',
                    dest='filename',
                    type=argparse.FileType('r'),
                    default='blacklist4.json')

parser.add_argument('-o',
                    default='plain',
                    choices=['plain', 'iptables', 'nginx403', 'nginx404', 'p2p'],
                    help='output format')

args = parser.parse_args()

blacklist = json.load(args.filename)


def gen_plain(b_list):
    out_list = []
    for _ in b_list:
        for e in _['ranges']:
            # "dirty list" hack
            if not e[0] == '#':
                out_list.append(str(e))
    return out_list


def gen_nginx403(b_list):
    print '''# add this to section in site specific config file, usually /etc/nginx/sites-available/
location / {'''

    for _ in gen_plain(b_list):
        print '    deny {};'.format(_)

    print '''    allow all;
    ...
}'''


def gen_nginx404(b_list):
    print '''# add this to section in main nginx config file, usually /etc/nginx/nginx.conf
http {
    geo $gov_ip {
        default 0;'''

    for _ in gen_plain(b_list):
        print '        {} 1;'.format(_)

    print '''     }
     ...
}

# add this to section in site specific config file, usually /etc/nginx/sites-available/
location / {
    if ($gov_ip != 0) {
        return 404;
    }
    ...
}'''


def gen_iptables(b_list):
    for _ in gen_plain(b_list):
        print "iptables -A INPUT -s {} -j DROP".format(_)


def gen_p2p(b_list):
    def subnet2range(ip_mask):
        (addr_string, cidr_string) = ip_mask.split('/')
        addr = addr_string.split('.')
        cidr = int(cidr_string)
        mask = [0, 0, 0, 0]
        for i in range(cidr):
            mask[i / 8] += 1 << (7 - i % 8)

        net = []
        for i in range(4):
            net.append(int(addr[i]) & mask[i])

        broad = list(net)
        brange = 32 - cidr
        for i in range(brange):
            broad[3 - i / 8] += 1 << (i % 8)

        return addr_string + '-' + ".".join(map(str, broad))

    for cur_item in b_list:
        for _ in cur_item['ranges']:
            # "dirty list" hack
            if not _[0] == '#':
                print u'{}:{}'.format(cur_item['name']['trans'], subnet2range(_))


if args.o == 'iptables':
    gen_iptables(blacklist)

elif args.o == 'nginx403':
    gen_nginx403(blacklist)

elif args.o == 'nginx404':
    gen_nginx404(blacklist)

elif args.o == 'p2p':
    gen_p2p(blacklist)

else:
    print '\n'.join(gen_plain(blacklist))
