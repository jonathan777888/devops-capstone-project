from flask import Blueprint, jsonify, request

accounts_bp = Blueprint("accounts", __name__)

ACCOUNTS = {}
NEXT_ACCOUNT_ID = 1


def reset_accounts():
    global ACCOUNTS, NEXT_ACCOUNT_ID
    ACCOUNTS = {}
    NEXT_ACCOUNT_ID = 1


@accounts_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Customer Accounts Service is running"}), 200


@accounts_bp.route("/accounts", methods=["POST"])
def create_account():
    global NEXT_ACCOUNT_ID

    data = request.get_json(silent=True) or {}

    account = {
        "id": NEXT_ACCOUNT_ID,
        "name": data.get("name"),
        "email": data.get("email"),
        "address": data.get("address")
    }

    ACCOUNTS[NEXT_ACCOUNT_ID] = account
    NEXT_ACCOUNT_ID += 1

    return jsonify(account), 201


@accounts_bp.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify(list(ACCOUNTS.values())), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = ACCOUNTS.get(account_id)

    if account is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(account), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = ACCOUNTS.get(account_id)

    if account is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json(silent=True) or {}
    account.update(data)

    return jsonify(account), 200


@accounts_bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    if account_id not in ACCOUNTS:
        return jsonify({"error": "Account not found"}), 404

    del ACCOUNTS[account_id]

    return "", 204
