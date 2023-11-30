# Email Verification API
Validate email addresses using our Email Verification API. Check the format, domain, and existence of an email address to ensure it's deliverable.
## Sample API Request

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}

params = {
    'email': 'example@email.com'
}

response = requests.get('https://api.tinyapi.co/v1/email-verification/', headers=headers, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

## Sample API Response

```json
{
    "email": "example@email.com",
    "isValid": true,
    "isDisposable": false,
    "isRoleAccount": false,
    "isFreeMail": false,
    "domain": "email.com",
    "mxRecords": ["mx.email.com"]
}
```

Use the Email Verification API to validate email addresses, reduce bounce rates, and maintain a clean email list for your marketing and transactional email campaigns.

## Integration

_Easily integrate Tiny API into your projects_

Integrating Tiny API into your projects is a straightforward process. Follow these simple steps, and you'll have the power of Tiny API at your fingertips.

### Step 1: Sign Up and Get Your API Key

To get started with Tiny API, you'll first need to sign up for an account on our website. Once you've signed up, you'll receive an API key, which you'll need to include in your API requests for authentication.

### Step 2: Choose Your API

Next, you'll need to choose the API you want to integrate into your project. Explore our extensive catalog of APIs, and find the one that best suits your needs. Make sure to familiarize yourself with the API documentation, which includes important information on the available endpoints, request parameters, and response formats.

### Step 3: Make API Requests

With your API key and chosen API in hand, you're now ready to start making API requests. You can use any programming language or tool that supports HTTP requests to make calls to the Tiny API endpoints. Remember to include your API key in the request headers for authentication.
