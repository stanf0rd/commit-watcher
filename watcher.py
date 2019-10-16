# !/usr/bin/env python3
"""
Commit-watcher entry point

Recieves requests, checks signature and proceeds data to modules

Powered by Flask
"""

# Standard library imports
import hashlib
import hmac
import logging
from enum import Enum
import json

# Third party imports
from flask import Flask, abort, request, jsonify
from flask.logging import default_handler
from gevent.pywsgi import WSGIServer

# Local application imports
from config import REPOS, CONFIG
from reporter import report
# from deployer import deploy


class CertificateError(Enum):
    """ Certificate error descriptions """
    INVALID = 1
    NO_HEADER = 2


APP = Flask(__name__)
LOGGER = APP.logger

default_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s - %(message)s",
    datefmt="%d/%b/%y %H:%M:%S"
))


@APP.route("/<app_id>", methods=["POST"])
def common(app_id):
    """
    Checks route and signature
    Sends payload to modules
    """

    if app_id not in REPOS:
        LOGGER.info("Unknown request: /%s", app_id)
        abort(404)

    app_config = REPOS.get(app_id)

    check_result = check_signature(app_config.get("MAIN"))
    if check_result == CertificateError.INVALID:
        LOGGER.warning("Request with invalid signature: /%s", app_id)
        return jsonify({"msg": "Invalid signature."}), 403
    elif check_result == CertificateError.NO_HEADER:
        LOGGER.warning("Request with no signature: /%s", app_id)
        return jsonify({"msg": "No signature."}), 403
    elif check_result != 0:
        LOGGER.error("Unknown error while checking signature")
        return jsonify({"msg": "Unknown signature error."}), 403

    event = request.headers.get("X-GitHub-Event")

    report(
        app_id,
        event,
        json.loads(request.data),
        app_config.get('MAIN')
    )

    # if "DEPLOY" in app_config and event == "push":
    #     deploy(json.loads(request.data), app_config.get("DEPLOY"))

    return "", 200


def check_signature(config):
    """ Checks signature validity reading current request """
    if "X-Hub-Signature" not in request.headers:
        return CertificateError.NO_HEADER

    signature_header = request.headers.get("X-Hub-Signature")

    if APP.debug and signature_header == "DISABLE__SIGNATURE":
        return 0

    splitted = signature_header.split("sha1=", 1)

    if len(splitted) == 1:
        return CertificateError.INVALID

    received_signature = splitted[1]

    counted_signature = create_signature(
        config.get("secret"),
        request.data,
    )
    signature_is_valid = compare_signatures(
        counted_signature,
        received_signature,
    )

    if signature_is_valid:
        return 0
    else:
        return CertificateError.INVALID


def create_signature(secret, payload):
    """ Creates signature using secret and request payolad """
    key = bytes(secret, "utf-8")
    digester = hmac.new(key=key, msg=payload, digestmod=hashlib.sha1)
    signature = digester.hexdigest()
    return signature


def compare_signatures(first, second):
    """ Safely compares two signatures """
    return hmac.compare_digest(
        str(first),
        str(second),
    )


HTTP_SERVER = WSGIServer(('', CONFIG.get('port')), APP)
HTTP_SERVER.serve_forever()
