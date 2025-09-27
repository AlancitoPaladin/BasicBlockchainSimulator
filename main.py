import time

import SPEITransaction as SPEITransaction
import SPEIBlockchain as SPEIBlockchain


def demo_spei_blockchain():
    """Función de demostración del sistema blockchain SPEI"""
    print(" Iniciando demostración del sistema Blockchain-SPEI")
    print("=" * 70)

    # Crear blockchain
    blockchain = SPEIBlockchain.SPEIBlockchain()

    # Transacciones de prueba
    test_transactions = [
        {
            'sender': "012180001234567890",  # BBVA
            'receiver': "002010098765432109",  # BANAMEX
            'amount': 1500.00,
            'reference': "Pago de servicios profesionales"
        },
        {
            'sender': "002010098765432109",  # BANAMEX
            'receiver': "014027015555555555",  # Santander
            'amount': 750.50,
            'reference': "Transferencia familiar"
        },
        {
            'sender': "021180001111111118",  # HSBC
            'receiver': "036180002222222229",  # Inbursa
            'amount': 2250.75,
            'reference': "Pago de renta departamento"
        },
        {
            'sender': "014027015555555555",  # Santander
            'receiver': "127180003333333330",  # Azteca
            'amount': 500.00,
            'reference': "Ahorro mensual"
        },
        {
            'sender': "127180003333333330",  # Azteca
            'receiver': "012180001234567890",  # BBVA
            'amount': 1200.25,
            'reference': "Pago de tarjeta de crédito"
        }
    ]

    print(f"\n Creando {len(test_transactions)} transacciones de prueba...")

    # Agregar transacciones
    successful_transactions = []
    for i, tx_data in enumerate(test_transactions, 1):
        print(f"\n--- Transacción {i} ---")

        transaction = SPEITransaction.SPEITransaction(
            sender_clabe=tx_data['sender'],
            receiver_clabe=tx_data['receiver'],
            amount=tx_data['amount'],
            reference=tx_data['reference']
        )

        success, message = blockchain.add_transaction(transaction)
        if success:
            successful_transactions.append(transaction)

        time.sleep(0.5)  # Pausa para mejor visualización

    # Minar primer bloque
    print(f"\n{'=' * 50}")
    print("🔨 INICIANDO PROCESO DE MINADO")
    print(f"{'=' * 50}")

    block1 = blockchain.mine_pending_transactions()

    # Agregar más transacciones para un segundo bloque
    print(f"\n Agregando transacciones para segundo bloque...")

    additional_transactions = [
        {
            'sender': "036180002222222229",  # Inbursa
            'receiver': "021180001111111118",  # HSBC
            'amount': 3500.00,
            'reference': "Inversión en acciones"
        },
        {
            'sender': "002010098765432109",  # BANAMEX
            'receiver': "014027015555555555",  # Santander
            'amount': 825.30,
            'reference': "Compra de materiales"
        }
    ]

    for tx_data in additional_transactions:
        transaction = SPEITransaction.SPEITransaction(
            sender_clabe=tx_data['sender'],
            receiver_clabe=tx_data['receiver'],
            amount=tx_data['amount'],
            reference=tx_data['reference']
        )
        blockchain.add_transaction(transaction)

    # Minar segundo bloque
    block2 = blockchain.mine_pending_transactions()

    # Validar blockchain
    print(f"\n{'=' * 50}")
    print(" VALIDANDO BLOCKCHAIN")
    print(f"{'=' * 50}")

    blockchain.is_chain_valid()

    # Mostrar estadísticas
    blockchain.print_blockchain_summary()

    # Demostrar búsquedas
    print(f"\n{'=' * 50}")
    print(" DEMOSTRANDO FUNCIONES DE BÚSQUEDA")
    print(f"{'=' * 50}")

    if successful_transactions:
        # Buscar por número de rastreo
        first_tx = successful_transactions[0]
        print(f"\n Buscando transacción por número de rastreo: {first_tx.tracking_number}")

        result = blockchain.get_transaction_by_tracking(first_tx.tracking_number)
        if result:
            tx = result['transaction']
            print(f" Transacción encontrada:")
            print(f"    Monto: ${tx['amount']:,.2f}")
            print(f"    De: {blockchain.get_bank_name(tx['sender_clabe'])}")
            print(f"    A: {blockchain.get_bank_name(tx['receiver_clabe'])}")
            print(f"    Bloque: #{result['block_number']}")
            print(f"    Confirmaciones: {result['confirmations']}")

        # Historial de cuenta
        test_clabe = successful_transactions[0].sender_clabe
        print(f"\n Historial de cuenta: {test_clabe}")
        print(f"    ({blockchain.get_bank_name(test_clabe)})")

        history = blockchain.get_account_history(test_clabe)
        for i, record in enumerate(history[:3], 1):  # Mostrar solo las primeras 3
            tx = record['transaction']
            direction = "➡️  Enviado" if record['type'] == 'sent' else "⬅️  Recibido"
            counterpart = tx['receiver_clabe'] if record['type'] == 'sent' else tx['sender_clabe']

            print(f"   {i}. {direction} - ${tx['amount']:,.2f}")
            print(f"      Contraparte: {blockchain.get_bank_name(counterpart)}")
            print(f"      Ref: {tx['reference']}")
            print(f"      Bloque: #{record['block_number']}")

    # Guardar blockchain
    print(f"\n Guardando blockchain en archivo...")
    blockchain.save_to_file("demo_blockchain_spei.json")

    print(f"\n¡Demostración completada exitosamente!")
    print(f"{'=' * 70}")

    return blockchain


