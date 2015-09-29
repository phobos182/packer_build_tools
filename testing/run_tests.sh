#!/bin/bash
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
set -x
set -e

TESTS=${TESTS:-base}

# install serverspec for testing
cd /tmp/tests

# install to local directory
bundle install --path ./gems/

# run tests
for t in $TESTS; do
  bundle exec rake spec:${t}
  mv serverspec.xml ${t}.xml
done
