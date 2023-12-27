# Domain Tracker API
The Domain Tracker API provides a simple and efficient way to track the status and details of domain names. Built using Django and Django REST Framework, this API offers endpoints to check domain availability, retrieve WHOIS information, and monitor domain expiration dates.

## Features
- Domain Status Check: Determine if a domain is registered or available.
- Domain Details: Fetch WHOIS information for a domain, including the owner, expiration date, and registrar details.
- Bulk Domain Tracking: Ability to track multiple domains simultaneously.

## API Endpoints

### 1. Domain Status

**Endpoint**: `/domain-tracker/status/`

- **Method**: `POST`
- **Description**: Checks the registration status of provided domain names.
- **Request Body**:
  ```json
  {
    "domains": ["example.com", "example.org"]
  }
  ```
- **Response**: 
  - Code: `200`
  - Body: 
  ```json
  [
    {"example.com": "Registered"},
    {"example.org": "Available"}
  ]
  ``` 

### 2. Domain Detail

**Endpoint**: `/domain-tracker/details/`

- **Method**: `POST`
- **Description**: Retrieves detailed WHOIS information for a given domain.
- **Request Body**:
  ```json
  {
    "domain": "example.com"
  }
  ```
- **Response**: 
  - Code: `200`
  - Body: 
  ```json
  {
    "domain": "example.com",
    "status": "registered",
    "creation_date": "1995-08-15T04:00:00Z",
    "expiration_date": "2022-08-14T04:00:00Z",
    "last_updated": "2021-07-15T03:45:05Z",
    "registrar": {
        "name": "Example Registrar, Inc.",
        "whois_server": "whois.example-registrar.com",
        "url": "http://www.example-registrar.com"
    },
    "registrant_contact": {
        "name": "Example Company",
        "organization": "Example Company Inc.",
        "address": "123 Example Street, Example City, 12345",
        "country": "Exampleland",
        "phone": "+1.234567890",
        "email": "contact@example.com"
    },
    "name_servers": [
        "ns1.exampledns.com",
        "ns2.exampledns.com",
        "ns3.exampledns.com"
    ],
    "dnssec": "unsigned",
    "status_codes": [
        "clientTransferProhibited",
        "serverDeleteProhibited",
        "serverTransferProhibited",
        "serverUpdateProhibited"
    ],
    "emails": [
        "abuse@example-registrar.com",
        "support@example-registrar.com"
    ],
    "raw_whois_data": "Raw WHOIS data text here..."
  }
  ``` 

## Sample API Request

```python
import requests

headers = {
    'Authorization': 'Api-Key YOUR_API_KEY'
}

body = {
    'domains': ['tinyapi.co', 'tinyapi.com'],
}

response = requests.get('https://api.tinyapi.co/v1/domain-tracker/status/', headers=headers, body=body)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

## Sample API Response

```json
{
    "domain": "example.com",
    "status": "registered",
    "creation_date": "1995-08-15T04:00:00Z",
    "expiration_date": "2022-08-14T04:00:00Z",
    "last_updated": "2021-07-15T03:45:05Z",
    "registrar": {
        "name": "Example Registrar, Inc.",
        "whois_server": "whois.example-registrar.com",
        "url": "http://www.example-registrar.com"
    },
    "registrant_contact": {
        "name": "Example Company",
        "organization": "Example Company Inc.",
        "address": "123 Example Street, Example City, 12345",
        "country": "Exampleland",
        "phone": "+1.234567890",
        "email": "contact@example.com"
    },
    "name_servers": [
        "ns1.exampledns.com",
        "ns2.exampledns.com",
        "ns3.exampledns.com"
    ],
    "dnssec": "unsigned",
    "status_codes": [
        "clientTransferProhibited",
        "serverDeleteProhibited",
        "serverTransferProhibited",
        "serverUpdateProhibited"
    ],
    "emails": [
        "abuse@example-registrar.com",
        "support@example-registrar.com"
    ],
    "raw_whois_data": "Raw WHOIS data text here..."
}
```

Use the Weather Forecast API to get accurate weather forecasts, current conditions, and weather alerts for any location worldwide. It's perfect for travel planning, outdoor activities, and event management.

## Integration

_Easily integrate Tiny API into your projects_

Integrating Tiny API into your projects is a straightforward process. Follow these simple steps, and you'll have the power of Tiny API at your fingertips.

### Step 1: Sign Up and Get Your API Key

To get started with Tiny API, you'll first need to sign up for an account on our website. Once you've signed up, you'll receive an API key, which you'll need to include in your API requests for authentication.

### Step 2: Choose Your API

Next, you'll need to choose the API you want to integrate into your project. Explore our extensive catalog of APIs, and find the one that best suits your needs. Make sure to familiarize yourself with the API documentation, which includes important information on the available endpoints, request parameters, and response formats.

### Step 3: Make API Requests

With your API key and chosen API in hand, you're now ready to start making API requests. You can use any programming language or tool that supports HTTP requests to make calls to the Tiny API endpoints. Remember to include your API key in the request headers for authentication.

