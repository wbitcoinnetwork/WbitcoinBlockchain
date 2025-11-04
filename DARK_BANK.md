# Dark Bank

A privacy-focused banking system for the Wbitcoin Blockchain. Dark Bank provides anonymous account management, encrypted transactions, and secure balance tracking for the WBTC network.

## Overview

Dark Bank is designed to provide privacy-first banking operations on the Wbitcoin blockchain, managing the 500 trillion WBTC supply with complete anonymity and security.

### Key Features

- **Anonymous Accounts**: Hash-based account IDs ensure complete anonymity
- **Private Transactions**: All transactions are cryptographically signed and encrypted
- **Secure Balance Management**: Track WBTC balances with precision
- **Transaction History**: View transaction history while maintaining privacy
- **State Persistence**: Save and load bank state for continuity
- **Supply Management**: Enforces total WBTC supply limits

## Installation

No external dependencies required. Dark Bank uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/wbitcoinnetwork/WbitcoinBlockchain.git
cd WbitcoinBlockchain

# Make CLI executable (optional)
chmod +x dark_bank_cli.py
```

## Quick Start

### Using Python API

```python
from dark_bank import DarkBank

# Initialize Dark Bank
bank = DarkBank()

# Create accounts
account1 = bank.create_account(initial_deposit=1000.0)
account2 = bank.create_account()

# Check balance
balance = bank.get_balance(account1)
print(f"Balance: {balance} WBTC")

# Transfer funds
tx_id = bank.transfer(account1, account2, 200.0)

# View transaction history
history = bank.get_transaction_history(account1)
```

### Using CLI

```bash
# Create a new account
python3 dark_bank_cli.py create --deposit 1000 --save bank_state.json

# Check balance
python3 dark_bank_cli.py --load bank_state.json balance <ACCOUNT_ID>

# Deposit funds
python3 dark_bank_cli.py --load bank_state.json deposit <ACCOUNT_ID> 500 --save bank_state.json

# Transfer funds
python3 dark_bank_cli.py --load bank_state.json transfer <FROM_ACCOUNT> <TO_ACCOUNT> 200 --save bank_state.json

# View transaction history
python3 dark_bank_cli.py --load bank_state.json history <ACCOUNT_ID> --limit 10

# Show system statistics
python3 dark_bank_cli.py --load bank_state.json stats
```

## API Reference

### DarkBank Class

Main class for Dark Bank operations.

#### Methods

##### `create_account(initial_deposit=0.0) -> str`
Create a new anonymous account.

**Parameters:**
- `initial_deposit` (float): Initial WBTC deposit amount (default: 0.0)

**Returns:**
- Account ID (64-character SHA256 hash)

**Raises:**
- `ValueError`: If deposit is negative or exceeds total supply

**Example:**
```python
account_id = bank.create_account(initial_deposit=1000.0)
```

##### `get_balance(account_id) -> float`
Get current account balance.

**Parameters:**
- `account_id` (str): Account identifier

**Returns:**
- Balance in WBTC

**Raises:**
- `ValueError`: If account not found

**Example:**
```python
balance = bank.get_balance(account_id)
```

##### `deposit(account_id, amount) -> str`
Deposit WBTC to an account.

**Parameters:**
- `account_id` (str): Target account
- `amount` (float): Deposit amount

**Returns:**
- Transaction ID

**Raises:**
- `ValueError`: If account not found, amount invalid, or exceeds supply

**Example:**
```python
tx_id = bank.deposit(account_id, 500.0)
```

##### `withdraw(account_id, amount) -> str`
Withdraw WBTC from an account.

**Parameters:**
- `account_id` (str): Source account
- `amount` (float): Withdrawal amount

**Returns:**
- Transaction ID

**Raises:**
- `ValueError`: If account not found, amount invalid, or insufficient balance

**Example:**
```python
tx_id = bank.withdraw(account_id, 200.0)
```

##### `transfer(from_account, to_account, amount) -> str`
Transfer WBTC between accounts.

**Parameters:**
- `from_account` (str): Source account
- `to_account` (str): Destination account
- `amount` (float): Transfer amount

**Returns:**
- Transaction ID

**Raises:**
- `ValueError`: If accounts not found, amount invalid, or insufficient balance

**Example:**
```python
tx_id = bank.transfer(account1, account2, 300.0)
```

##### `get_transaction_history(account_id, limit=10) -> List[Dict]`
Get transaction history for an account.

**Parameters:**
- `account_id` (str): Account to query
- `limit` (int): Maximum transactions to return (default: 10)

**Returns:**
- List of transaction dictionaries (most recent first)

**Raises:**
- `ValueError`: If account not found

**Example:**
```python
history = bank.get_transaction_history(account_id, limit=20)
```

##### `get_system_stats() -> Dict`
Get Dark Bank system statistics.

**Returns:**
- Dictionary containing:
  - `total_accounts`: Number of accounts
  - `total_transactions`: Number of transactions
  - `total_deposited`: Total WBTC in circulation
  - `total_supply`: Maximum WBTC supply
  - `remaining_supply`: Available WBTC
  - `timestamp`: Current timestamp

**Example:**
```python
stats = bank.get_system_stats()
print(f"Total Accounts: {stats['total_accounts']}")
```

##### `save_state(filepath) -> None`
Save bank state to file.

**Parameters:**
- `filepath` (str): Path to save state file

**Example:**
```python
bank.save_state('bank_state.json')
```

##### `load_state(filepath) -> None`
Load bank state from file.

**Parameters:**
- `filepath` (str): Path to state file

**Example:**
```python
bank.load_state('bank_state.json')
```

### Transaction Data Structure

```python
{
    'tx_id': str,           # Transaction ID (SHA256 hash)
    'from_account': str,    # Source account ID or 'SYSTEM'
    'to_account': str,      # Destination account ID or 'SYSTEM'
    'amount': float,        # Transaction amount in WBTC
    'timestamp': float,     # Unix timestamp
    'signature': str        # Transaction signature (SHA256 hash)
}
```

### Account Data Structure

```python
{
    'account_id': str,      # Account ID (SHA256 hash)
    'balance': float,       # Current balance in WBTC
    'created_at': float,    # Creation timestamp
    'is_anonymous': bool    # Always True for Dark Bank
}
```

## Security Features

### Anonymous Accounts
- Account IDs are SHA256 hashes, providing anonymity
- No personal information required or stored
- Cryptographically unique identifiers

### Transaction Privacy
- All transactions cryptographically signed
- Hash-based transaction IDs prevent tracking
- Timestamp-based signature generation

### Supply Enforcement
- Maximum supply: 500,000,000,000,000 WBTC
- Automatic validation on all deposits
- Prevents inflation beyond total supply

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python3 -m unittest test_dark_bank.py

# Run with verbose output
python3 -m unittest test_dark_bank.py -v

# Run specific test
python3 -m unittest test_dark_bank.TestDarkBank.test_create_account
```

