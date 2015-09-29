#!/usr/bin/env python
import json
import logging
import optparse
import sys

import boto
import boto.ec2

# consts
_DEFAULT_ENV = 'prod'
_DEFAULT_APP = 'base'
_DEFAULT_ARCH = 'x86_64'
_DEFAULT_INSTANCE_TYPE = 'ebs'
_DEFAULT_VIRTUALIZATION = 'hvm'
_DEFAULT_RELEASE = 'precise'

# setup logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(filename)s:%(lineno)s %(levelname)s:%(message)s')


def filter_images(boto_ec2, filters):
    """
    Using the provided ec2 connection, query for all images with a filter. Return
    the ami id sorted by recent time
    :param boto_ec2: a boto.EC2Connection object
    :param filters: The dictionary of filters to apply to the query call
    :return: a dict() with the ami name, and id
    """
    result = []
    images = boto_ec2.get_all_images(owners=['self'], filters=filters)
    for _ in images:
        result.append({'name': _.name, 'id': _.id})
        print _
    # TODO: For demo purposes, please sort based on your criteria
    result.sort()
    return result.pop()


def create_image_filter(environment, application, release, instance_type, virtualization, architecture):
    """ Return dictionary representing a image filter. """
    image_filter = {'tag:environment': '{}'.format(environment),
                    'tag:application': '{}'.format(application),
                    'tag:release': '{}'.format(release),
                    'root_device_type': '{}'.format(instance_type),
                    'virtualization_type': '{}'.format(virtualization),
                    'architecture': '{}'.format(architecture)}
    return image_filter


if __name__ == '__main__':
    # Parse Options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--codename', type='string', default=_DEFAULT_RELEASE, dest='codename',
                      help='Ubuntu codename (precise, trysty)')
    parser.add_option('-e', '--environment', type='string', default=_DEFAULT_ENV, dest='environment',
                      help='Environment (test|prod|dev)')
    parser.add_option('-p', '--application', type='string', default=_DEFAULT_APP, dest='application',
                      help='Application type (base)')
    parser.add_option('-t', '--instance-type', type='string', default=_DEFAULT_INSTANCE_TYPE, dest='instance_type',
                      help='Instance Type (ebs, instance-store, ebs-ssd, ebs-io1)')
    parser.add_option('-v', '--virtualization', type='string', default=_DEFAULT_VIRTUALIZATION, dest='virtualization',
                      help='Virtualization (hvm, paravirtual)')
    parser.add_option('-a', '--architecture', type='string', default=_DEFAULT_ARCH, dest='architecture',
                      help='Architecture (x86_64)')
    parser.add_option('-q', '--quiet', action='store_true', default=False, dest='quiet',
                      help='Quiet mode. Only output AMI ID')
    (opts, args) = parser.parse_args()

    imagefilter = create_image_filter(environment=opts.environment,
                                      application=opts.application,
                                      release=opts.codename,
                                      virtualization=opts.virtualization,
                                      architecture=opts.architecture,
                                      instance_type=opts.instance_type)

    ec2 = boto.connect_ec2()
    image = filter_images(ec2, imagefilter)

    if image:
        if opts.quiet:
            print image['id']
        else:
            print json.dumps(image, indent=4)
