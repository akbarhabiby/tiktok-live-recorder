import argparse
import re
import os

from utils.custom_exceptions import ArgsParseError
from utils.enums import Mode, Regex


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="TikTok Live Recorder - A tool for recording live TikTok sessions.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-url",
        dest="url",
        help="Record a live session from the TikTok URL.",
        action='store'
    )

    parser.add_argument(
        "-user",
        dest="user",
        help="Record a live session from the TikTok username.",
        action='store'
    )

    parser.add_argument(
        "-room_id",
        dest="room_id",
        help="Record a live session from the TikTok room ID.",
        action='store'
    )

    parser.add_argument(
        "-mode",
        dest="mode",
        help=(
            "Recording mode: (manual, automatic) [Default: manual]\n"
            "[manual] => Manual live recording.\n"
            "[automatic] => Automatic live recording when the user is live."
        ),
        default="manual",
        action='store'
    )

    parser.add_argument(
        "-proxy",
        dest="proxy",
        help=(
            "Use HTTP proxy to bypass login restrictions in some countries.\n"
            "Example: -proxy http://127.0.0.1:8080"
        ),
        action='store'
    )

    parser.add_argument(
        "-output",
        dest="output",
        help=(
            "Specify the output directory where recordings will be saved.\n"
        ),
        action='store'
    )

    parser.add_argument(
        "-duration",
        dest="duration",
        help="Specify the duration in seconds to record the live session [Default: None].",
        type=int,
        default=None,
        action='store'
    )

    args = parser.parse_args()

    return args


def validate_and_parse_args():
    args = parse_args()

    args.output = os.getenv("TLR_OUTPUT") or args.output
    args.url = os.getenv("TLR_URL") or args.url
    args.user = os.getenv("TLR_USERNAME") or args.user
    args.room_id = os.getenv("TLR_ROOM_ID") or args.room_id
    args.duration = int(os.getenv("TLR_DURATION", 0)) or args.duration
    args.mode = os.getenv("TLR_MODE") or args.mode

    if not args.user and not args.room_id and not args.url:
        raise ArgsParseError("Missing URL, username, or room ID. Please provide one of these parameters.")

    if not args.mode:
        raise ArgsParseError("Missing mode value. Please specify the mode (manual or automatic).")
    if args.mode not in ["manual", "automatic"]:
        raise ArgsParseError("Incorrect mode value. Choose between 'manual' and 'automatic'.")

    if args.url and not re.match(str(Regex.IS_TIKTOK_LIVE), args.url):
        raise ArgsParseError("The provided URL does not appear to be a valid TikTok live URL.")

    if (args.user and args.room_id) or (args.user and args.url) or (args.room_id and args.url):
        raise ArgsParseError("Please provide only one among username, room ID, or URL.")

    mode = Mode.MANUAL if args.mode == "manual" else Mode.AUTOMATIC

    return args, mode
