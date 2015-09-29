packer tools
=============

Example packer tooling to find and build AMI's


uci_locator
=============

* Find Ubuntu Cloud Images
* Example: AMI_ID=$(python ./uci_locator.py)

find_in_registry
=============

* Example EC2 query script using image tags as a registry
* Example: AMI_ID=$(python ./find_in_registry -p base -e prod -c trusty)
