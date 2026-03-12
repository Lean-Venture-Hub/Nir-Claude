#!/bin/bash
# Prompt for confirmation before EC2 SSH/SCP commands
# Hook type: PreToolUse (Bash)

INPUT=$(cat)
TOOL_NAME="$TOOL_NAME"

if [[ "$TOOL_NAME" == "Bash" ]]; then
    CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null)
    if [[ "$CMD" == *"ssh"*"ec2"* ]] || [[ "$CMD" == *"scp"*".pem"* ]] || [[ "$CMD" == *"ssh"*".pem"* ]]; then
        echo '{"decision": "ask", "reason": "This command accesses a remote EC2 server. Please confirm."}'
        exit 0
    fi
fi
echo '{"decision": "approve"}'
exit 0
