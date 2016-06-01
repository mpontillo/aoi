## Introduction

Before you can deploy a cloud, you first need a blue sky. That's where `aoi`
(pronounced "ah-oh-E") comes in. (`aoi` is the Japanese word for "blue".)

`aoi` is a set of scripts that allow you to easily deploy Ubuntu cloud images
onto local virtual machines *for test purposes only*. **This tool is optimized
to create consistent test environments, and should not be used for production
environments.**

### Why virtual machines and not containers?

Because containers can behave slightly differently than a fully virtualized
host. Since `aoi` is intended for software QA, it needs to remove the
"are we in a container?" variable.

Simply, running software in containers is a separate test case. It would be
great `aoi` to support them alongside virtual machines.

### Features

`aoi` has the following features, which are interesting for creating
test environments:

#### Fast Virtual Machine Creation

When you initialize `aoi`, it uses `rsync` to download the latest Ubuntu
cloud images, then verifies them and creates a hash-based link.

The cloud images are used as a base image for any new virtual machine
launched, so virtual machines are fast to create and space-efficient.

#### Consistent MAC Addresses

When you launch an image with `aoi`, instances with the same name will always
get the same MAC address. This makes it easy to identify which nodes on the
network belong to which host, which means it's much easier to create scripts
which must work with MAC addresses.

As a side benefit, DHCP servers will provide consistent IP addresses to
test machines as well. (No more running out of IP addresses since you tore
down and rebuilt your test environment too much!)

#### Consistent SSH Keys

When you initialize `aoi`, it creates SSH host keys that will be used for
every virtual machine. That makes it easier to use `ssh`, since the host key
won't change whenever a test environment is torn down and rebuilt.

#### Runs as a Normal User

After `aoi` is initialized, no root access is required to launch new
virtual machines. Your user must belong to the `libvirtd` and `kvm` groups
(and this will be done for you automatically upon `aoi init`).

#### Compartmentalized Testing

By default, `aoi` simply uses the `virbr0` bridge that is created when
`libvirt` is installed. (A second private network is created for testing.)
There is no dependency on network configuration.

## Prerequisites

This set of scripts was developed on Ubuntu 16.04 LTS (Xenial). It is not
guaranteed to work on any other platform. (At least one script requires
`python3` at the time of this writing.)

Assuming your platform is supported, the `init` script will take care
of setting up the dependencies. See the **Installation Notes** section
for more details.

Your `~/.ssh/authorized_keys` file *MUST* be populated with whatever keys
you wish to use with the virtual machines. The cloud images do not have
a default username and password.

## Usage

You should put `aoi` in your `$PATH`. For example:

    git clone https://github.com/pontillo/aoi.git
    cd aoi
    export PATH="$(pwd):$PATH"

Running `aoi init` will take care of the tasks needed to get started. If your
user is not already in the `kvm` and `libvirtd` groups, you may need lot out
and run the script again.

Example usage (from scratch):

    aoi init
    aoi launch <release-codename> <instance-name>

By default, the *release-codename* argument can be `trusty` or `xenial`, but
cloud images for other releases can by synchronized manually.

For example, to create a virtual machine named `foo` running xenial, you
could use:

    aoi launch xenial foo

Then you can SSH to the instance (even without knowing its IP address)
using the `aoi-ssh` script:

    aoi-ssh foo

After you've finished with the virutal machine, you can easily delete it
(along with all its data):

    aoi-delete foo

### Re-synchronizing Images

As part of the `init` script, the `sync` script runs. While `sync` must only
be run once, if it is run subsequently, it will fetch the latest cloud image,
but leave the old image in place (based on its sha256 hash) in case other
images were built upon it.

## Test Networks

By default, a test network (called `testnet`) will be created by the `init`
script, using the `172.16.99.0/24` subnet (this cannot yet be configured
without changing the script).

## Command Reference

This repository also contains a few helper scripts, which can be helpful
(assuming, as the scripts do, that you are using `virbr0`).

### `aoi-get-ip-via-arp`

Returns the IP address for the specified hostname, based on its mac (returned
from `aoi-get-mac`), by looking it up in the ARP cache.

### `aoi-get-ip-via-virsh-dhcp`

Returns the IP address for the specified hostname, based on its mac (returned
from `get-mac`), by looking it up in the DHCP lease table.

### `aoi-get-mac`

Utility to return a consistent MAC address given the specified hostname. This
is useful so that when tearing down and recreating virtual machines with the
same name, consistent MAC addresses are used, which should cause `dnsmasq` to
hand out consistent IP addresses as well.

### `aoi-get-libvirt-bridge`

Gets the name of a virsh bridge, based on the virsh network name.

### `aoi-untrusted-ssh`

A wrapper that allows SSH without checking the key of the remote system.
This is used despite the "consistent SSH keys" approach for easier scripting
(but you'll appreciate the consistent keys if you need to manually poke at
a test environment).

### `aoi-ssh`

A wrapper which attempts to look up the IP address of the virtual machine
(based on the ARP cache and the expected hostname-based MAC from the
`aoi-get-mac` script), then uses `aoi-untrusted-ssh` to open a session.

### `aoi-clear-virsh-dnsmasq`

Utility script to clear out `dnsmasq`'s lease database for the default network
(most likely `virbr0`).  Also restarts the `libvirt-bin` service. Use with
caution, as this can cause virtual machines (and containers) attached to the
bridge to be disconnected until restarted.

### `aoi-dig`

Wrapper to use `dig` to query the `dnsmasq` running on `virbr0`.

## Appendix A: Installation Notes

Items in this appendix are now taken care of by the `aoi init` script.

First, you'll need to ensure the following packages are installed:

    sudo apt install libvirt-bin qemu-kvm virtinst uuid

Your user must be in the `libvirtd` and `kvm` groups for these scripts to
work:

    sudo usermod -a -G libvirtd,kvm $USER

### Possible Workaround Needed

This is currently taken care of by the `aoi init` script.

If you get errors regarding permission to access the backing images, you may
need to set the AppArmor profile for libvirt to *complain mode*:

    $ sudo apt-get install apparmor-profiles apparmor-utils
    $ sudo aa-complain /usr/lib/libvirt/virt-aa-helper
