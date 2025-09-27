from datetime import datetime
import hashlib
import json
import time
from typing import List


class Block:
    """Clase que representa un bloque en la blockchain"""

    def __init__(self, index: int, transactions: List[dict], previous_hash: str):
        self.index = index
        self.timestamp = datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calcula el hash SHA-256 del bloque"""
        block_string = (
            f"{self.index}"
            f"{self.timestamp.isoformat()}"
            f"{json.dumps(self.transactions, sort_keys=True)}"
            f"{self.previous_hash}"
            f"{self.nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        """Mina el bloque hasta encontrar un hash que cumpla la dificultad"""
        target = "0" * difficulty
        start_time = time.time()

        print(f"\n🔨 Minando bloque #{self.index}...")
        print(f" Transacciones en bloque: {len(self.transactions)}")
        print(f" Dificultad: {difficulty} (debe empezar con {'0' * difficulty})")

        attempts = 0
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            attempts += 1

            # Mostrar progreso cada 50000 intentos
            if attempts % 50000 == 0:
                elapsed = time.time() - start_time
                print(f"️  Intentos: {attempts:,} | Tiempo: {elapsed:.1f}s | Hash: {self.hash[:20]}...")

        mining_time = time.time() - start_time
        hash_rate = attempts / mining_time if mining_time > 0 else 0

        print(f" ¡Bloque minado exitosamente!")
        print(f" Nonce ganador: {self.nonce:,}")
        print(f" Hash final: {self.hash}")
        print(f" Tiempo de minado: {mining_time:.2f} segundos")
        print(f" Tasa de hash: {hash_rate:,.0f} H/s")

    def to_dict(self) -> dict:
        """Convierte el bloque a diccionario"""
        return {
            'index': self.index,
            'timestamp': self.timestamp.isoformat(),
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce
        }