### Test Coverage

The test suite includes:
- Account creation and management
- Deposit/withdrawal operations
- Transfer operations
- Transaction history
- State persistence
- Error handling
- Edge cases
- Security validations

## Examples

### Basic Banking Operations

```python
from dark_bank import DarkBank

# Initialize
bank = DarkBank()

# Create accounts
alice = bank.create_account(initial_deposit=10000.0)
bob = bank.create_account(initial_deposit=5000.0)

# Alice sends 1000 WBTC to Bob
bank.transfer(alice, bob, 1000.0)

# Check balances
print(f"Alice: {bank.get_balance(alice)} WBTC")  # 9000.0
print(f"Bob: {bank.get_balance(bob)} WBTC")      # 6000.0
```

### State Persistence

```python
from dark_bank import DarkBank

# Create and use bank
bank = DarkBank()
account = bank.create_account(initial_deposit=1000.0)
bank.deposit(account, 500.0)

# Save state
bank.save_state('my_bank.json')

# Later, restore state
new_bank = DarkBank()
new_bank.load_state('my_bank.json')

# State is preserved
balance = new_bank.get_balance(account)  # 1500.0
```

### Transaction Tracking

```python
from dark_bank import DarkBank

bank = DarkBank()
account = bank.create_account(initial_deposit=1000.0)

# Multiple operations
bank.deposit(account, 200.0)
bank.withdraw(account, 100.0)
bank.deposit(account, 300.0)

# View history
history = bank.get_transaction_history(account, limit=5)
for tx in history:
    print(f"TX: {tx['tx_id'][:16]}... | Amount: {tx['amount']} WBTC")
```

## CLI Examples

### Complete Workflow

```bash
# 1. Create first account with initial deposit
python3 dark_bank_cli.py create --deposit 10000 --save bank.json
# Output: Account created successfully!
#         Account ID: a1b2c3d4...

# 2. Create second account
python3 dark_bank_cli.py --load bank.json create --save bank.json
# Output: Account created successfully!
#         Account ID: e5f6g7h8...

# 3. Check balance
python3 dark_bank_cli.py --load bank.json balance a1b2c3d4...
# Output: Account Balance: 10,000 WBTC

# 4. Transfer funds
python3 dark_bank_cli.py --load bank.json transfer a1b2c3d4... e5f6g7h8... 2000 --save bank.json
# Output: ✓ Transfer successful!

# 5. View transaction history
python3 dark_bank_cli.py --load bank.json history a1b2c3d4... --limit 5

# 6. Check system statistics
python3 dark_bank_cli.py --load bank.json stats
```

## Architecture

### Components

1. **DarkBank**: Core banking system
2. **Account**: Account data structure
3. **Transaction**: Transaction data structure
4. **CLI**: Command-line interface

### Design Principles

- **Privacy First**: All operations prioritize anonymity
- **Immutable Transactions**: Transaction records cannot be altered
- **Supply Constraints**: Enforces maximum WBTC supply
- **Cryptographic Security**: SHA256 hashing for IDs and signatures

## License

This project is part of the Wbitcoin Blockchain ecosystem.

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows existing style
- Privacy features are maintained
- Documentation is updated

## Support

For issues or questions, please open an issue on GitHub.

---

**Dark Bank** - Privacy-focused banking for the Wbitcoin Blockchain
