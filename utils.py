# -*- coding: utf-8 -*-
######################################################################
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
######################################################################
import os, re
import uuid
from numpy import frombuffer, int16, int64, mean, array


def bytestoint(frame: "bytes", channels: int) -> array:
    """ transform bytes string into an array of ints """
    return frombuffer(frame, int16)[::channels].astype(int64)

def energy(frame: "array of ints") -> int64:
    """ compute frame short term energy """
    return mean(frame**2)

def generate_file_name(folder : str, gender: bool, device_type='RS') -> str :
    """ Generate filename using pattern <GENDER>_<DEVICE_TYPE>_<UUID>.wav"""
    return "%s_%s_%s.wav" % (('M' if gender else 'F'), device_type, str(uuid.uuid4()))
