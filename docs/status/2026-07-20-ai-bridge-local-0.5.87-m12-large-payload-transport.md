# AI Bridge Local 0.5.87 - M12 large payload transport

Date: 2026-07-20

## Authoritative scope

M12 implements safe transport for large command payloads.

## Baseline

- Base commit: `6cedadd90031fb3ad88d8e51cfcff0d1b5e702c5`
- Base release: `0.5.86`
- Target release: `0.5.87`

## Existing foundation

Before M12, the compact command plane already provided:

- `POST /v1/payloads`;
- SHA-256 durable payload references;
- an inline argument limit of 32768 bytes;
- payload expiration and validation;
- execution-time payload loading and JSON merge.

## M12 change

The browser background service now:

- preserves the original inline path for small argument objects;
- measures the UTF-8 byte length of serialized `args`;
- uploads larger JSON argument objects through `/v1/payloads`;
- submits the command with empty inline arguments and `payload_ref`;
- passes through commands that already contain a payload reference.

## Explicit exclusions

- Control Center v2 functional work;
- payload-reference support in the legacy gateway;
- payload-reference persistence in the legacy queue;
- payload-reference resolution in Brain Worker;
- replacement of command-plane payload storage.

## Validation

Source validation includes:

- JavaScript syntax checks;
- Python compilation;
- Node behavioral smoke;
- command-plane durable payload round trip;
- active version-literal checks;
- complete pytest suite;
- exact Git allowlist validation;
- preservation of the running 0.5.86 processes until publication.
