from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import HashResult
from .utils import hash_cracker_worker
from .wordlist_service import generate_dynamic_wordlist

hash_cracker_bp = Blueprint('hash_cracker', __name__)

@hash_cracker_bp.route('/crack', methods=['POST'])
@jwt_required()
def crack_hash():
    """Crack a hash using the specified hash type and wordlist."""
    data = request.get_json()
    hash_to_crack = data['hash']
    hash_type = data['hash_type']
    
    user_id = get_jwt_identity()
    wordlist = generate_dynamic_wordlist(user_id)
    
    result = hash_cracker_worker(hash_to_crack, hash_type, wordlist)
    return jsonify(result), 200
