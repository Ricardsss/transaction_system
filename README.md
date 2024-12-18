# Banking API

This is a Django-based API for a banking system. The system supports account management, transactions, disputes, recurring transactions, and user authentication.

## Endpoints

### Authentication

#### Register

**POST** `/auth/register/`

```json
Request:
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "role": "customer"
}

Response:
{
  "message": "User registered successfully!",
  "user": "uuid-of-user"
}
```

#### Login

**POST** `/auth/login/`

```json
Request:
{
  "username": "johndoe",
  "password": "securepassword"
}

Response:
{
  "message": "Login successful"
}
```

#### Logout

**DELETE** `/auth/logout/`

```json
Response:
{
  "message": "Logout successful"
}
```

---

### Accounts

#### List Accounts

**GET** `/accounts/`

```json
Response:
{
  "accounts": [
    {
      "id": "uuid-of-account",
      "account_number": "123456789012",
      "account_type": "savings",
      "balance": "1000.00",
      "currency": "CAD",
      "status": "active",
      "created_at": "2023-11-20T10:00:00Z"
    }
  ]
}
```

#### Create Account

**POST** `/accounts/`

```json
Request:
{
  "account_type": "checking",
  "balance": 500.00,
  "currency": "USD"
}

Response:
{
  "message": "Account created successfully!",
  "account": "uuid-of-account"
}
```

#### Get Account Details

**GET** `/accounts/<uuid:pk>/`

```json
Response:
{
  "id": "uuid-of-account",
  "account_number": "123456789012",
  "account_type": "savings",
  "balance": "1000.00",
  "currency": "CAD",
  "status": "active",
  "created_at": "2023-11-20T10:00:00Z"
}
```

#### Update Account Status

**PATCH** `/accounts/<uuid:pk>/`

```json
Request:
{
  "status": "closed"
}

Response:
{
  "message": "Account updated successfully!"
}
```

---

### Transactions

#### Deposit

**POST** `/accounts/transactions/deposit/<uuid:pk>/`

```json
Request:
{
  "amount": 100.00
}

Response:
{
  "message": "Deposit successful.",
  "balance": "1100.00",
  "transaction": "uuid-of-transaction"
}
```

#### Withdraw

**POST** `/accounts/transactions/withdraw/<uuid:pk>/`

```json
Request:
{
  "amount": 50.00
}

Response:
{
  "message": "Withdrawal successful.",
  "balance": "950.00",
  "transaction": "uuid-of-transaction"
}
```

#### Transfer

**POST** `/accounts/transactions/transfer/`

```json
Request:
{
  "amount": 200.00,
  "source_account_id": "uuid-of-source-account",
  "destination_account_id": "uuid-of-destination-account"
}

Response:
{
  "message": "Transfer successful.",
  "transaction": "uuid-of-transaction"
}
```

---

### Recurring Transactions

#### List Recurring Transactions

**GET** `/accounts/recurring/`

```json
Response:
{
  "status": "success",
  "transactions": [
    {
      "id": "uuid-of-recurring-transaction",
      "user": "uuid-of-user",
      "source_account": "uuid-of-source-account",
      "destination_account": "uuid-of-destination-account",
      "amount": "100.00",
      "frequency": "monthly",
      "start_date": "2023-11-01",
      "end_date": "2024-11-01",
      "is_active": true
    }
  ]
}
```

#### Create Recurring Transaction

**POST** `/accounts/recurring/`

```json
Request:
{
  "source_account_id": "uuid-of-source-account",
  "destination_account_id": "uuid-of-destination-account",
  "amount": 100.00,
  "frequency": "monthly",
  "start_date": "2023-11-01",
  "end_date": "2024-11-01"
}

Response:
{
  "message": "Recurring transaction created successfully!",
  "transaction": "uuid-of-recurring-transaction"
}
```

#### Update Recurring Transaction

**PATCH** `/accounts/recurring/<uuid:pk>/`

```json
Request:
{
  "frequency": "weekly"
}

Response:
{
  "message": "Recurring transaction updated successfully!"
}
```

#### Cancel Recurring Transaction

**DELETE** `/accounts/recurring/<uuid:pk>/`

```json
Response:
{
  "message": "Transaction cancelled successfully."
}
```

---

### Disputes

#### List Disputes

**GET** `/accounts/disputes/`

```json
Response:
{
  "disputes": [
    {
      "id": "uuid-of-dispute",
      "transaction_id": "uuid-of-transaction",
      "reason": "unauthorized_charge",
      "status": "open",
      "created_at": "2023-11-20T10:00:00Z"
    }
  ]
}
```

#### Create Dispute

**POST** `/accounts/disputes/`

```json
Request:
{
  "transaction": "uuid-of-transaction",
  "reason": "unauthorized_charge"
}

Response:
{
  "message": "Dispute created successfully!",
  "dispute": "uuid-of-dispute"
}
```

#### Update Dispute Status

**PATCH** `/accounts/disputes/<uuid:pk>/`

```json
Request:
{
  "status": "resolved",
  "resolution_details": "Issue resolved with a refund."
}

Response:
{
  "message": "Dispute updated successfully."
}
```

### Reports

#### Generate Account Statement

**GET** `/accounts/reports/account-statement/?account_id=<uuid>&start_date=<YYYY-MM-DD>&end_date=<YYYY-MM-DD>`

```json
Response:
{
  "account": {
    "account_number": "1234567890",
    "account_type": "savings"
  },
  "outgoing_transactions": [
    {
      "id": "uuid-of-transaction",
      "transaction_type": "withdrawal",
      "amount": "200.00",
      "description": "ATM withdrawal",
      "created_at": "2024-01-05T10:30:00Z"
    },
    {
      "id": "uuid-of-transaction",
      "transaction_type": "transfer",
      "amount": "300.00",
      "description": "Transfer to checking account",
      "created_at": "2024-01-10T14:20:00Z"
    }
  ],
  "incoming_transactions": [
    {
      "id": "uuid-of-transaction",
      "transaction_type": "deposit",
      "amount": "500.00",
      "description": "Salary deposit",
      "created_at": "2024-01-08T09:15:00Z"
    }
  ]
}
```

#### Generate Internal Report

**GET** `/accounts/reports/internal-summary/`

```json
Response:
{
  "total_deposits": 10000.0,
  "total_withdrawal": 3000.0,
  "total_transfers": 2000.0,
  "net_balance": 7000.0,
  "transaction_count": 45
}
```

---

## Setup Instructions

1. Clone the repository.
2. Change into the project folder

   ```bash
   cd transaction_system
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the Django development server:
   ```bash
   python manage.py runserver
   ```
6. Create a .env file in the root folder and add SECRET_KEY and set it to a secret key generated from https://djecrety.ir.

## Online Access

This API is also accessible via Heroku. In order to reduce costs, the url is only available upon request. If you would like access to test it out, please contact me via my email address on my resume.
