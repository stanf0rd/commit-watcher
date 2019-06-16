# !/usr/bin/env python3
"""
Commit-watcher entry point

Recieves requests, check signature and proceeds data to modules

Powered by Flask
"""

# Standard library imports
import hashlib
import hmac
import logging

# Third party imports
from flask import Flask, abort, request, jsonify
from flask.logging import create_logger

# Local application imports
from config import WATCHER_CONFIG


APP = Flask(__name__)
LOGGER = create_logger(APP)

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)


@APP.route('/<app_id>', methods=['POST'])
def common(app_id):
    """
    Checks route and signature
    Sends payload to modules
    """
    if app_id in WATCHER_CONFIG.get('repos'):
        if 'X-Hub-Signature' not in request.headers:
            LOGGER.warning("Request with no signature: /%s", app_id)
            return jsonify({"msg": "No signature."}), 403

        counted_signature = create_signature(
            WATCHER_CONFIG.get('repos').get(app_id).get('secret'),
            request.data
        )
        signature_is_valid = check_signature(
            counted_signature,
            request.headers.get('X-Hub-Signature'),
        )
        if not signature_is_valid:
            LOGGER.warning("Request with invalid signature: /%s", app_id)
            return jsonify({"msg": "Invalid signature."}), 403

        return '', 200
    else:
        LOGGER.info("Unknown request: /%s", app_id)
        abort(404)


def create_signature(secret, payload):
    """ Creates signature using secret and request payolad """
    key = bytes(secret, 'utf-8')
    digester = hmac.new(key=key, msg=payload, digestmod=hashlib.sha1)
    signature = digester.hexdigest()
    return signature


def check_signature(first, second):
    """ Safely compares two signatures """
    return hmac.compare_digest(
        str(first),
        str(second),
    )
