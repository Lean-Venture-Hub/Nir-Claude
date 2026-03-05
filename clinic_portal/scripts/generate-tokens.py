#!/usr/bin/env python3
"""Generate tokens.json mapping magic-link tokens to clinic IDs for 439 clinics."""
import json
import hashlib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'dashboard_admin', 'data')
OUTPUT_PATH = os.path.join(DATA_DIR, 'tokens.json')

SECRET = 'clinic-portal-2026'  # Simple seed for deterministic tokens

tokens = {}
for clinic_id in range(1, 440):
    raw = f'{SECRET}-{clinic_id}'
    token = hashlib.sha256(raw.encode()).hexdigest()[:24]
    tokens[token] = clinic_id

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(tokens, f, indent=2)

print(f'Generated {len(tokens)} tokens → {OUTPUT_PATH}')
print(f'Example: clinic 1 → token {list(tokens.keys())[0]}')
print(f'  URL: /clinic/{list(tokens.keys())[0]}')
