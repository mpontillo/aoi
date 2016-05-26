## Introduction

This repository contains a set of scripts that allow you to easily deploy
Ubuntu cloud images onto local virtual machines.

## Prerequisites

This set of scripts was developed on Ubuntu 16.04 LTS (Xenial). It is not
guaranteed to work on any other platform. (At least one script requires
`python3` at the time of this writing.)

First, you'll need to ensure the following packages are installed:

    sudo apt install libvirt-bin qemu-kvm virtinst uuid

Your `~/.ssh/authorized_keys` file *MUST* be populated with whatever keys
you wish to use with the virtual machines. The cloud images do not have
a default username and password.

Your user must be in the `libvirtd` and `kvm` groups for these scripts to
work:

    sudo usermod -a -G libvirtd,kvm $USER

### Possible Workaround Needed

If you get errors regarding permission to access the backing images, you may
need to set the AppArmor profile for libvirt to *complain mode*:

    $ sudo apt-get install apparmor-profiles apparmor-utils
    $ sudo aa-complain /usr/lib/libvirt/virt-aa-helper

## Usage

An `init` script is supplied, which will take care of the tasks needed to get
started. If your user is not already in the `kvm` and `libvirtd` groups, you
may need to run the script twice.

Example usage (from scratch):

    ./init
    ./create <vm-hostname> [distro]

For example, to create a virtual machine named `foo` running xenial, you
could use:

    ./create foo xenial

As part of the `init` script, the `sync` script runs. While `sync` must only
be run once, if it is run subsequently, it will fetch the latest cloud image,
but leave the old image in place (based on its sha256 hash) in case other
images were built upon it.

After you've finished with the virutal machine, you can easily delete it
(along with all its data):

    ./delete <vm-hostname>

## Configuring a Test Network

You can configure a test network by running the `./configure-networks` script.
This will create a `maas` network, and also redefine the domain name for the
default network to be `.vm`. This means you can look up the IP addresses
for your machines in the `.vm` domain using the `dnsmasq` running on the default
network, which is at `192.168.122.1` by default.

If you want your virutual machines to be resolved in Ubuntu, (assuming you are running
NetworkManager), you can create `/etc/NetworkManager/dnsmasq.d/libvirt.conf` as follows:

    server=/vm/192.168.122.1

This assumes that your `default` network is configured to with an IP address
of `192.168.122.1`.

## Utility Scripts

This repository also contains a few helper scripts, which can be helpful
(assuming, as the scripts do, that you are using `virbr0`).

### `get-ip-via-arp`

Returns the IP address for the specified hostname, based on its mac (returned
from `get-mac`), by looking it up in the ARP cache.

### `get-ip-via-virsh-dhcp`

Returns the IP address for the specified hostname, based on its mac (returned
from `get-mac`), by looking it up in the DHCP lease table.

### `get-mac`

Utility to return a consistent MAC address given the specified hostname. This
is useful so that when tearing down and recreating virtual machines with the
same name, consistent MAC addresses are used, which should cause `dnsmasq` to
hand out consistent IP addresses as well.

### `get-virsh-bridge`

Gets the name of a virsh bridge, based on the virsh network name.

### `ussh`

The `ussh` utility stands for **Untrusted SSH**. It is a wrapper that allows
SSH without checking the key of the remote system.

### `vssh`

The `vssh` utility stands for **VM SSH**. It is a wrapper which attempts to
look up the IP address of the virtual machine (based on the ARP cache and the
expected hostname-based MAC from the `get_mac` script), then runs `ussh` to open a session.

### `vcleardns`

Utility script to clear out `dnsmasq`'s lease database for the default network
(most likely `virbr0`).  Also restarts the `libvirt-bin` service.

### `get-mac`

Utility to return a consistent MAC address given the specified hostname. This
is useful so that when tearing down and recreating virtual machines with the
same name, consistent MAC addresses are used, which should cause `dnsmasq` to
hand out consistent IP addresses as well.

### `vdig`

Wrapper to use `dig` to query the `dnsmasq` running on `virbr0`.
