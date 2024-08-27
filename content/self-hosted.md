---
Title: Personal data and self hosting
Date: 2024-08-26
Category: technical
Tags: self-hosted
Summary: Details of how I how self host services to maintain a degree of
         digital privacy and freedom.
Status: published
---

{% import 'post-macros.html' as macros %}

{{ macros.image('self-hosted/boxes.jpg') }}

As part of a conscious effort to reduce or remove my dependence on cloud
services for storing my data, I have been running a modest self-hosted setup
for quite a few years, which has worked well and required very little ongoing
maintenance. I haven’t attempted to self-host services like email, opting
instead for trusted providers. This short note goes over the main details.

The goals for my personal computing are:

- To have complete control over my personal data, giving me flexibility over
  how to manage and access it. Even with GDPR, this would be an ambitious goal for
  all personal data, so I really mean files and media created on personal
  computing devices. Anything that I can download from a cloud service, I aim
  backup on my own storage, or master it there if I no longer require access via
  the cloud service.

- To have independence from companies that (a) offer free services in return
  for collecting profiling data or to target adverts at me, (b) lock me in as a
  user so it is hard to move to another service and (c) to avoid services that I
  come to rely on being end-of-lifed.

- To have a system that is simple to set up, maintain, use, upgrade and
  possibly/eventually to migrate from.

- To provide a significant amount of storage (in personal data terms, ~tens of TBs).
  This is because accessing volumes of data this large through cloud services can be
  expensive when you factor in monthly charges and transfer costs.


## Details

The main philosophy of my approach is to minimise maintenance effort whilst
still achieving the above goals, so my setup is very vanilla. Many more exotic
and interesting self hosted systems can be found (I’ve linked to a few
resources at [the end][#links]).

The main machine is a Synology Diskstation DS220+, a two-bay network-attached-storage (NAS) box.
I have this running with two 8 TB disks in RAID 1 configuration (two-way redundant
using one disk as a mirror), and I upgraded it with 16GB of memory in addition to the
2 GB it comes with. There are many applications that Synology provide, but the main ones
I use are:

- Fileserver (SMB for access via Windows and Mac machines, and the Drive app for accessing and syncing files).
- Photos (in particular the photos mobile app automatically syncs photos to the NAS for backup).
- Music.
- Hyperbackup.
- VPN server.
- DNS server.

The big advantage of a Synology system is good hardware complemented
by their ecosystem of applications, spanning iPhone and Android too. The catch
is that this ecosystem is closed source and managed by Synology. As such, support for old
hardware is eventually dropped and some software packages are deprecated.
To mitigate these problems, an alternative is TrueNAS (formerly FreeNAS), running on
some suitable hardware. Other non-Synology software can be run on
a Synology device using Docker, however I've had problems doing this with constant disk
accesses caused by
[container health checks](https://www.reddit.com/r/synology/comments/xpn5rh/docker_constant_hdd_readwrite).

A neat feature of Synology is their [Quickconnect](https://quickconnect.to)
remote access, without needing a VPN or having an open port. This works with
the web interface and phone apps.

The single most important aspect of managing personal data is ensuring it is
robustly backed up. RAID 1 provides protection against loss of a single disk
(and Synology handles this well), but not against damage to the system such as would
happen in an accident or fire. To mitigate this, I have setup an off-site backup
using another Synology Diskstation NAS. A full incremental backup
is performed nightly using Synology's Hyperbackup. I have checked that files
are retrievable but I admit I have not tried a full system restore since it has
not yet been necessary.

## Linux host

The second box in the picture above is a Lenovo ThinkCentre M75q Tiny PC that I
got to plug the gap in the Synology's capabilities, namely in running
additional services and providing a Linux host that I can use for development
etc, rather than paying for an under powered VPS. The machine has a Ryzen 5
3400GE processor with 16GB DDR3 RAM  and a 500 GB NVMe SSD. You can pick these
machines up very cheaply.

{{ macros.image('self-hosted/homepage.png') }}

Currently it runs:

- [Homepage](https://gethomepage.dev) providing a general internal landing page for statuses and convenient links.
- [FreshRSS](https://freshrss.org) for aggregating and reading RSS feeds.
- [Speedtest Tracker](https://speedtest-tracker.dev) for monitoring my internet connection.
- [Octograph](https://github.com/Yanson/octograph) for monitoring my home electricity use and pricing.


## Access

Using Synology VPN server on the DS220+, I have an OpenVPN service setup that
allows me to access my home network remotely. This gives me access to the
various services, as well as to machines via RDP and SSH. Within the network, I
have a local DNS service (also running on the DS220+) to provide convenient
names for devices.


## Other services

As I mentioned at the start, there are a number of third-party services that I
use. The key ones are:

- [Proton](https://proton.me) primarily for email, calendar and passwords.
- [Github](https://github.com) for code and Github pages for hosting this website (at the time of writing).
- [Digital Ocean](https://www.digitalocean.com) for object storage with Spaces.
- [Google Sheets](https://docs.google.com) for word processing and spreadsheets.
- [Standard notes](https://standardnotes.com) for note taking, since they have
  recently been acquired by Proton.
- [Apple iCloud](https://www.icloud.com) for contacts and reminders.
- [Strava](https://www.strava.com) and [Garmin](https://connect.garmin.com) for fitness data.

This list is not exhaustive but these services all hold valuable data that I
would not want to lose in the event the provider loses the data or I get
locked out of my account. Although these scenarios is unlikely, I mitigate the
risks by taking manual backups, albeit on a less frequent basis that I should.


## Summary

This note details hardware and software alternatives for operating personal services
that are east to setup and maintain, with scope to add much more functionality. This
approach provides a strong alternative to entrusting a third party to hold your data.
Moreover, it can be done cheaply too, with the cost of NAS setups being dominated by the
price of disks themselves and many great open-source software options.

<a name="links"></a>
## Related links

There are many great blog posts about self hosting of computing services. These
are a few that I have come across.

- [Awesome-Selfhosted](https://awesome-selfhosted.net)
- [How I Computer in 2024](https://jnsgr.uk/2024/07/how-i-computer-in-2024), blog post by Jon Seager.
- [My homelab setup](https://blog.fidelramos.net/software/homelab), blog post by Fidel Ramos.
- [Building a DIY Home Server with FreeNAS](https://www.devroom.io/2020/02/28/building-a-diy-home-server-with-freenas), devroom.io.
