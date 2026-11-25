# HTTP Status Checker

Check HTTP status codes for a list of URLs.

## Requirements

- Python 3 (standard library only — no extra packages)

## Usage

```bash
python3 main.py https://example.com https://httpstat.us/404
python3 main.py --file urls.txt
echo "https://example.com" | python3 main.py --stdin
```

Options:

- `urls` — one or more URLs to check (bare hostnames get `https://` added)
- `--file, -f FILE` — file with one URL per line
- `--stdin` — read URLs from standard input
- `--timeout SECONDS` — request timeout (default: 10)
- `--method {HEAD,GET}` — HTTP method to use (default: HEAD)

## Example

```bash
$ python3 main.py https://example.com https://httpstat.us/404
https://example.com -> 200 OK
https://httpstat.us/404 -> 404 Not Found
```

The exit code is 0 unless every URL failed or returned an error status.
HTTP errors such as 404 are reported with their real status code, and
network failures are reported as `ERROR` instead of crashing.
