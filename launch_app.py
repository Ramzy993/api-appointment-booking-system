#!/usr/bin/env python3

# lib imports

# project imports


from abs.web_app.app import start_app
from abs.common.log_manager.log_manger import LogManager


if __name__ == '__main__':
    LogManager().info("Welcome to Appointment Booking System ....")
    start_app()
