import smbus2
from TOFSensors import State


class SRF_RANGE_UNITS:
    """ SRF-XX rangefinder constants. """
    IN = 0x50
    CM = 0x51
    US = 0x52


class SRFBase(object):
    i2c = None
    bus_address = None
    old_value = 20
    """
    A base class for SRF08 and SRF10 rangefinders.
    Essentially a SRF-xx rangefinder emulates a 24xx series EEPROM and implements
    a number of user readable and writable registers. These registers map to
    the specific hardware functions and readings from the rangefinder.
    Since the '08 and '10 are very similar in their functionality this class
    serves as a base implementation which can be overridden to form a class
    for a specific sensor.
    """

    def __init__(self):
        """
        If any arguments are present self.init() is called.
        """
        super(SRFBase, self).__init__()
        self.i2c = smbus2.SMBus(1)
        self.bus_addr = 0x71
        self.rxb = bytearray(4)


    def bus_address(self, *args):
        """
        Sets the rangefinder I2C bus address if provided, otherwise returns the
        current rangefinder bus address.
        """
        if len(args) > 0:
            self.bus_addr = args[0]
        else:
            return self.bus_addr

    def scan_bus(self):
        """
        Scans I2C bus and returns a list of addresses found.
        """
        return self.i2c.scan()

    def sw_rev(self):
        """
        Returns the software revision of sensor.
        """
        rev = bytearray((256,))
        self.i2c.mem_read(rev, self.bus_addr, 0)
        if rev[0] > 255:
            raise Exception('Error reading from sensor.')
        return rev[0]

    def set_max_range(self, range_mm):
        """
        Sets the maximum range of the sensor.
        :param range_mm: Integer range in mm, min. 43mm max 11008mm.
        :return:
        """
        if range_mm < 43:
            raise ValueError('Minimum range is 43mm.')
        if range_mm > 11008:
            raise ValueError('Maximum range is 11008mm.')
        c = int(range_mm) // 43 - 1
        self.i2c.write_byte_data(self.bus_addr, 2, c)
        # self.i2c.mem_write(c, self.bus_addr, 2)

    def set_analog_gain(self, gain):
        """
        Sets the analog gain of the sensor.
        :param gain: Sensor gain register value.
        :return:
        """
        if gain < 0:
            raise ValueError('Gain register must be greater than 0.')
        self.i2c.write_byte_data(self.bus_addr, 1, int(gain))
        # self.i2c.mem_write(int(gain), self.bus_addr, 1)

    def measure_range(self):
        """
        Initiate rangefinder ranging.
        :param units: SRF_RANGE_UNITS, either IC, CM, or US for µ seconds.
        :return:
        """

        self.i2c.write_byte_data(self.bus_addr, 0, SRF_RANGE_UNITS.CM)
        # self.i2c.mem_write(units, self.bus_addr, 0)

    def read_range(self):
        """
        Read the range registers after ranging has completed.
        :param:
        :return: A list of integer range values in the units specified by
        measure_range(). In the case of sensors which report multiple echos,
        the first item in the list represents the first echo and the nth item
        represents the nth echo. If no echos were returned list will be empty.
        """
        self.rxb = self.i2c.read_i2c_block_data(self.bus_addr, 0, 4)
        print(str(self.rxb))
        # self.i2c.mem_read(self.rxb, self.bus_addr, 0)
        values = []
        # skip first 2 bytes, then unpack high and low bytes from buffer data
        # data is pack in big-endian form
        for i in range(2, len(self.rxb), 2):
            range_val = (self.rxb[i] << 8) + self.rxb[i + 1]
            if range_val > 0:
                values.append(range_val)
        values.append(self.rxb[0])
        return values

    def measure_and_read(self):
        values = self.read_range()
        if values[-1] != 255:
            # writes the measured values into registers on the sensor.
            new_value = values[0]
            self.measure_range()
            print("Abstand SRF10 in cm : {}".format(values[0]))
            result =(new_value + self.old_value) / 2
            self.old_value = new_value
            return result
        return self.old_value


class SRF08(SRFBase):
    """
    A SRF08 Rangefinder.
    Supports up to 17 echo range values.
    Maximum analog gain of 31.
    TODO: Add ability to read light meter.
    """

    def __init__(self, *args, **kwargs):
        super(SRF08, self).__init__(*args, **kwargs)
        self.rxb = bytearray(36)

    def __str__(self):
        return '<SRF08 address {} on {}>'.format(self.bus_addr, self.i2c)

    def set_analog_gain(self, gain):
        if gain > 31:
            raise ValueError('Gain register must be less than or equal to 31.')
        super(SRF08, self).set_analog_gain(gain)


class SRF02(SRFBase):
    """
    A SRF10 rangefinder.
    Supports single echo range value.
    Maximum analog gain of 16.
    """
    srf02_state = State.FREE

    def __str__(self):
        return '<SRF10 address {} on {}>'.format(self.bus_addr, self.i2c)

    def set_analog_gain(self, gain):
        if gain > 16:
            raise ValueError('Gain register must be less than or equal to 16.')
        super(SRF02, self).set_analog_gain(gain)

    def run(self):
        """
        Starts measuring the distance and sets the state of the sensor according to the distance measured.
        The sensor is blocked if the distance is less than 25 cm and free if the distance is more than 25 cm.
        :return:
        """
        measured_distance = self.measure_and_read()
        if measured_distance < 25:
            self.srf02_state = State.BLOCKED
        else:
            self.srf02_state = State.FREE
