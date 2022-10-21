# RXLS
Read .xlsx spreadsheets and convert each row of data into a REST call to ServiceNow. This tool can read any sheet with the following format:

| Col 1 | Col 2 | Col 3 |

| data 1.1 | data 1.2 | data 1.3 |

| data 2.1 | data 2.2 | data 2.3 |

...

The spreadsheet above is converted to the following:

`POST /api/someendpoint`
```json
{
    "Col 1": "data 1.1",
    "Col 2": "data 1.2",
    "Col 3": "data 1.3"
}
```
`POST /api/someendpoint`
```json
{
    "Col 1": "data 2.1",
    "Col 2": "data 2.2",
    "Col 3": "data 2.3"
}
```
## Installation
Download the lastest .whl or .tar.gz file found in the Releases section.

Install it with pip:

`pip3 install dist/rxls-1.0.0-py3-none-any.whl`

The command should now be accessible using `rxls`. Type `rxls -h` for usage details. See Configuration below before running other commands.

## Configuration
The requests made to ServiceNow reference a file called `connection.conf`. This file  must include the following information:

- Section name: This is the environment/instance name of ServiceNow to connect to. Specify a new section for each connection you wish to store and reference later.
- verb: One of the following: POST, PUT, PATCH, GET, DELETE. Assumed POST if "verb" is not present in the config file.
- endpoint: The REST endpoint you are reaching out to with this connection. Do not include anything before "...service-now.com".
- user: The username of the user who will be making the requests.
- pass The password of the user who will be making the requests.

Example:
```ini
[myclientdev]
verb = POST
endpoint = /api/sn_customerservice/myspecialapi/create
user = myuser.name
pass = my super secret password

[myclienttest]
verb = POST
endpoint = /api/sn_customerservice/myspecialapi/create
user = myuser.name
pass = my super secret password

[myclientprod]
verb = POST
endpoint = /api/sn_customerservice/myspecialapi/create
user = myuser.name
pass = my super secret password
```

Please ensure that the `connection.conf` file is stored in the same location as the spreadsheets.

## Example Usage

Get help about usage:

`rxls -h`

Sends all rows as requests to the environment "myclientdev" specified in `connection.conf`:

`rxls -i test.xlsx -e myclientdev`

Sends four rows of data, skipping the first two (including the header). In other words, starts on row 3:

`rxls -i test.xlsx -e myclientdev -r 2:4`

## Building
Make sure the latest version of PyPA's build is installed:

`python3 -m pip install --upgrade build`

Run the following to build:

`python3 -m build`

This will create a `dist/` folder with the corresponding new release.
