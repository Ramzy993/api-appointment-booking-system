#!/usr/bin/env python3

# lib imports
from datetime import datetime
import re

# project imports
from src.db_manager.db_driver import DBDriver
from src.common.log_manager.log_manger import LogManager
from src.common.config_manager.config_manager import ConfigManager


DATETIME_FORMAT = '%d-%b-%Y %H:%M:%S'


def validate_date_format(date_text):
    try:
        datetime.strptime(date_text, DATETIME_FORMAT)
        return True
    except:
        return False


def get_datetime_diff_second(start_datetime, end_datetime):
    start_datetime = datetime.strptime(start_datetime, DATETIME_FORMAT)
    end_datetime = datetime.strptime(end_datetime, DATETIME_FORMAT)
    return (end_datetime - start_datetime).total_seconds()


class AppointmentHandler:
    def __init__(self):
        self.max_hours = ConfigManager().get_int('APPOINTMENT', 'max_hours')
        self.validation_messages = []

    def appointment_checker(self, appointment_start_datetime, appointment_end_datetime):
        if not self.__check_appointment_str(appointment_start_datetime, appointment_end_datetime):
            return False, self.validation_messages

        if not self.__check_appointment_period(appointment_start_datetime, appointment_end_datetime):
            return False, self.validation_messages

        if not self.__check_appointment_availability(appointment_start_datetime, appointment_end_datetime):
            return False, self.validation_messages

        return True, self.validation_messages

    def __check_appointment_str(self, appointment_start_datetime, appointment_end_datetime):
        if not validate_date_format(appointment_start_datetime):
            self.validation_messages.append("Incorrect start datetime format, should be DD-MMM-YYYY HH:MM:SS")
            return False

        if not validate_date_format(appointment_end_datetime):
            self.validation_messages.append("Incorrect end datetime format, should be DD-MMM-YYYY HH:MM:SS")
            return False

        return True

    def __check_appointment_period(self, appointment_start_datetime, appointment_end_datetime):
        seconds = get_datetime_diff_second(appointment_start_datetime, appointment_end_datetime)

        if seconds < 0:
            self.validation_messages.append("End datetime is less than start datetime.")
            return False
        elif seconds == 0:
            self.validation_messages.append("End datetime is equal than start datetime.")
            return False
        elif seconds > 3600 * self.max_hours:
            self.validation_messages.append(f"Max hours for an appointment is {self.max_hours} Hours.")
            return False
        else:
            return True

    def __check_appointment_availability(self, appointment_start_datetime, appointment_end_datetime):
        appointments = DBDriver().get_appointments(appointment_start_datetime=appointment_start_datetime,
                                                   appointment_end_datetime=appointment_end_datetime)
        if len(appointments) > 0:
            self.validation_messages.append("This time slot is not available.")
            return False
        return True
