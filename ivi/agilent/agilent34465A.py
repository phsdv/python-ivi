"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2015-2017 Hermann Kraus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .agilent34461A import *
from .. import ivi
from .. import scpi
from .. import dmm
from .. import extra

MeasurementAutoZeroMapping = {
        'dc_volts': 'volt:dc:zero:auto',
        'dc_current': 'curr:dc:zero:auto',
        'two_wire_resistance': 'res:zero:auto',
        'temperature': 'temp:zero:auto',
        }

MeasurementApertureMapping = {
        'dc_volts': 'volt:dc:aperture',
        'dc_current': 'curr:dc:aperture',
        'two_wire_resistance': 'res:aperture',
        'four_wire_resistance': 'fres:aperture',
        'frequency': 'freq:aperture',
        'period': 'per:aperture',
        'capacitance': 'cap:aperture'}

class agilent34465A(agilent34461A): 
    "Agilent 34465A IVI DMM driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '34465A')
        
        super(agilent34465A, self).__init__(*args, **kwargs)
        self._identity_description = "Agilent 34465A IVI DMM driver"
        self._identity_supported_instrument_models = ['34465A']

        self._add_property('advanced.auto_zero',
                        self._get_advanced_auto_zero,
                        self._set_advanced_auto_zero)
        
        self._add_property('advanced.aperture_time',
                        self._get_advanced_aperture_time,
                        self._set_advanced_aperture_time)
        
#        self._add_property('advanced.aperture_time_units',
#                        self._get_advanced_aperture_time_units,
#                        self._set_advanced_aperture_time_units)

        self._add_property('trigger.multi_point.sample_interval',
                        self._get_trigger_multi_point_sample_interval,
                        self._set_trigger_multi_point_sample_interval)

    def _get_advanced_auto_zero(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():

            func = self._get_measurement_function()
            if func in MeasurementAutoZeroMapping:
                cmd = MeasurementAutoZeroMapping[func]
                value = self._ask("{}?".format(cmd))
            self._advanced_auto_zero = value
            self._set_cache_valid()
        return self._advanced_auto_zero
    
    def _set_advanced_auto_zero(self, value):
        if value not in dmm.Auto:
            return ivi.ValueNotSupportedException
        func = self._get_measurement_function()
        if not self._driver_operation_simulate:
            if func in MeasurementAutoZeroMapping:
                cmd = MeasurementAutoZeroMapping[func]
                self._write("{} {}".format(cmd, value))
        self._advanced_auto_zero = value

    def _get_advanced_aperture_time(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask(":aperture?").lower()
            self._advanced_aperture_time = value  #just testting should be value
        return self._advanced_aperture_time
    
    def _set_advanced_aperture_time(self, value):
        if not self._driver_operation_simulate:
            func = self._get_measurement_function()
            if func in MeasurementApertureMapping:
                cmd = MeasurementApertureMapping[func]
                self._write("%s %g" % (cmd, value))
            self._advanced_aperture_time = value
            self._set_cache_valid()
        return self._advanced_aperture_time
    
#    def _get_advanced_aperture_time_units(self):
#        # TODO
#        return self._advanced_aperture_time_units
    
#    def _set_advanced_aperture_time_units(self, value):
#        # TODO
#        return self._advanced_aperture_time_units


    def _get_trigger_multi_point_sample_interval(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            value = self._ask("sample:tim?").lower()
            self._trigger_multi_point_sample_interval = value  #just testting should be value
        return self._trigger_multi_point_sample_interval
    
    def _set_trigger_multi_point_sample_interval(self, value):
        if not self._driver_operation_simulate:
            self._write("sample:tim {}".format(value))
        self._trigger_multi_point_sample_interval = value
