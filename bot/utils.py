import argparse
import csv
import json
import re


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-config",
        type=str,
        default="config.json",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "-output",
        type=str,
        help="Path to the output file",
    )

    return parser.parse_args()


def read_config(config_path="config.json"):
    """Read a JSON configuration file"""
    with open(config_path, "r") as file:
        return json.load(file)


def write_to_csv(users: list, file_path: str):
    """Write the users to a CSV file"""
    with open(file_path + ".csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ["first_name", "last_name", "email", "password"]
        csv_writer.writerow(header)
        for user in users:
            row = [user.first_name, user.last_name, user.email, user.password]
            csv_writer.writerow(row)
