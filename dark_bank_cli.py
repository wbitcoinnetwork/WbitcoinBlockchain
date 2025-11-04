#!/usr/bin/env python3
"""
Dark Bank CLI - Command-line interface for Dark Bank operations
"""

import sys
import argparse
from dark_bank import DarkBank


def create_account(bank, args):
    """Create a new anonymous account"""
    initial_deposit = args.deposit if args.deposit else 0.0
    
    try:
        account_id = bank.create_account(initial_deposit=initial_deposit)
        print(f"✓ Account created successfully!")
        print(f"  Account ID: {account_id}")
        print(f"  Initial Balance: {initial_deposit:,} WBTC")
        
        if args.save:
            bank.save_state(args.save)
            print(f"  State saved to: {args.save}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def check_balance(bank, args):
    """Check account balance"""
    try:
        balance = bank.get_balance(args.account)
        print(f"Account Balance: {balance:,} WBTC")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def deposit_funds(bank, args):
    """Deposit funds to an account"""
    try:
        tx_id = bank.deposit(args.account, args.amount)
        new_balance = bank.get_balance(args.account)
        
        print(f"✓ Deposit successful!")
        print(f"  Transaction ID: {tx_id}")
        print(f"  Amount: {args.amount:,} WBTC")
        print(f"  New Balance: {new_balance:,} WBTC")
        
        if args.save:
            bank.save_state(args.save)
            print(f"  State saved to: {args.save}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def withdraw_funds(bank, args):
    """Withdraw funds from an account"""
    try:
        tx_id = bank.withdraw(args.account, args.amount)
        new_balance = bank.get_balance(args.account)
        
        print(f"✓ Withdrawal successful!")
        print(f"  Transaction ID: {tx_id}")
        print(f"  Amount: {args.amount:,} WBTC")
        print(f"  New Balance: {new_balance:,} WBTC")
        
        if args.save:
            bank.save_state(args.save)
            print(f"  State saved to: {args.save}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def transfer_funds(bank, args):
    """Transfer funds between accounts"""
    try:
        tx_id = bank.transfer(args.from_account, args.to_account, args.amount)
        from_balance = bank.get_balance(args.from_account)
        to_balance = bank.get_balance(args.to_account)
        
        print(f"✓ Transfer successful!")
        print(f"  Transaction ID: {tx_id}")
        print(f"  Amount: {args.amount:,} WBTC")
        print(f"  From Balance: {from_balance:,} WBTC")
        print(f"  To Balance: {to_balance:,} WBTC")
        
        if args.save:
            bank.save_state(args.save)
            print(f"  State saved to: {args.save}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def show_history(bank, args):
    """Show transaction history"""
    try:
        limit = args.limit if args.limit else 10
        history = bank.get_transaction_history(args.account, limit=limit)
        
        print(f"Transaction History for Account: {args.account[:16]}...")
        print(f"Showing {len(history)} most recent transactions:")
        print("-" * 80)
        
        for i, tx in enumerate(history, 1):
            direction = "←" if tx['to_account'] == args.account else "→"
            counterparty = tx['to_account'] if tx['from_account'] == args.account else tx['from_account']
            
            print(f"{i}. {direction} {tx['amount']:,} WBTC")
            print(f"   TX: {tx['tx_id'][:16]}...")
            print(f"   Counterparty: {counterparty[:16]}...")
            print()
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


def show_stats(bank, args):
    """Show Dark Bank system statistics"""
    stats = bank.get_system_stats()
    
    print("=" * 60)
    print("DARK BANK SYSTEM STATISTICS")
    print("=" * 60)
    print(f"Total Accounts:      {stats['total_accounts']:,}")
    print(f"Total Transactions:  {stats['total_transactions']:,}")
    print(f"Total Deposited:     {stats['total_deposited']:,} WBTC")
    print(f"Total Supply:        {stats['total_supply']:,} WBTC")
    print(f"Remaining Supply:    {stats['remaining_supply']:,} WBTC")
    print(f"Utilization:         {(stats['total_deposited'] / stats['total_supply'] * 100):.6f}%")
    print("=" * 60)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Dark Bank CLI - Privacy-focused banking for Wbitcoin',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--load',
        help='Load bank state from file',
        metavar='FILE'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create account
    create_parser = subparsers.add_parser('create', help='Create a new account')
    create_parser.add_argument('--deposit', type=float, help='Initial deposit amount')
    create_parser.add_argument('--save', help='Save state to file', metavar='FILE')
    
    # Check balance
    balance_parser = subparsers.add_parser('balance', help='Check account balance')
    balance_parser.add_argument('account', help='Account ID')
    
    # Deposit
    deposit_parser = subparsers.add_parser('deposit', help='Deposit funds')
    deposit_parser.add_argument('account', help='Account ID')
    deposit_parser.add_argument('amount', type=float, help='Amount to deposit')
    deposit_parser.add_argument('--save', help='Save state to file', metavar='FILE')
    
    # Withdraw
    withdraw_parser = subparsers.add_parser('withdraw', help='Withdraw funds')
    withdraw_parser.add_argument('account', help='Account ID')
    withdraw_parser.add_argument('amount', type=float, help='Amount to withdraw')
    withdraw_parser.add_argument('--save', help='Save state to file', metavar='FILE')
    
    # Transfer
    transfer_parser = subparsers.add_parser('transfer', help='Transfer funds')
    transfer_parser.add_argument('from_account', help='Source account ID')
    transfer_parser.add_argument('to_account', help='Destination account ID')
    transfer_parser.add_argument('amount', type=float, help='Amount to transfer')
    transfer_parser.add_argument('--save', help='Save state to file', metavar='FILE')
    
    # History
    history_parser = subparsers.add_parser('history', help='Show transaction history')
    history_parser.add_argument('account', help='Account ID')
    history_parser.add_argument('--limit', type=int, help='Number of transactions to show')
    
    # Stats
    stats_parser = subparsers.add_parser('stats', help='Show system statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize bank
    bank = DarkBank()
    
    # Load state if specified
    if args.load:
        try:
            bank.load_state(args.load)
            print(f"✓ Loaded state from: {args.load}\n")
        except Exception as e:
            print(f"✗ Error loading state: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Execute command
    commands = {
        'create': create_account,
        'balance': check_balance,
        'deposit': deposit_funds,
        'withdraw': withdraw_funds,
        'transfer': transfer_funds,
        'history': show_history,
        'stats': show_stats
    }
    
    commands[args.command](bank, args)


if __name__ == '__main__':
    main()
