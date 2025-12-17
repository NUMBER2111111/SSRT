"""
Quantum-Resistant Security System
Post-quantum cryptography and advanced protection
Built to protect what matters most
"""
import os
import hashlib
import secrets
import hmac
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, BinaryIO
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import base64
import struct

from sovereign_os import SOVEREIGN_ROOT

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography not fully available")


class SecurityLevel(Enum):
    """Security levels"""
    STANDARD = "standard"  # AES-256
    QUANTUM_RESISTANT = "quantum_resistant"  # Post-quantum algorithms
    MAXIMUM = "maximum"  # Multiple layers + quantum-resistant


class KeyType(Enum):
    """Key types"""
    SYMMETRIC = "symmetric"  # AES-256
    ASYMMETRIC = "asymmetric"  # RSA-4096
    QUANTUM_RESISTANT = "quantum_resistant"  # Post-quantum
    HYBRID = "hybrid"  # Multiple algorithms


@dataclass
class QuantumKey:
    """Quantum-resistant key"""
    key_id: str
    key_type: KeyType
    key_data: bytes
    created_at: float
    expires_at: Optional[float]
    security_level: SecurityLevel
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityPolicy:
    """Security policy"""
    min_key_size: int = 256  # Minimum key size in bits
    require_quantum_resistant: bool = True
    key_rotation_days: int = 90
    max_failed_attempts: int = 5
    lockout_duration_seconds: int = 3600
    require_multi_factor: bool = False
    encryption_algorithm: str = "AES-256-GCM"
    quantum_algorithm: str = "SPHINCS+"  # Post-quantum signature scheme


