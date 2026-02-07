from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.cookiejar import CookieJar
from typing import Any, Optional


@dataclass(frozen=True)
class HttpResult:
    status: int
    headers: dict[str, str]
    body_text: str
    body_json: Optional[Any]


def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _safe_json_loads(s: str) -> Optional[Any]:
    try:
        return json.loads(s)
    except Exception:
        return None


def _print_section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def _get_cookie_value(jar: CookieJar, name: str) -> Optional[str]:
    for c in jar:
        if c.name == name:
            return c.value
    return None


def _parse_set_cookie_session_id(set_cookie: Optional[str]) -> Optional[str]:
    if not set_cookie:
        return None
    parts = [p.strip() for p in set_cookie.split(";")]
    for p in parts:
        if p.startswith("session_id="):
            return p.split("=", 1)[1]
    return None


def http_json(
    opener: urllib.request.OpenerDirector,
    method: str,
    url: str,
    json_body: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
) -> HttpResult:
    data = None
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)

    if json_body is not None:
        raw = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        data = raw
        req_headers["Content-Type"] = "application/json; charset=utf-8"

    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=req_headers)

    print(f"[{_now()}] REQ {req.method} {url}")
    if json_body is not None:
        print(f"  json: {json.dumps(json_body, ensure_ascii=False)}")

    try:
        with opener.open(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            headers_dict = {k: v for k, v in resp.headers.items()}
            body_json = _safe_json_loads(body)
            print(f"[{_now()}] RESP {resp.status}")
            if body_json is not None:
                print(f"  json: {json.dumps(body_json, ensure_ascii=False)}")
            else:
                print(f"  body: {body}")
            return HttpResult(resp.status, headers_dict, body, body_json)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        headers_dict = {k: v for k, v in (e.headers.items() if e.headers else [])}
        body_json = _safe_json_loads(body) if body else None
        print(f"[{_now()}] RESP {e.code} (HTTPError)")
        if body_json is not None:
            print(f"  json: {json.dumps(body_json, ensure_ascii=False)}")
        elif body:
            print(f"  body: {body}")
        return HttpResult(int(e.code), headers_dict, body, body_json)


def main(argv: list[str]) -> int:
    base_url = "http://127.0.0.1:8000/api/users"
    if len(argv) >= 2:
        base_url = argv[1]

    _print_section("CONFIG")
    print(f"[{_now()}] base_url: {base_url}")

    jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    _print_section("LOGIN (mentor id=1 expected)")
    login_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", "login")
    login_result = http_json(
        opener=opener,
        method="POST",
        url=login_url,
        json_body={"email": "mentor@test.com", "password": "1234", "role": "mentor"},
    )

    session_id = _get_cookie_value(jar, "session_id") or _parse_set_cookie_session_id(
        login_result.headers.get("Set-Cookie")
    )
    print(f"[{_now()}] cookie session_id: {session_id!r}")

    _print_section("GET /mentee")
    mentee_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", "mentee")
    headers = {"Cookie": f"session_id={session_id}"} if session_id else None
    _ = http_json(opener=opener, method="GET", url=mentee_url, headers=headers)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

