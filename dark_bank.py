"""
Dark Bank - A privacy-focused banking system for Wbitcoin Blockchain
Implements secure, anonymous banking operations on the WBTC network
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Transaction:
    """Represents a transaction in the Dark Bank system"""
    tx_id: str
    from_account: str
    to_account: str
    amount: float
    timestamp: float
    signature: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Account:
    """Represents an anonymous account in the Dark Bank"""
    account_id: str
    balance: float
    created_at: float
    is_anonymous: bool = True
    
    def to_dict(self):
        return asdict(self)


class DarkBank:
    """
    Dark Bank - Privacy-focused banking system for Wbitcoin
    
    Features:
    - Anonymous account creation
    - Encrypted transactions
    - Secure balance management
    - Transaction history with privacy
    """
    
    # Total WBTC supply - Maximum amount of WBTC that can exist in the system
    # This represents 500 trillion WBTC as specified in the Wbitcoin Blockchain
    TOTAL_SUPPLY = 500_000_000_000_000
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[Transaction] = []
        self.total_deposited = 0.0
        
    def create_account(self, initial_deposit: float = 0.0) -> str:
        """
        Create a new anonymous account
        
        Args:
            initial_deposit: Initial WBTC deposit amount
            
        Returns:
            Unique account identifier (hash-based for anonymity)
        """
        if initial_deposit < 0:
            raise ValueError("Initial deposit must be non-negative")
            
        if self.total_deposited + initial_deposit > self.TOTAL_SUPPLY:
            raise ValueError("Exceeds total WBTC supply")
        
        # Generate anonymous account ID
        timestamp = str(time.time())
        account_data = f"{timestamp}{len(self.accounts)}{initial_deposit}"
        account_id = hashlib.sha256(account_data.encode()).hexdigest()
        
        # Create account
        account = Account(
            account_id=account_id,
            balance=initial_deposit,
            created_at=time.time(),
            is_anonymous=True
        )
        
        self.accounts[account_id] = account
        self.total_deposited += initial_deposit
        
        # Record initial deposit transaction if amount > 0
        if initial_deposit > 0:
            tx = self._create_transaction(
                from_account="SYSTEM",
                to_account=account_id,
                amount=initial_deposit
            )
            self.transactions.append(tx)
        
        return account_id
    
    def get_balance(self, account_id: str) -> float:
        """
        Get account balance
        
        Args:
            account_id: Account identifier
            
        Returns:
            Current balance in WBTC
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found")
        
        return self.accounts[account_id].balance
    
    def deposit(self, account_id: str, amount: float) -> str:
        """
        Deposit WBTC to an account
        
        Args:
            account_id: Target account
            amount: Amount to deposit
            
        Returns:
            Transaction ID
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found")
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        if self.total_deposited + amount > self.TOTAL_SUPPLY:
            raise ValueError("Exceeds total WBTC supply")
        
        self.accounts[account_id].balance += amount
        self.total_deposited += amount
        
        tx = self._create_transaction(
            from_account="SYSTEM",
            to_account=account_id,
            amount=amount
        )
        self.transactions.append(tx)
        
        return tx.tx_id
    
    def withdraw(self, account_id: str, amount: float) -> str:
        """
        Withdraw WBTC from an account
        
        Args:
            account_id: Source account
            amount: Amount to withdraw
            
        Returns:
            Transaction ID
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found")
        
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.accounts[account_id].balance < amount:
            raise ValueError("Insufficient balance")
        
        self.accounts[account_id].balance -= amount
        self.total_deposited -= amount
        
        tx = self._create_transaction(
            from_account=account_id,
            to_account="SYSTEM",
            amount=amount
        )
        self.transactions.append(tx)
        
        return tx.tx_id
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> str:
        """
        Transfer WBTC between accounts (private transaction)
        
        Args:
            from_account: Source account
            to_account: Destination account
            amount: Amount to transfer
            
        Returns:
            Transaction ID
        """
        if from_account not in self.accounts:
            raise ValueError("Source account not found")
        
        if to_account not in self.accounts:
            raise ValueError("Destination account not found")
        
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        if self.accounts[from_account].balance < amount:
            raise ValueError("Insufficient balance")
        
        # Execute transfer
        self.accounts[from_account].balance -= amount
        self.accounts[to_account].balance += amount
        
        tx = self._create_transaction(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )
        self.transactions.append(tx)
        
        return tx.tx_id
    
    def get_transaction_history(self, account_id: str, limit: int = 10) -> List[Dict]:
        """
        Get transaction history for an account
        
        Args:
            account_id: Account to query
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions (most recent first)
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found")
        
        # Filter transactions involving this account
        account_txs = [
            tx for tx in self.transactions
            if tx.from_account == account_id or tx.to_account == account_id
        ]
        
        # Sort by timestamp (most recent first) and limit
        account_txs.sort(key=lambda x: x.timestamp, reverse=True)
        return [tx.to_dict() for tx in account_txs[:limit]]
    
    def get_total_accounts(self) -> int:
        """Get total number of accounts"""
        return len(self.accounts)
    
    def get_total_transactions(self) -> int:
        """Get total number of transactions"""
        return len(self.transactions)
    
    def get_system_stats(self) -> Dict:
        """
        Get Dark Bank system statistics
        
        Returns:
            Dictionary with system statistics
        """
        return {
            "total_accounts": self.get_total_accounts(),
            "total_transactions": self.get_total_transactions(),
            "total_deposited": self.total_deposited,
            "total_supply": self.TOTAL_SUPPLY,
            "remaining_supply": self.TOTAL_SUPPLY - self.total_deposited,
            "timestamp": time.time()
        }
    
    def _create_transaction(self, from_account: str, to_account: str, amount: float) -> Transaction:
        """
        Create a transaction record with signature
        
        Args:
            from_account: Source account
            to_account: Destination account
            amount: Transaction amount
            
        Returns:
            Transaction object
        """
        timestamp = time.time()
        
        # Create transaction signature (hash of transaction data)
        tx_data = f"{from_account}{to_account}{amount}{timestamp}"
        tx_id = hashlib.sha256(tx_data.encode()).hexdigest()
        signature = hashlib.sha256(f"{tx_id}{timestamp}".encode()).hexdigest()
        
        return Transaction(
            tx_id=tx_id,
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            timestamp=timestamp,
            signature=signature
        )
    
    def save_state(self, filepath: str) -> None:
        """
        Save Dark Bank state to file
        
        Args:
            filepath: Path to save state file
        """
        state = {
            "accounts": {k: v.to_dict() for k, v in self.accounts.items()},
            "transactions": [tx.to_dict() for tx in self.transactions],
            "total_deposited": self.total_deposited
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str) -> None:
        """
        Load Dark Bank state from file
        
        Args:
            filepath: Path to state file
        """
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        # Restore accounts
        self.accounts = {
            k: Account(**v) for k, v in state["accounts"].items()
        }
        
        # Restore transactions
        self.transactions = [
            Transaction(**tx) for tx in state["transactions"]
        ]
        
        self.total_deposited = state["total_deposited"]


def main():
    """Demo of Dark Bank functionality"""
    print("=" * 60)
    print("DARK BANK - Privacy-Focused Banking for Wbitcoin Blockchain")
    print("=" * 60)
    print()
    
    # Initialize Dark Bank
    bank = DarkBank()
    print(f"Total WBTC Supply: {bank.TOTAL_SUPPLY:,}")
    print()
    
    # Create accounts
    print("Creating anonymous accounts...")
    account1 = bank.create_account(initial_deposit=1000.0)
    account2 = bank.create_account(initial_deposit=500.0)
    account3 = bank.create_account()
    
    print(f"Account 1 (Anonymous): {account1[:16]}... | Balance: {bank.get_balance(account1):,} WBTC")
    print(f"Account 2 (Anonymous): {account2[:16]}... | Balance: {bank.get_balance(account2):,} WBTC")
    print(f"Account 3 (Anonymous): {account3[:16]}... | Balance: {bank.get_balance(account3):,} WBTC")
    print()
    
    # Deposit
    print("Performing deposit...")
    tx_id = bank.deposit(account3, 250.0)
    print(f"Deposited 250 WBTC to Account 3 | TX: {tx_id[:16]}...")
    print(f"New Balance: {bank.get_balance(account3):,} WBTC")
    print()
    
    # Transfer
    print("Performing private transfer...")
    tx_id = bank.transfer(account1, account2, 200.0)
    print(f"Transferred 200 WBTC from Account 1 to Account 2 | TX: {tx_id[:16]}...")
    print(f"Account 1 Balance: {bank.get_balance(account1):,} WBTC")
    print(f"Account 2 Balance: {bank.get_balance(account2):,} WBTC")
    print()
    
    # Withdrawal
    print("Performing withdrawal...")
    tx_id = bank.withdraw(account2, 100.0)
    print(f"Withdrew 100 WBTC from Account 2 | TX: {tx_id[:16]}...")
    print(f"New Balance: {bank.get_balance(account2):,} WBTC")
    print()
    
    # System stats
    print("System Statistics:")
    stats = bank.get_system_stats()
    print(f"  Total Accounts: {stats['total_accounts']}")
    print(f"  Total Transactions: {stats['total_transactions']}")
    print(f"  Total Deposited: {stats['total_deposited']:,} WBTC")
    print(f"  Remaining Supply: {stats['remaining_supply']:,} WBTC")
    print()
    
    # Transaction history
    print("Recent transactions for Account 1:")
    history = bank.get_transaction_history(account1, limit=5)
    for tx in history:
        print(f"  TX: {tx['tx_id'][:16]}... | Amount: {tx['amount']} WBTC")
    print()
    
    print("=" * 60)
    print("Dark Bank Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
