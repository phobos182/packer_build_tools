#!/usr/bin/env python
import logging
import optparse
import sys

import urllib2

# consts
_DEFAULT_REGION = 'us-east-1'
_DEFAULT_INSTANCE_TYPE = 'ebs'
_DEFAULT_ARCH = 'amd64'
_DEFAULT_VIRTUALIZATION = 'hvm'
_DEFAULT_CODENAME = 'trusty'
_UCI_URL = 'http://cloud-images.ubuntu.com/query/{}/server/released.current.txt'

# setup logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(filename)s:%(lineno)s %(levelname)s:%(message)s')


def get_current_list(codename):
    """
    Download current list from Ubuntu cloud-images
    :param codename: The codname of the images to search. Ex: precise, trusty
    :return: a dict() representing the metadata about the ami found
    """
    amis = {}
    response = urllib2.urlopen(_UCI_URL.format(codename))
    # Look at each line in the resulting text response
    body = response.read()
    for l in body.split('\n'):
        # if line is empty, skip it
        if not l:
            continue
        try:
            line_list = l.split('\t')
            ami_id = line_list[7]
            amis[ami_id] = {}
            amis[ami_id]['name'] = line_list[0]
            amis[ami_id]['type'] = line_list[1]
            amis[ami_id]['release'] = line_list[3]
            amis[ami_id]['instance-type'] = line_list[4]
            amis[ami_id]['arch'] = line_list[5]
            amis[ami_id]['region'] = line_list[6]
            amis[ami_id]['virtualization'] = line_list[10]
        except Exception, e:
            log.error('exception processing line: {}, {}'.format(e))
    return amis


def query_instance(amis, region, instance_type, arch, virtualization):
    """
    Query the AMI locator with the passed in filter. Return a list of ami id's
    which match the query.
    :param amis: The dict() of ami metadata from the UCI api
    :param region: the region of the image. Ex: us-east-1
    :param instance_type: The instance type. Ex: instance-store, ebs, ebs-io1, ebs-ssd
    :param arch: The architecture of the imag. Ex: amd64
    :param virtualization: The virtualization type of the image. Ex: hvm
    :return: a list of ami id's which matches the query
    """
    result_list = [_ for _ in amis if all([instance_type == amis[_]['instance-type'],
                                           virtualization == amis[_]['virtualization'],
                                           arch == amis[_]['arch'],
                                           region == amis[_]['region']])]
    return result_list


if __name__ == '__main__':
    #_ Parse Options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--codename', type='string', default=_DEFAULT_CODENAME, dest='codename',
                      help='Ubuntu codename (precise, trusty)')
    parser.add_option('-r', '--region', type='string', default=_DEFAULT_REGION, dest='region',  help='AWS Region (us-east-1, us-west-2')
    parser.add_option('-t', '--instance-type', type='string', default=_DEFAULT_INSTANCE_TYPE, dest='instance_type',
                      help='Instance Type (instance-store, ebs, ebs-io1, ebs-ssd)')
    parser.add_option('-a', '--arch', type='string', default=_DEFAULT_ARCH, dest='arch',
                      help='Architecture (amd64, i386)')
    parser.add_option('-v', '--virtualization', type='string', default=_DEFAULT_VIRTUALIZATION, dest='virtualization',
                      help='Virtualization (hvm, paravirtual)')
    (opts, args) = parser.parse_args()

    # get the current amis
    ami_list = get_current_list(opts.codename)

    # filter the amis
    result = query_instance(ami_list,
                            region=opts.region,
                            instance_type=opts.instance_type,
                            arch=opts.arch,
                            virtualization=opts.virtualization)

    # for demo purposes, print the first ami
    if result:
        ami = result.pop()
    else:
        log.error('Could not find an ami based on query')
        sys.exit(1)

    print ami
