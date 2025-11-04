"""
Tests for Dark Bank system
"""

import unittest
import os
import json
from dark_bank import DarkBank, Account, Transaction


class TestDarkBank(unittest.TestCase):
    """Test suite for Dark Bank functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.bank = DarkBank()
    
    def test_create_account_no_deposit(self):
        """Test creating an account with no initial deposit"""
        account_id = self.bank.create_account()
        
        self.assertIsNotNone(account_id)
        self.assertEqual(len(account_id), 64)  # SHA256 hash length
        self.assertEqual(self.bank.get_balance(account_id), 0.0)
        self.assertEqual(self.bank.get_total_accounts(), 1)
    
    def test_create_account_with_deposit(self):
        """Test creating an account with initial deposit"""
        initial_amount = 1000.0
        account_id = self.bank.create_account(initial_deposit=initial_amount)
        
        self.assertEqual(self.bank.get_balance(account_id), initial_amount)
        self.assertEqual(self.bank.total_deposited, initial_amount)
        self.assertEqual(self.bank.get_total_transactions(), 1)
    
    def test_create_account_negative_deposit(self):
        """Test that negative deposits are rejected"""
        with self.assertRaises(ValueError) as context:
            self.bank.create_account(initial_deposit=-100.0)
        
        self.assertIn("non-negative", str(context.exception))
    
    def test_create_account_exceeds_supply(self):
        """Test that deposits exceeding total supply are rejected"""
        with self.assertRaises(ValueError) as context:
            self.bank.create_account(initial_deposit=self.bank.TOTAL_SUPPLY + 1)
        
        self.assertIn("supply", str(context.exception))
    
    def test_get_balance(self):
        """Test getting account balance"""
        account_id = self.bank.create_account(initial_deposit=500.0)
        balance = self.bank.get_balance(account_id)
        
        self.assertEqual(balance, 500.0)
    
    def test_get_balance_nonexistent_account(self):
        """Test getting balance for nonexistent account"""
        with self.assertRaises(ValueError) as context:
            self.bank.get_balance("nonexistent")
        
        self.assertIn("not found", str(context.exception))
    
    def test_deposit(self):
        """Test depositing WBTC"""
        account_id = self.bank.create_account()
        tx_id = self.bank.deposit(account_id, 250.0)
        
        self.assertIsNotNone(tx_id)
        self.assertEqual(self.bank.get_balance(account_id), 250.0)
        self.assertEqual(self.bank.total_deposited, 250.0)
    
    def test_deposit_negative_amount(self):
        """Test that negative deposits are rejected"""
        account_id = self.bank.create_account()
        
        with self.assertRaises(ValueError) as context:
            self.bank.deposit(account_id, -50.0)
        
        self.assertIn("positive", str(context.exception))
    
    def test_deposit_zero_amount(self):
        """Test that zero deposits are rejected"""
        account_id = self.bank.create_account()
        
        with self.assertRaises(ValueError) as context:
            self.bank.deposit(account_id, 0.0)
        
        self.assertIn("positive", str(context.exception))
    
    def test_withdraw(self):
        """Test withdrawing WBTC"""
        account_id = self.bank.create_account(initial_deposit=1000.0)
        tx_id = self.bank.withdraw(account_id, 300.0)
        
        self.assertIsNotNone(tx_id)
        self.assertEqual(self.bank.get_balance(account_id), 700.0)
        self.assertEqual(self.bank.total_deposited, 700.0)
    
    def test_withdraw_insufficient_balance(self):
        """Test that withdrawals with insufficient balance are rejected"""
        account_id = self.bank.create_account(initial_deposit=100.0)
        
        with self.assertRaises(ValueError) as context:
            self.bank.withdraw(account_id, 200.0)
        
        self.assertIn("Insufficient", str(context.exception))
    
    def test_transfer(self):
        """Test transferring WBTC between accounts"""
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account(initial_deposit=500.0)
        
        tx_id = self.bank.transfer(account1, account2, 200.0)
        
        self.assertIsNotNone(tx_id)
        self.assertEqual(self.bank.get_balance(account1), 800.0)
        self.assertEqual(self.bank.get_balance(account2), 700.0)
        # Total deposited should remain the same
        self.assertEqual(self.bank.total_deposited, 1500.0)
    
    def test_transfer_insufficient_balance(self):
        """Test that transfers with insufficient balance are rejected"""
        account1 = self.bank.create_account(initial_deposit=100.0)
        account2 = self.bank.create_account()
        
        with self.assertRaises(ValueError) as context:
            self.bank.transfer(account1, account2, 200.0)
        
        self.assertIn("Insufficient", str(context.exception))
    
    def test_transfer_nonexistent_source(self):
        """Test transfer from nonexistent account"""
        account2 = self.bank.create_account()
        
        with self.assertRaises(ValueError) as context:
            self.bank.transfer("nonexistent", account2, 100.0)
        
        self.assertIn("not found", str(context.exception))
    
    def test_transfer_nonexistent_destination(self):
        """Test transfer to nonexistent account"""
        account1 = self.bank.create_account(initial_deposit=500.0)
        
        with self.assertRaises(ValueError) as context:
            self.bank.transfer(account1, "nonexistent", 100.0)
        
        self.assertIn("not found", str(context.exception))
    
    def test_transaction_history(self):
        """Test getting transaction history"""
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account()
        
        # Perform several transactions
        self.bank.transfer(account1, account2, 100.0)
        self.bank.withdraw(account1, 50.0)
        self.bank.deposit(account1, 200.0)
        
        history = self.bank.get_transaction_history(account1, limit=10)
        
        # Should have 4 transactions: initial deposit + 3 operations
        self.assertEqual(len(history), 4)
        
        # Most recent should be the deposit
        self.assertEqual(history[0]['to_account'], account1)
        self.assertEqual(history[0]['amount'], 200.0)
    
    def test_transaction_history_limit(self):
        """Test transaction history limit"""
        account1 = self.bank.create_account(initial_deposit=100.0)
        account2 = self.bank.create_account()
        
        # Create 5 transactions
        for _ in range(5):
            self.bank.deposit(account1, 10.0)
        
        history = self.bank.get_transaction_history(account1, limit=3)
        
        # Should only return 3 most recent
        self.assertEqual(len(history), 3)
    
    def test_system_stats(self):
        """Test getting system statistics"""
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account(initial_deposit=500.0)
        
        stats = self.bank.get_system_stats()
        
        self.assertEqual(stats['total_accounts'], 2)
        self.assertEqual(stats['total_transactions'], 2)
        self.assertEqual(stats['total_deposited'], 1500.0)
        self.assertEqual(stats['total_supply'], self.bank.TOTAL_SUPPLY)
        self.assertEqual(stats['remaining_supply'], self.bank.TOTAL_SUPPLY - 1500.0)
        self.assertIn('timestamp', stats)
    
    def test_save_and_load_state(self):
        """Test saving and loading bank state"""
        # Create some accounts and transactions
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account(initial_deposit=500.0)
        self.bank.transfer(account1, account2, 200.0)
        
        # Save state
        test_file = '/tmp/test_dark_bank_state.json'
        self.bank.save_state(test_file)
        
        # Create new bank and load state
        new_bank = DarkBank()
        new_bank.load_state(test_file)
        
        # Verify state was restored
        self.assertEqual(new_bank.get_total_accounts(), 2)
        self.assertEqual(new_bank.get_total_transactions(), 3)  # 2 initial + 1 transfer
        self.assertEqual(new_bank.get_balance(account1), 800.0)
        self.assertEqual(new_bank.get_balance(account2), 700.0)
        self.assertEqual(new_bank.total_deposited, 1500.0)
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
    
    def test_unique_account_ids(self):
        """Test that account IDs are unique"""
        account_ids = set()
        
        for _ in range(100):
            account_id = self.bank.create_account()
            self.assertNotIn(account_id, account_ids)
            account_ids.add(account_id)
    
    def test_transaction_signatures(self):
        """Test that transactions have valid signatures"""
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account()
        
        self.bank.transfer(account1, account2, 100.0)
        
        # Get transaction
        history = self.bank.get_transaction_history(account1, limit=10)
        
        for tx in history:
            self.assertIn('tx_id', tx)
            self.assertIn('signature', tx)
            self.assertEqual(len(tx['tx_id']), 64)  # SHA256
            self.assertEqual(len(tx['signature']), 64)  # SHA256
    
    def test_account_anonymity(self):
        """Test that accounts are marked as anonymous"""
        account_id = self.bank.create_account()
        account = self.bank.accounts[account_id]
        
        self.assertTrue(account.is_anonymous)
    
    def test_multiple_transfers(self):
        """Test multiple transfers in sequence"""
        account1 = self.bank.create_account(initial_deposit=1000.0)
        account2 = self.bank.create_account()
        account3 = self.bank.create_account()
        
        # Chain of transfers
        self.bank.transfer(account1, account2, 300.0)
        self.bank.transfer(account2, account3, 100.0)
        self.bank.transfer(account3, account1, 50.0)
        
        # Verify final balances
        self.assertEqual(self.bank.get_balance(account1), 750.0)  # 1000 - 300 + 50
        self.assertEqual(self.bank.get_balance(account2), 200.0)  # 0 + 300 - 100
        self.assertEqual(self.bank.get_balance(account3), 50.0)   # 0 + 100 - 50


if __name__ == '__main__':
    unittest.main()
