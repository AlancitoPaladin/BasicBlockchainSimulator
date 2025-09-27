import datetime
import random
import string
import uuid


class SPEITransaction:
    """Clase que representa una transacción SPEI"""

    def __init__(self, sender_clabe: str, receiver_clabe: str, amount: float, reference: str):
        self.id = self.generate_spei_id()
        self.sender_clabe = sender_clabe
        self.receiver_clabe = receiver_clabe
        self.amount = amount
        self.reference = reference
        self.tracking_number = self.generate_tracking()
        self.timestamp = datetime.datetime.now()
        self.status = "pending"

    def generate_spei_id(self) -> str:
        """Genera un ID único para la transacción"""
        return str(uuid.uuid4())[:8].upper()

    def generate_tracking(self) -> str:
        """Genera número de rastreo como SPEI real (30 caracteres)"""
        return ''.join(random.choices(string.digits, k=30))

    def to_dict(self) -> dict:
        """Convierte la transacción a diccionario"""
        return {
            'id': self.id,
            'sender_clabe': self.sender_clabe,
            'receiver_clabe': self.receiver_clabe,
            'amount': self.amount,
            'reference': self.reference,
            'tracking_number': self.tracking_number,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }

    def __str__(self):
        return f"SPEI {self.id}: {self.sender_clabe} → {self.receiver_clabe} ${self.amount:,.2f}"
