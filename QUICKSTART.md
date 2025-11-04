# Quick Start Guide - Dark Bank

Get started with Dark Bank in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- No external dependencies required

## Installation

```bash
# Clone the repository
git clone https://github.com/wbitcoinnetwork/WbitcoinBlockchain.git
cd WbitcoinBlockchain
```

## Try It Now

### 1. Run the Demo

```bash
python3 dark_bank.py
```

This will show you Dark Bank in action with sample accounts and transactions.

### 2. Run the Complete Example

```bash
python3 example.py
```

This demonstrates a complete workflow including:
- Creating accounts
- Deposits and withdrawals
- Transfers between accounts
- Transaction history
- State persistence

### 3. Run Tests

```bash
python3 -m unittest test_dark_bank.py -v
```

All 23 tests should pass.

### 4. Use the CLI

Create your first account:

```bash
python3 dark_bank_cli.py create --deposit 10000 --save mybank.json
```

This will:
- Create a new anonymous account
- Deposit 10,000 WBTC
- Save the state to `mybank.json`
- Display your account ID

Check system stats:

```bash
python3 dark_bank_cli.py --load mybank.json stats
```

## Next Steps

### Using the Python API

```python
from dark_bank import DarkBank

# Create bank
bank = DarkBank()

# Create accounts
account1 = bank.create_account(initial_deposit=5000.0)
account2 = bank.create_account()

# Transfer
bank.transfer(account1, account2, 1000.0)

# Check balance
balance = bank.get_balance(account2)
print(f"Balance: {balance} WBTC")
```

### Common CLI Commands

```bash
# Create account
python3 dark_bank_cli.py create --deposit 1000 --save bank.json

# Check balance (replace ACCOUNT_ID with your actual ID)
python3 dark_bank_cli.py --load bank.json balance ACCOUNT_ID

# Deposit funds
python3 dark_bank_cli.py --load bank.json deposit ACCOUNT_ID 500 --save bank.json

# Transfer between accounts
python3 dark_bank_cli.py --load bank.json transfer FROM_ID TO_ID 200 --save bank.json

# View transaction history
python3 dark_bank_cli.py --load bank.json history ACCOUNT_ID --limit 10

# Show statistics
python3 dark_bank_cli.py --load bank.json stats
```

## Documentation

For complete documentation, see:
- [DARK_BANK.md](DARK_BANK.md) - Full API reference and examples
- [README.md](README.md) - Project overview

## Features at a Glance

✓ **Anonymous Accounts** - No personal information required  
✓ **Private Transactions** - Cryptographically signed and encrypted  
✓ **Secure Balances** - Accurate tracking with supply enforcement  
✓ **Transaction History** - Complete audit trail  
✓ **State Persistence** - Save and restore your bank state  
✓ **CLI Interface** - Easy command-line operations  

## Need Help?

- Check the [full documentation](DARK_BANK.md)
- Run tests to see examples: `python3 -m unittest test_dark_bank.py -v`
- Look at [example.py](example.py) for complete workflow

## Security

Dark Bank enforces:
- Maximum supply of 500 trillion WBTC
- Cryptographic account IDs (SHA256)
- Transaction signatures
- Balance validation on all operations

---

Happy banking with Dark Bank! 🏦