if __name__ == "__main__":
    # Ejecutar demostración
    blockchain = demo_spei_blockchain()

    # Menú interactivo opcional
    print(f"\n🔧 ¿Deseas ejecutar comandos adicionales? (s/n): ", end="")
    if input().lower().startswith('s'):
        while True:
            print(f"\n{'=' * 50}")
            print("COMANDOS DISPONIBLES:")
            print("1. Crear nueva transacción")
            print("2. Minar transacciones pendientes")
            print("3. Validar blockchain")
            print("4. Ver estadísticas")
            print("5. Buscar transacción")
            print("6. Ver historial de cuenta")
            print("7. Salir")
            print(f"{'=' * 50}")

            choice = input("Selecciona una opción (1-7): ")

            if choice == '1':
                sender = input("CLABE origen (18 dígitos): ")
                receiver = input("CLABE destino (18 dígitos): ")
                try:
                    amount = float(input("Monto: $"))
                    reference = input("Referencia: ")

                    tx = SPEITransaction.SPEITransaction(sender, receiver, amount, reference)
                    blockchain.add_transaction(tx)
                except ValueError:
                    print(" Monto inválido")

            elif choice == '2':
                blockchain.mine_pending_transactions()

            elif choice == '3':
                blockchain.is_chain_valid()

            elif choice == '4':
                blockchain.print_blockchain_summary()

            elif choice == '5':
                tracking = input("Número de rastreo: ")
                result = blockchain.get_transaction_by_tracking(tracking)
                if result:
                    tx = result['transaction']
                    print(f" Transacción encontrada en bloque #{result['block_number']}")
                    print(f" ${tx['amount']:,.2f} - {tx['reference']}")
                else:
                    print(" Transacción no encontrada")

            elif choice == '6':
                clabe = input("CLABE a consultar: ")
                history = blockchain.get_account_history(clabe)
                if history:
                    print(f" Historial ({len(history)} transacciones):")
                    for record in history[:5]:
                        tx = record['transaction']
                        direction = "️ " if record['type'] == 'sent' else " "
                        print(f"{direction}${tx['amount']:,.2f} - {tx['reference']}")
                else:
                    print(" No se encontraron transacciones")

            elif choice == '7':
                print("¡Hasta luego!")
                break

            else:
                print(" Opción inválida")
