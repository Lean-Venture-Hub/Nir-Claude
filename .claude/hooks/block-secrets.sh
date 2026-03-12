#!/bin/bash
# Block writes to .env, secrets, and credential files
# Hook type: PreToolUse (Edit, Write)

INPUT=$(cat)
TOOL_NAME="$TOOL_NAME"

if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    FILE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)
    if [[ "$FILE" == *".env"* || "$FILE" == *"secrets"* || "$FILE" == *"credentials"* || "$FILE" == *".pem"* ]]; then
        echo '{"decision": "block", "reason": "Cannot write to secrets/credentials files (.env, .pem, secrets/)"}'
        exit 0
    fi
fi
echo '{"decision": "approve"}'
exit 0
