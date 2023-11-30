# IP Geolocation API

The IP Geolocation API provides information about the location of an IP address. It can be used in web applications to provide personalized content, detect fraud, and more.
- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [IP Geolocation (via IP address)](#ip-geolocation-via-ip-address)
    - [`GET /v1/ip-geolocation/<IP_ADDRESS>`](#get-v1ip-geolocationip_address)
      - [Parameters](#parameters)
  - [IP Geolocation (auto-detect IP address)](#ip-geolocation-auto-detect-ip-address)
    - [`GET /v1/ip-geolocation/`](#get-v1ip-geolocation)
      - [Response](#response)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

You can read more about the IP Geolocation API in the [documentation](https://docs.odyssey.co/api/ip-geolocation).

## Getting Started

### Prerequisites

- Python 3.8 or newer
- Django 3.2 or newer
- Docker (optional, but recommended)

### Installation

1. Clone the odyssey repository: `git clone https://github.com/odyssey/odyssey.git`
2. Navigate to the IP Geolocation API directory: `cd odyssey/ip_geolocation`
3. Install the required Python packages: `pip install -r requirements.txt`
4. Apply the migrations: `python manage.py migrate`
5. Run the server: `python manage.py runserver`

Alternatively, you can use Docker to run the API:

```shell
docker-compose up
```
## Usage
Once the server is running, you can use the IP Geolocation API with the following endpoint:

### IP Geolocation (via IP address)
#### `GET /v1/ip-geolocation/<IP_ADDRESS>`
`https://api.odyssey.co/v1/ip-geolocation/<IP_ADDRESS>`

##### Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| `IP_ADDRESS` | `string` | The IP address to geolocate. |

### IP Geolocation (auto-detect IP address)
#### `GET /v1/ip-geolocation/`
`https://api.odyssey.co/v1/ip-geolocation/`

##### Response
```json
{
    "ip": "49.207.196.170",
    "countryCode": "IN",
    "countryName": "India",
    "regionCode": "KA",
    "regionName": "Karnataka",
    "city": "Bengaluru",
    "postalCode": "560008",
    "latitude": 12.9634,
    "longitude": 77.5855,
    "accuracyRadius": 500,
    "timeZone": "Asia/Kolkata",
    "phoneCode": "+91",
    "connection": {
        "asn": null,
        "isp": null,
        "organization": null,
        "domain": null,
        "isHostingProvider": false,
        "isPublicProxy": false,
        "isTorExitNode": false,
        "userType": null
    },
    "security": {
        "isProxy": false,
        "isCrawler": false,
        "proxyType": null,
        "crawlerName": null
    }
}
```

## Contributing
We welcome contributions to the IP Geolocation API! Here's how you can help:

- Report bugs: If you encounter any issues with the API, please report them on the GitHub issues page.
- Suggest features: Have an idea for a new feature? Let us know by opening a new issue.
- Submit pull requests: If you've fixed a bug or implemented a new feature, you can submit a pull request. Please make sure your code follows our coding guidelines.

## Testing
We use Django's built-in test framework for testing. To run the tests, use the following command:

```shell
python manage.py test ip_geocode
```

## Contact
If you have any questions or feedback, please open an issue on GitHub or reach out to us at [hello@odyssey.co](mailto:hello@odyssey.co)

## License
The IP Geolocation API is open-source software licensed under the [MIT License]()