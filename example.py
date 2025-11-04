#!/usr/bin/env python3
"""
Dark Bank Example - Demonstrates complete usage of the Dark Bank system

This example shows:
1. Account creation with and without initial deposits
2. Deposit operations
3. Withdrawal operations
4. Transfer between accounts
5. Transaction history tracking
6. System statistics
7. State persistence
"""

from dark_bank import DarkBank


def print_separator(title=""):
    """Print a separator line"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")
    else:
        print("-" * 60)


def main():
    """Run complete Dark Bank example"""
    
    print_separator("DARK BANK EXAMPLE - Complete Workflow")
    
    # Initialize Dark Bank
    bank = DarkBank()
    print("Initialized Dark Bank")
    print(f"Total WBTC Supply: {bank.TOTAL_SUPPLY:,}")
    
    # Step 1: Create accounts
    print_separator("Step 1: Creating Accounts")
    
    alice = bank.create_account(initial_deposit=10000.0)
    print(f"✓ Created account for Alice")
    print(f"  Account ID: {alice[:32]}...")
    print(f"  Balance: {bank.get_balance(alice):,} WBTC")
    
    bob = bank.create_account(initial_deposit=5000.0)
    print(f"\n✓ Created account for Bob")
    print(f"  Account ID: {bob[:32]}...")
    print(f"  Balance: {bank.get_balance(bob):,} WBTC")
    
    charlie = bank.create_account()
    print(f"\n✓ Created account for Charlie (no initial deposit)")
    print(f"  Account ID: {charlie[:32]}...")
    print(f"  Balance: {bank.get_balance(charlie):,} WBTC")
    
    # Step 2: Deposits
    print_separator("Step 2: Depositing Funds")
    
    tx_id = bank.deposit(charlie, 2500.0)
    print(f"✓ Deposited 2,500 WBTC to Charlie's account")
    print(f"  Transaction ID: {tx_id[:32]}...")
    print(f"  New Balance: {bank.get_balance(charlie):,} WBTC")
    
    # Step 3: Transfers
    print_separator("Step 3: Transferring Funds")
    
    tx_id = bank.transfer(alice, bob, 1500.0)
    print(f"✓ Alice → Bob: 1,500 WBTC")
    print(f"  Transaction ID: {tx_id[:32]}...")
    print(f"  Alice's Balance: {bank.get_balance(alice):,} WBTC")
    print(f"  Bob's Balance: {bank.get_balance(bob):,} WBTC")
    
    tx_id = bank.transfer(bob, charlie, 1000.0)
    print(f"\n✓ Bob → Charlie: 1,000 WBTC")
    print(f"  Transaction ID: {tx_id[:32]}...")
    print(f"  Bob's Balance: {bank.get_balance(bob):,} WBTC")
    print(f"  Charlie's Balance: {bank.get_balance(charlie):,} WBTC")
    
    tx_id = bank.transfer(charlie, alice, 500.0)
    print(f"\n✓ Charlie → Alice: 500 WBTC")
    print(f"  Transaction ID: {tx_id[:32]}...")
    print(f"  Charlie's Balance: {bank.get_balance(charlie):,} WBTC")
    print(f"  Alice's Balance: {bank.get_balance(alice):,} WBTC")
    
    # Step 4: Withdrawal
    print_separator("Step 4: Withdrawing Funds")
    
    tx_id = bank.withdraw(alice, 1000.0)
    print(f"✓ Alice withdrew 1,000 WBTC")
    print(f"  Transaction ID: {tx_id[:32]}...")
    print(f"  New Balance: {bank.get_balance(alice):,} WBTC")
    
    # Step 5: Transaction History
    print_separator("Step 5: Transaction History")
    
    print("Alice's Recent Transactions:")
    history = bank.get_transaction_history(alice, limit=5)
    for i, tx in enumerate(history, 1):
        direction = "Received" if tx['to_account'] == alice else "Sent"
        amount_sign = "+" if direction == "Received" else "-"
        print(f"  {i}. {direction}: {amount_sign}{tx['amount']:,} WBTC")
        print(f"     TX: {tx['tx_id'][:32]}...")
    
    print("\nBob's Recent Transactions:")
    history = bank.get_transaction_history(bob, limit=5)
    for i, tx in enumerate(history, 1):
        direction = "Received" if tx['to_account'] == bob else "Sent"
        amount_sign = "+" if direction == "Received" else "-"
        print(f"  {i}. {direction}: {amount_sign}{tx['amount']:,} WBTC")
        print(f"     TX: {tx['tx_id'][:32]}...")
    
    # Step 6: System Statistics
    print_separator("Step 6: System Statistics")
    
    stats = bank.get_system_stats()
    print(f"Total Accounts: {stats['total_accounts']}")
    print(f"Total Transactions: {stats['total_transactions']}")
    print(f"Total Deposited: {stats['total_deposited']:,} WBTC")
    print(f"Total Supply: {stats['total_supply']:,} WBTC")
    print(f"Remaining Supply: {stats['remaining_supply']:,} WBTC")
    print(f"Utilization: {(stats['total_deposited'] / stats['total_supply'] * 100):.6f}%")
    
    # Step 7: Account Balances Summary
    print_separator("Step 7: Final Account Balances")
    
    print(f"Alice:   {bank.get_balance(alice):,} WBTC")
    print(f"Bob:     {bank.get_balance(bob):,} WBTC")
    print(f"Charlie: {bank.get_balance(charlie):,} WBTC")
    total_balance = (bank.get_balance(alice) + 
                     bank.get_balance(bob) + 
                     bank.get_balance(charlie))
    print(f"\nTotal in accounts: {total_balance:,} WBTC")
    
    # Step 8: State Persistence
    print_separator("Step 8: State Persistence")
    
    state_file = "/tmp/dark_bank_example.json"
    bank.save_state(state_file)
    print(f"✓ Saved state to: {state_file}")
    
    # Load state to verify
    new_bank = DarkBank()
    new_bank.load_state(state_file)
    print(f"✓ Loaded state from: {state_file}")
    
    # Verify state was preserved
    print(f"\nVerification:")
    print(f"  Accounts preserved: {new_bank.get_total_accounts()}")
    print(f"  Transactions preserved: {new_bank.get_total_transactions()}")
    print(f"  Alice's balance preserved: {new_bank.get_balance(alice):,} WBTC")
    
    # Cleanup
    import os
    if os.path.exists(state_file):
        os.remove(state_file)
        print(f"✓ Cleaned up example state file")
    
    print_separator("Example Complete")
    print("Dark Bank demonstration finished successfully!")
    print("All operations completed without errors.\n")


if __name__ == "__main__":
    main()