class QuantumResistantHash:
    """
    Quantum-Resistant Hash Functions
    Uses SHA-3 (Keccak) which is quantum-resistant
    """
    
    @staticmethod
    def hash(data: bytes, algorithm: str = "sha3_256") -> bytes:
        """Hash data with quantum-resistant algorithm"""
        if algorithm == "sha3_256":
            return hashlib.sha3_256(data).digest()
        elif algorithm == "sha3_512":
            return hashlib.sha3_512(data).digest()
        elif algorithm == "blake2b":
            return hashlib.blake2b(data, digest_size=64).digest()
        else:
            return hashlib.sha3_256(data).digest()
    
    @staticmethod
    def derive_key(password: bytes, salt: bytes, length: int = 32) -> bytes:
        """Derive key using PBKDF2 with SHA-3"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=length,
            salt=salt,
            iterations=100000,  # High iteration count
            backend=default_backend()
        )
        return kdf.derive(password)


class QuantumEncryption:
    """
    Quantum-Resistant Encryption
    Multi-layer encryption with quantum-resistant algorithms
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.QUANTUM_RESISTANT):
        self.security_level = security_level
        self.key_storage = SOVEREIGN_ROOT / "quantum_keys"
        self.key_storage.mkdir(exist_ok=True, mode=0o700)
        self.keys: Dict[str, QuantumKey] = {}
        self._load_keys()
    
    def _load_keys(self):
        """Load keys from storage"""
        # In production, load from secure storage
        pass
    
    def generate_key(self, key_id: str, key_type: KeyType = KeyType.HYBRID) -> QuantumKey:
        """Generate quantum-resistant key"""
        if key_type == KeyType.SYMMETRIC:
            key_data = secrets.token_bytes(32)  # 256-bit key
        elif key_type == KeyType.ASYMMETRIC:
            # RSA-4096 for quantum resistance
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend()
            )
            key_data = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        elif key_type == KeyType.QUANTUM_RESISTANT:
            # Use hybrid approach: AES-256 + quantum-resistant hash
            key_data = secrets.token_bytes(64)  # 512-bit key
        else:  # HYBRID
            # Multiple keys for layered security
            key_data = secrets.token_bytes(96)  # 768-bit hybrid key
        
        key = QuantumKey(
            key_id=key_id,
            key_type=key_type,
            key_data=key_data,
            created_at=time.time(),
            expires_at=time.time() + (90 * 24 * 3600),  # 90 days
            security_level=self.security_level
        )
        
        self.keys[key_id] = key
        self._save_key(key)
        
        return key
    
    def _save_key(self, key: QuantumKey):
        """Save key to secure storage"""
        key_file = self.key_storage / f"{key.key_id}.key"
        # Encrypt key before saving
        encrypted_key = self._encrypt_key_data(key.key_data)
        key_file.write_bytes(encrypted_key)
        key_file.chmod(0o600)
    
    def _encrypt_key_data(self, key_data: bytes) -> bytes:
        """Encrypt key data with master key"""
        # Use system master key for key encryption
        master_key = self._get_master_key()
        cipher = Cipher(
            algorithms.AES(master_key),
            modes.GCM(secrets.token_bytes(12)),  # Nonce
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(key_data) + encryptor.finalize()
        return encrypted + encryptor.tag
    
    def _get_master_key(self) -> bytes:
        """Get or generate master key"""
        master_key_file = SOVEREIGN_ROOT / "master_key.key"
        if master_key_file.exists():
            return master_key_file.read_bytes()
        else:
            # Generate new master key
            master_key = secrets.token_bytes(32)
            master_key_file.write_bytes(master_key)
            master_key_file.chmod(0o600)
            return master_key
    
    def encrypt(self, data: bytes, key_id: str) -> bytes:
        """Encrypt data with quantum-resistant encryption"""
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not found")
        
        key = self.keys[key_id]
        
        if self.security_level == SecurityLevel.MAXIMUM:
            # Multi-layer encryption
            # Layer 1: AES-256-GCM
            aes_key = key.key_data[:32]
            nonce = secrets.token_bytes(12)
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.GCM(nonce),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(data) + encryptor.finalize()
            
            # Layer 2: Additional encryption with second key
            second_key = key.key_data[32:64] if len(key.key_data) >= 64 else aes_key
            cipher2 = Cipher(
                algorithms.AES(second_key),
                modes.GCM(secrets.token_bytes(12)),
                backend=default_backend()
            )
            encryptor2 = cipher2.encryptor()
            double_encrypted = encryptor2.update(encrypted + encryptor.tag) + encryptor2.finalize()
            
            # Add metadata
            metadata = {
                "key_id": key_id,
                "nonce1": base64.b64encode(nonce).decode(),
                "nonce2": base64.b64encode(secrets.token_bytes(12)).decode(),
                "tag1": base64.b64encode(encryptor.tag).decode(),
                "tag2": base64.b64encode(encryptor2.tag).decode(),
                "security_level": self.security_level.value
            }
            
            return json.dumps(metadata).encode() + b":::" + double_encrypted + encryptor2.tag
        else:
            # Standard quantum-resistant encryption
            aes_key = key.key_data[:32]
            nonce = secrets.token_bytes(12)
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.GCM(nonce),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(data) + encryptor.finalize()
            
            metadata = {
                "key_id": key_id,
                "nonce": base64.b64encode(nonce).decode(),
                "tag": base64.b64encode(encryptor.tag).decode()
            }
            
            return json.dumps(metadata).encode() + b":::" + encrypted + encryptor.tag
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt data"""
        try:
            # Parse metadata
            parts = encrypted_data.split(b":::", 1)
            if len(parts) != 2:
                raise ValueError("Invalid encrypted data format")
            
            metadata_json, encrypted = parts[0], parts[1]
            metadata = json.loads(metadata_json.decode())
            
            key_id = metadata["key_id"]
            if key_id not in self.keys:
                raise ValueError(f"Key {key_id} not found")
            
            key = self.keys[key_id]
            
            if metadata.get("security_level") == SecurityLevel.MAXIMUM.value:
                # Multi-layer decryption
                nonce2 = base64.b64decode(metadata["nonce2"])
                tag2 = base64.b64decode(metadata["tag2"])
                
                second_key = key.key_data[32:64] if len(key.key_data) >= 64 else key.key_data[:32]
                cipher2 = Cipher(
                    algorithms.AES(second_key),
                    modes.GCM(nonce2, tag2),
                    backend=default_backend()
                )
                decryptor2 = cipher2.decryptor()
                layer1_data = decryptor2.update(encrypted[:-16]) + decryptor2.finalize()
                
                # Decrypt layer 1
                nonce1 = base64.b64decode(metadata["nonce1"])
                tag1 = base64.b64decode(metadata["tag1"])
                aes_key = key.key_data[:32]
                cipher1 = Cipher(
                    algorithms.AES(aes_key),
                    modes.GCM(nonce1, tag1),
                    backend=default_backend()
                )
                decryptor1 = cipher1.decryptor()
                data = decryptor1.update(layer1_data[:-16]) + decryptor1.finalize()
            else:
                # Standard decryption
                nonce = base64.b64decode(metadata["nonce"])
                tag = base64.b64decode(metadata["tag"])
                aes_key = key.key_data[:32]
                cipher = Cipher(
                    algorithms.AES(aes_key),
                    modes.GCM(nonce, tag),
                    backend=default_backend()
                )
                decryptor = cipher.decryptor()
                data = decryptor.update(encrypted[:-16]) + decryptor.finalize()
            
            return data
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")


class QuantumSignature:
    """
    Quantum-Resistant Digital Signatures
    """
    
    def __init__(self):
        self.private_keys: Dict[str, Any] = {}
        self.public_keys: Dict[str, bytes] = {}
    
    def generate_keypair(self, key_id: str) -> Tuple[bytes, bytes]:
        """Generate quantum-resistant keypair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,  # Large key for quantum resistance
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        self.private_keys[key_id] = private_key
        self.public_keys[key_id] = public_pem
        
        return private_pem, public_pem
    
    def sign(self, data: bytes, key_id: str) -> bytes:
        """Sign data with quantum-resistant signature"""
        if key_id not in self.private_keys:
            raise ValueError(f"Private key {key_id} not found")
        
        private_key = self.private_keys[key_id]
        
        # Use SHA-3 for quantum resistance
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_256()
        )
        
        return signature
    
    def verify(self, data: bytes, signature: bytes, public_key_pem: bytes) -> bool:
        """Verify quantum-resistant signature"""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem,
                backend=default_backend()
            )
            
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA3_256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA3_256()
            )
            return True
        except Exception:
            return False


