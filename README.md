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

## Usage

First, you need to pull down the cloud images. The `fetch` script is used
for this. Simply type `./fetch` and the images (plus their GPG signatures)
will be downloaded.

Next, it would be wise to verify the signed image SHA256 hashes. The `verify`
script can be used for that.

Finally, create the virtual machine.  When creating a virtual machine, you must
specify the desired hostname, and the desired distribution. The default
distribution is `trusty`, but you can also specify `xenial`.

Example usage (from scratch):

    ./fetch
    ./verify
    ./create <vm-hostname> [distro]

(The `fetch` and `verify` steps only need to happen once.)

After you've finished with the virutal machine, you can easily delete it
(along with all its data):

    ./delete <vm-hostname>

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

Utility script to clear out `dnsmasq`'s lease database for `virbr0`.
Also restarts the `libvirt-bin` service.

### `get-mac`

Utility to return a consistent MAC address given the specified hostname. This
is useful so that when tearing down and recreating virtual machines with the
same name, consistent MAC addresses are used, which should cause `dnsmasq` to
hand out consistent IP addresses as well.

### `vdig`

Wrapper to use `dig` to query the `dnsmasq` running on `virbr0`.
