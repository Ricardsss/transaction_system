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

---

## Setup Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Start the development server: `python manage.py runserver`.

## License

This project is licensed under the MIT License.
