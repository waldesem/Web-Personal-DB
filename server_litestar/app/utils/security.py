"""Security module."""

from __future__ import annotations

import hashlib
import hmac
import secrets

from constants import DEFAULT_PASSWORD

"""https://github.com/pallets/werkzeug/blob/main/src/werkzeug/security.py"""

SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_PBKDF2_ITERATIONS = 1_000_000


def gen_salt(length: int) -> str:
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if length <= 0:
        msg = "Salt length must be at least 1."
        raise ValueError(msg)

    return "".join(secrets.choice(SALT_CHARS) for _ in range(length))


def _hash_internal(method: str, salt: str, password: str) -> tuple[str, str]:
    method, *args = method.split(":")
    salt_bytes = salt.encode()
    password_bytes = password.encode()

    if method == "scrypt":
        if not args:
            n = 2**15
            r = 8
            p = 1
        else:
            try:
                n, r, p = map(int, args)
            except ValueError:
                msg = "'scrypt' takes 3 arguments."
                raise ValueError(msg) from None

        maxmem = 132 * n * r * p  # ideally 128, but some extra seems needed
        return (
            hashlib.scrypt(
                password_bytes,
                salt=salt_bytes,
                n=n,
                r=r,
                p=p,
                maxmem=maxmem,
            ).hex(),
            f"scrypt:{n}:{r}:{p}",
        )
    if method == "pbkdf2":
        len_args = len(args)

        if len_args == 0:
            hash_name = "sha256"
            iterations = DEFAULT_PBKDF2_ITERATIONS
        elif len_args == 1:
            hash_name = args[0]
            iterations = DEFAULT_PBKDF2_ITERATIONS
        elif len_args == 2:
            hash_name = args[0]
            iterations = int(args[1])
        else:
            msg = "'pbkdf2' takes 2 arguments."
            raise ValueError(msg)

        return (
            hashlib.pbkdf2_hmac(
                hash_name,
                password_bytes,
                salt_bytes,
                iterations,
            ).hex(),
            f"pbkdf2:{hash_name}:{iterations}",
        )
    msg = f"Invalid hash method '{method}'."
    raise ValueError(msg)


def generate_password_hash(
    password: str = DEFAULT_PASSWORD,
    method: str = "scrypt",
    salt_length: int = 16,
) -> str:
    """Securely hash a password for storage."""
    salt = gen_salt(salt_length)
    h, actual_method = _hash_internal(method, salt, password)
    return f"{actual_method}${salt}${h}"


def check_password_hash(pwhash: str, password: str) -> bool:
    """Securely check that the given stored password hash."""
    try:
        method, salt, hashval = pwhash.split("$", 2)
    except ValueError:
        return False

    return hmac.compare_digest(_hash_internal(method, salt, password)[0], hashval)
