#!/usr/bin/env python3
"""Check HTTP status codes for a list of URLs.

Usage:
    python3 main.py https://example.com https://httpstat.us/404
    python3 main.py --file urls.txt
    echo "https://example.com" | python3 main.py --stdin
"""
import argparse
import sys
import urllib.error
import urllib.request


def check_url(url, timeout, method="HEAD"):
    """Return (status_code, reason) for a URL, following redirects."""
    request = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.reason
    except urllib.error.HTTPError as exc:
        # HTTPError still carries the real status code (404, 500, ...).
        if method == "HEAD" and exc.code in (405, 501):
            return check_url(url, timeout, method="GET")
        return exc.code, exc.reason
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except (TimeoutError, ValueError) as exc:
        return None, str(exc)


def collect_urls(args):
    urls = list(args.urls)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            urls.extend(line.strip() for line in handle if line.strip())
    if args.stdin:
        urls.extend(line.strip() for line in sys.stdin if line.strip())
    # Normalise bare hostnames to https:// URLs.
    return [u if "://" in u else "https://" + u for u in urls]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check HTTP status codes for a list of URLs.")
    parser.add_argument("urls", nargs="*", help="URL(s) to check")
    parser.add_argument("--file", "-f", help="file with one URL per line")
    parser.add_argument("--stdin", action="store_true",
                        help="read URLs from standard input")
    parser.add_argument("--timeout", type=float, default=10,
                        help="request timeout in seconds (default: 10)")
    parser.add_argument("--method", default="HEAD", choices=["HEAD", "GET"],
                        help="HTTP method to use (default: HEAD)")
    args = parser.parse_args(argv)

    urls = collect_urls(args)
    if not urls:
        parser.error("no URLs given (pass URLs, --file, or --stdin)")

    failures = 0
    for url in urls:
        status, reason = check_url(url, args.timeout, args.method)
        if status is None:
            print(f"{url} -> ERROR: {reason}")
            failures += 1
        else:
            print(f"{url} -> {status} {reason}")
            if status >= 400:
                failures += 1
    if failures:
        print(f"\n{failures} of {len(urls)} URL(s) failed or returned an error status.",
              file=sys.stderr)
    return 1 if failures == len(urls) else 0


if __name__ == "__main__":
    raise SystemExit(main())
