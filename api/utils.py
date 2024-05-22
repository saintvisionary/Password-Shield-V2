import hashlib
from .models import HashResult
from .ml.gpt2_model import generate_passwords_with_gpt2
from .ml.lstm_model import predict_passwords_with_lstm
from kafka import KafkaProducer
import json
import os
import requests
from .blockchain_service import log_to_blockchain

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

def generate_token(user):
    # Implement token generation logic
    pass

def verify_token(token):
    # Implement token verification logic
    pass

def hash_cracker_worker(hash_to_crack, hash_type, wordlist):
    """Crack the given hash using the specified hash type and wordlist."""
    hash_function = getattr(hashlib, hash_type.lower().replace('-', ''))
    for word in wordlist:
        if hash_function(word.encode()).hexdigest() == hash_to_crack:
            new_passwords = generate_passwords_with_gpt2(word)
            predicted_passwords = predict_passwords_with_lstm(word)
            result = f"Password found: {word}. Suggested new passwords: {new_passwords + predicted_passwords}"
            save_result_to_db(hash_type, hash_to_crack, result)
            log_to_blockchain(hash_type, hash_to_crack, result)
            return result

    result = "Password not found"
    save_result_to_db(hash_type, hash_to_crack, result)
    return result

def save_result_to_db(hash_type, hash_value, result):
    """Save the hash result to the database and send it to Kafka."""
    hash_result = HashResult(hash_type=hash_type, hash_value=hash_value, result=result)
    hash_result.save_to_db()
    kafka_producer.send('hash_cracking_results', json.dumps(result).encode('utf-8'))

def check_breach_status(password):
    """Check if the password has been breached using the Have I Been Pwned API."""
    url = "https://api.haveibeenpwned.com/api/v2/breachedaccount/"
    headers = {'User-Agent': 'PasswordShield'}
    response = requests.get(url + password, headers=headers)
    if response.status_code == 200:
        return True
    return False
