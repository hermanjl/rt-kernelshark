#
# Copyright (C) International Business Machines  Corp., 2009
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# 2009-Dec-17:	Initial version by Darren Hart <dvhltc@us.ibm.com>
#

from ctracecmd import *

"""
Python interface to the tracecmd library for parsing ftrace traces

Python tracecmd applications should be written to this interface. It will be
updated as the tracecmd C API changes and try to minimze the impact to python
applications. The ctracecmd Python module is automatically generated using SWIG
and it is recommended applications not use it directly.

TODO: consider a complete class hierarchy of ftrace events...
"""

class Event(object):
    def __init__(self, pevent, record, cpu):
        self._pevent = pevent
        self._record = record
        self.cpu = cpu
        type = pevent_data_type(pevent, record)
        self._format = pevent_data_event_from_type(pevent, type)

    def __str__(self):
        return "%d.%d CPU%d %s: pid=%d comm=%s type=%d" % \
               (self.ts/1000000000, self.ts%1000000000, self.cpu, self.name,
                self.num_field("common_pid"), self.comm, self.type)

    def __del__(self):
        free_record(self._record);


    # TODO: consider caching the results of the properties
    @property
    def comm(self):
        return pevent_data_comm_from_pid(self._pevent, self.pid)

    @property
    def name(self):
        return event_format_name_get(self._format)

    @property
    def pid(self):
        return pevent_data_pid(self._pevent, self._record)

    @property
    def ts(self):
        return record_ts_get(self._record)

    @property
    def type(self):
        return pevent_data_type(self._pevent, self._record)

    def num_field(self, name):
        f = pevent_find_any_field(self._format, name)
        val = pevent_read_number_field_py(f, record_data_get(self._record))
        return val


class FileFormatError(Exception):
    pass

class Trace(object):
    """
    Trace object represents the trace file it is created with.

    The Trace object aggregates the tracecmd structures and functions that are
    used to manage the trace and extract events from it.
    """
    def __init__(self, filename):
        self._handle = tracecmd_alloc(filename)

        if tracecmd_read_headers(self._handle):
            raise FileFormatError("Invalid headers")

        if tracecmd_init_data(self._handle):
            raise FileFormatError("Failed to init data")

        self._pevent = tracecmd_get_pevent(self._handle)

    @property
    def cpus(self):
        return tracecmd_cpus(self._handle)

    def read_event(self, cpu):
        rec = tracecmd_read_data(self._handle, cpu)
        if rec:
            #rec.acquire()
            #rec.thisown = 1
            return Event(self._pevent, rec, cpu)
        return None

    def read_event_at(self, offset):
        res = tracecmd_read_at(self._handle, offset)
        # SWIG only returns the CPU if the record is None for some reason
        if isinstance(res, int):
            return None
        rec,cpu = res
        #rec.acquire()
        #rec.thisown = 1
        ev = Event(self._pevent, rec, cpu)
        return ev

    def peek_event(self, cpu):
        pass


# Basic builtin test, execute module directly
if __name__ == "__main__":
    t = Trace("trace.dat")
    print "Trace contains data for %d cpus" % (t.cpus)

    for cpu in range(0, t.cpus):
        print "CPU %d" % (cpu)
        ev = t.read_event(cpu)
        while ev:
            print "\t%s" % (ev)
            ev = t.read_event(cpu)



