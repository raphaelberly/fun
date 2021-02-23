# Filmotheque

The purpose of this program is to scrape the website of the "Filmotheque du Quartier Latin", a movie theater located in 
Paris, and to send the weekly program to a list of specified emails.

## Usage

### Requirements

To use the program, you need to have a python 3 environment with meeting the requirements listed in the file
`requirements.txt`.

There also needs to be a `credentials.yaml` file in the `conf/` folder, in the following format:

```yaml
payload:
  Messages:
    - From:
        Email: x@y.z
        Name: X
      To:
        - Email: x@y.z
          Name: X
```

Finally, there needs to be a `mailer.yaml` file in the `conf/` folder, in the following format:

```yaml
api_key: XXXXXXX
secret_key: XXXXXXX
```

### Command

Once requirements are met, run the program by running the following command: `python main.py`