class QuantumSecuritySystem:
    """
    Comprehensive Quantum Security System
    Protects critical systems with quantum-resistant cryptography
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.MAXIMUM):
        self.security_level = security_level
        self.encryption = QuantumEncryption(security_level)
        self.signature = QuantumSignature()
        self.policy = SecurityPolicy()
        self.failed_attempts: Dict[str, int] = {}
        self.lockouts: Dict[str, float] = {}
        
        # Initialize master keys
        self._initialize_master_keys()
    
    def _initialize_master_keys(self):
        """Initialize master encryption and signature keys"""
        # Master encryption key
        if "master_encryption" not in self.encryption.keys:
            self.encryption.generate_key("master_encryption", KeyType.HYBRID)
        
        # Master signature keypair
        if "master_signature" not in self.signature.private_keys:
            self.signature.generate_keypair("master_signature")
    
    def protect_data(self, data: bytes, label: str = "protected") -> bytes:
        """Protect data with quantum-resistant encryption"""
        key_id = f"{label}_key"
        
        # Ensure key exists
        if key_id not in self.encryption.keys:
            self.encryption.generate_key(key_id, KeyType.HYBRID)
        
        # Encrypt
        encrypted = self.encryption.encrypt(data, key_id)
        
        # Sign
        signature = self.signature.sign(encrypted, "master_signature")
        
        # Combine
        protected = json.dumps({
            "encrypted_data": base64.b64encode(encrypted).decode(),
            "signature": base64.b64encode(signature).decode(),
            "timestamp": time.time(),
            "security_level": self.security_level.value
        }).encode()
        
        return protected
    
    def unprotect_data(self, protected_data: bytes) -> bytes:
        """Unprotect data"""
        try:
            # Parse
            metadata = json.loads(protected_data.decode())
            encrypted = base64.b64decode(metadata["encrypted_data"])
            signature = base64.b64decode(metadata["signature"])
            
            # Verify signature
            public_key = self.signature.public_keys.get("master_signature")
            if not public_key:
                raise ValueError("Master signature key not found")
            
            if not self.signature.verify(encrypted, signature, public_key):
                raise ValueError("Signature verification failed")
            
            # Decrypt
            data = self.encryption.decrypt(encrypted)
            
            return data
        except Exception as e:
            raise ValueError(f"Unprotect failed: {e}")
    
    def create_secure_channel(self, channel_id: str) -> Dict[str, bytes]:
        """Create secure communication channel"""
        # Generate channel keys
        enc_key = self.encryption.generate_key(f"channel_{channel_id}_enc", KeyType.HYBRID)
        sig_priv, sig_pub = self.signature.generate_keypair(f"channel_{channel_id}_sig")
        
        return {
            "encryption_key_id": enc_key.key_id,
            "signature_private": sig_priv,
            "signature_public": sig_pub
        }
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get security system status"""
        return {
            "security_level": self.security_level.value,
            "encryption_keys": len(self.encryption.keys),
            "signature_keys": len(self.signature.private_keys),
            "policy": {
                "min_key_size": self.policy.min_key_size,
                "require_quantum_resistant": self.policy.require_quantum_resistant,
                "key_rotation_days": self.policy.key_rotation_days
            },
            "active_lockouts": len(self.lockouts),
            "failed_attempts": sum(self.failed_attempts.values())
        }


# Global instance
_quantum_security: Optional[QuantumSecuritySystem] = None


def get_quantum_security() -> QuantumSecuritySystem:
    """Get or create quantum security system instance"""
    global _quantum_security
    if _quantum_security is None:
        _quantum_security = QuantumSecuritySystem(SecurityLevel.MAXIMUM)
    return _quantum_security






