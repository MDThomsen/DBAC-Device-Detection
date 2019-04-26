#!/usr/bin/env python

"""
Modified version of https://github.com/JoelBender/bacpypes/blob/master/samples/Tutorial/SampleConsoleCmd.py
under MIT license.
"""

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run, enable_sleeping

from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.object import Object, ObjectIdentifierProperty,AnalogInputObject,ObjectIdentifier
import bacpypes.basetypes

# some debugging
_debug = 0
_log = ModuleLogger(globals())



@bacpypes_debugging
class DebugApplication(BIPSimpleApplication):
    def __init__(self, device, address):
        if _debug: DebugApplication._debug("__init__ %r %r", device, address)
        BIPSimpleApplication.__init__(self, device, address)

    def request(self, apdu):
        if _debug: DebugApplication._debug("request %r", apdu)
        BIPSimpleApplication.request(self, apdu)

    def indication(self, apdu):
        if _debug: DebugApplication._debug("indication %r", apdu)
        BIPSimpleApplication.indication(self, apdu)

    def response(self, apdu):
        if _debug: DebugApplication._debug("response %r", apdu)
        BIPSimpleApplication.response(self, apdu)

    def confirmation(self, apdu):
        if _debug: DebugApplication._debug("confirmation %r", apdu)
        BIPSimpleApplication.confirmation(self, apdu)

def main():
    # parse the command line arguments
    args = ConfigArgumentParser(description=__doc__).parse_args()

    if _debug: _log.debug("initialization")
    if _debug: _log.debug("    - args: %r", args)

    # make a device object
    this_device = LocalDeviceObject(
        objectName=args.ini.objectname,
        objectIdentifier=int(args.ini.objectidentifier),
        maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
        segmentationSupported=args.ini.segmentationsupported,
        vendorIdentifier=int(args.ini.vendoridentifier)
    )

    # make a sample application
    this_application = DebugApplication(this_device, args.ini.address)

    analog_input_object = AnalogInputObject(
        objectName='Temperature Sensor',
        objectIdentifier=('analogInput',0),
        objectType='analogInput',
        presentValue=21,
        statusFlags=bacpypes.basetypes.StatusFlags.bitNames['inAlarm'],
        eventState=bacpypes.basetypes.EventState.enumerations['normal'],
        outOfService=False,
        units='degreesCelsius'
    )

    this_application.add_object(analog_input_object)


    '''
    # make a console
    this_console = SampleConsoleCmd()
    if _debug: _log.debug("    - this_console: %r", this_console)
    '''

    # enable sleeping will help with threads
    enable_sleeping()

    _log.debug("running")

    run()

    _log.debug("fini")

if __name__ == "__main__":
    main()