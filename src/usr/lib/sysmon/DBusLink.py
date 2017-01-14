#!/usr/bin/env python3

from dbus import SystemBus, SessionBus, Interface

bus = SystemBus()
systemd = bus.get_object('org.freedesktop.systemd1',
                        '/org/freedesktop/systemd1')

manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')

manager.