import json
from datetime import datetime
from typing import List, Optional

import Block as Block
import SPEITransaction as SPEITransaction

class SPEIBlockchain:
    """Clase principal que maneja la blockchain SPEI"""

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[dict] = []
        self.difficulty = 3  # Dificultad de minado
        self.banks_db = self.load_banks_database()

        # Crear bloque génesis
        self.create_genesis_block()

        print(" Blockchain SPEI inicializada")
        print(f" Bancos registrados: {len(self.banks_db)}")
        print(f"️  Dificultad de minado: {self.difficulty}")

    @staticmethod
    def load_banks_database() -> dict:
        """Carga la base de datos de bancos mexicanos"""
        return {
            "002": "Banco Nacional de México (BANAMEX)",
            "012": "BBVA México",
            "014": "Banco Santander México",
            "021": "HSBC México",
            "030": "Banco Bajío",
            "036": "Banco Inbursa",
            "037": "Banco Interacciones",
            "042": "Banco Mifel",
            "058": "Banco Regional de Monterrey (Banregio)",
            "072": "Banco Autofin México",
            "103": "American Express Bank México",
            "106": "Bank of America México",
            "108": "Bank of Tokyo-Mitsubishi UFJ México",
            "110": "JP Morgan Chase Bank México",
            "112": "Banco Multiva",
            "127": "Banco Azteca",
            "128": "Banco Coppel",
            "129": "Banco Compartamos",
            "132": "Banco Actinver",
            "133": "Banco Ahorro Famsa",
            "135": "Afirme",
            "136": "Intercam Banco",
            "137": "Bancoppel",
            "138": "ABC Capital",
            "139": "Banco Fácil",
            "140": "Consubanco"
        }

    def create_genesis_block(self):
        """Crea el bloque génesis (primer bloque de la cadena)"""
        genesis_block = Block.Block(0, [], "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

        print("\n Bloque génesis creado")
        print(f" Hash génesis: {genesis_block.hash}")

    def get_bank_name(self, clabe: str) -> str:
        """Obtiene el nombre del banco a partir de la CLABE"""
        if len(clabe) >= 3:
            bank_code = clabe[:3]
            return self.banks_db.get(bank_code, f"Banco desconocido ({bank_code})")
        return "Código de banco inválido"

    def validate_clabe(self, clabe: str) -> bool:
        """Valida formato de CLABE (18 dígitos)"""
        if len(clabe) != 18:
            return False
        if not clabe.isdigit():
            return False

        # Validar código de banco
        bank_code = clabe[:3]
        if bank_code not in self.banks_db:
            return False

        # Validar dígito verificador (algoritmo simplificado para demo)
        return True

    def validate_transaction(self, transaction: SPEITransaction) -> tuple[bool, str]:
        """Válida una transacción SPEI"""
        # Validar CLABE origen
        if not self.validate_clabe(transaction.sender_clabe):
            return False, "CLABE de origen inválida"

        # Validar CLABE destino
        if not self.validate_clabe(transaction.receiver_clabe):
            return False, "CLABE de destino inválida"

        # Validar monto
        if transaction.amount <= 0:
            return False, "El monto debe ser mayor a 0"

        if transaction.amount > 999999.99:  # Límite SPEI por operación
            return False, "El monto excede el límite máximo de SPEI"

        # Validar referencia
        if len(transaction.reference) == 0:
            return False, "La referencia es obligatoria"

        if len(transaction.reference) > 40:
            return False, "La referencia no puede exceder 40 caracteres"

        # No permitir transferencias a la misma cuenta
        if transaction.sender_clabe == transaction.receiver_clabe:
            return False, "No se puede transferir a la misma cuenta"

        return True, "Transacción válida"

    def add_transaction(self, transaction: SPEITransaction) -> tuple[bool, str]:
        """Agrega una transacción al pool de transacciones pendientes"""
        is_valid, message = self.validate_transaction(transaction)

        if is_valid:
            transaction.status = "validated"
            self.pending_transactions.append(transaction.to_dict())

            print(f"\n Nueva transacción agregada:")
            print(f"    ID: {transaction.id}")
            print(f"    Rastreo: {transaction.tracking_number}")
            print(f"    Origen: {self.get_bank_name(transaction.sender_clabe)}")
            print(f"    Destino: {self.get_bank_name(transaction.receiver_clabe)}")
            print(f"    Monto: ${transaction.amount:,.2f}")
            print(f"    Referencia: {transaction.reference}")

            return True, f"Transacción {transaction.id} agregada al pool"
        else:
            print(f"\n Transacción rechazada: {message}")
            return False, message

    def mine_pending_transactions(self) -> Optional[Block]:
        """Mina un nuevo bloque con las transacciones pendientes"""
        if len(self.pending_transactions) == 0:
            print("\n  No hay transacciones pendientes para minar")
            return None

        # Marcar transacciones como procesándose
        for tx in self.pending_transactions:
            tx['status'] = 'processing'

        # Crear nuevo bloque
        new_block = Block.Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.chain[-1].hash
        )

        # Minar el bloque
        new_block.mine_block(self.difficulty)

        # Agregar bloque a la cadena
        self.chain.append(new_block)

        # Marcar transacciones como confirmadas
        for tx in new_block.transactions:
            tx['status'] = 'confirmed'

        # Limpiar pool de transacciones pendientes
        self.pending_transactions = []

        print(f"\n Bloque #{new_block.index} agregado exitosamente a la blockchain")
        print(f" Transacciones confirmadas: {len(new_block.transactions)}")
        print(f" Longitud de cadena: {len(self.chain)} bloques")

        return new_block

    def is_chain_valid(self) -> bool:
        """Valida la integridad de toda la blockchain"""
        print(f"\n Validando integridad de la blockchain...")

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verificar que el hash del bloque sea correcto
            if current_block.hash != current_block.calculate_hash():
                print(f" Hash inválido en bloque #{i}")
                return False

            # Verificar que el enlace con el bloque anterior sea correcto
            if current_block.previous_hash != previous_block.hash:
                print(f" Enlace roto entre bloque #{i - 1} y #{i}")
                return False

            # Verificar que el hash cumpla la dificultad
            if not current_block.hash.startswith("0" * self.difficulty):
                print(f" Bloque #{i} no cumple la dificultad requerida")
                return False

        print(f" Blockchain válida - {len(self.chain)} bloques verificados")
        return True

    def get_transaction_by_tracking(self, tracking_number: str) -> Optional[dict]:
        """Busca una transacción por su número de rastreo"""
        for block_index, block in enumerate(self.chain):
            for tx in block.transactions:
                if tx.get('tracking_number') == tracking_number:
                    confirmations = len(self.chain) - block.index
                    return {
                        'transaction': tx,
                        'block_number': block.index,
                        'block_hash': block.hash,
                        'confirmations': confirmations,
                        'found_in_block': block_index
                    }
        return None

    def get_account_history(self, clabe: str) -> List[dict]:
        """Obtiene el historial de transacciones de una cuenta"""
        transactions = []

        for block in self.chain:
            for tx in block.transactions:
                if (tx.get('sender_clabe') == clabe or
                        tx.get('receiver_clabe') == clabe):
                    # Determinar tipo de transacción
                    tx_type = "sent" if tx.get('sender_clabe') == clabe else "received"

                    transactions.append({
                        'transaction': tx,
                        'type': tx_type,
                        'block_number': block.index,
                        'block_hash': block.hash,
                        'confirmations': len(self.chain) - block.index
                    })

        # Ordenar por fecha (más reciente primero)
        transactions.sort(key=lambda x: x['transaction']['timestamp'], reverse=True)
        return transactions

    def get_blockchain_stats(self) -> dict:
        """Obtiene estadísticas de la blockchain"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_volume = 0

        for block in self.chain:
            for tx in block.transactions:
                total_volume += tx.get('amount', 0)

        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'pending_transactions': len(self.pending_transactions),
            'total_volume': total_volume,
            'average_transactions_per_block': total_transactions / max(1, len(self.chain) - 1),
            'difficulty': self.difficulty,
            'is_valid': self.is_chain_valid()
        }

    def print_blockchain_summary(self):
        """Imprime un resumen completo de la blockchain"""
        print(f"\n{'=' * 60}")
        print(f" RESUMEN DE BLOCKCHAIN SPEI")
        print(f"{'=' * 60}")

        stats = self.get_blockchain_stats()

        print(f" Total de bloques: {stats['total_blocks']}")
        print(f" Total de transacciones: {stats['total_transactions']}")
        print(f" Transacciones pendientes: {stats['pending_transactions']}")
        print(f" Volumen total: ${stats['total_volume']:,.2f}")
        print(f" Promedio tx/bloque: {stats['average_transactions_per_block']:.1f}")
        print(f"️  Dificultad actual: {stats['difficulty']}")
        print(f" Blockchain válida: {'Sí' if stats['is_valid'] else 'No'}")

        print(f"\n DETALLES POR BLOQUE:")
        print(f"{'Bloque':<8} {'Hash':<20} {'Tx':<5} {'Timestamp':<20}")
        print(f"{'-' * 60}")

        for block in self.chain:
            timestamp = block.timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(block, 'timestamp') else "N/A"
            print(f"#{block.index:<7} {block.hash[:18]:<18}.. {len(block.transactions):<5} {timestamp}")

    def save_to_file(self, filename: str = "blockchain_spei.json"):
        """Guarda la blockchain en un archivo JSON"""
        blockchain_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'difficulty': self.difficulty,
                'total_blocks': len(self.chain),
                'total_transactions': sum(len(block.transactions) for block in self.chain)
            },
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': self.pending_transactions
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(blockchain_data, f, indent=2, ensure_ascii=False)
            print(f"\n Blockchain guardada en: {filename}")
        except Exception as e:
            print(f"\n Error al guardar blockchain: {e}")
