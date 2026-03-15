#!/bin/bash
# Deploy feedback API to EC2 server
# Run from project root: bash feedback-api/deploy.sh

set -e
SSH="ssh -i ~/.ssh/test_env_ec2.pem ubuntu@18.184.97.242"
SCP="scp -i ~/.ssh/test_env_ec2.pem"

echo "=== 1. Install Flask ==="
$SSH "sudo pip3 install flask 2>/dev/null || sudo apt-get install -y python3-flask"

echo "=== 2. Deploy API code ==="
$SSH "sudo mkdir -p /opt/feedback-api && sudo chown ubuntu:ubuntu /opt/feedback-api"
$SCP feedback-api/app.py ubuntu@18.184.97.242:/opt/feedback-api/app.py

echo "=== 3. Create feedback data directory ==="
$SSH "sudo mkdir -p /var/www/lp.scalefox.ai/feedback && sudo chown www-data:www-data /var/www/lp.scalefox.ai/feedback && sudo chmod 755 /var/www/lp.scalefox.ai/feedback"

echo "=== 4. Install systemd service ==="
$SCP feedback-api/feedback-api.service ubuntu@18.184.97.242:/tmp/feedback-api.service
$SSH "sudo mv /tmp/feedback-api.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable feedback-api && sudo systemctl restart feedback-api"

echo "=== 5. Add nginx proxy (if not already configured) ==="
$SSH "sudo grep -q 'location /api/' /etc/nginx/sites-available/lp.scalefox.ai || sudo sed -i '/server_name/a\\n    location /api/ {\n        proxy_pass http://127.0.0.1:5111/api/;\n        proxy_set_header Host \$host;\n        proxy_set_header X-Real-IP \$remote_addr;\n        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;\n    }' /etc/nginx/sites-available/lp.scalefox.ai && sudo nginx -t && sudo systemctl reload nginx"

echo "=== 6. Verify ==="
sleep 2
$SSH "curl -s http://127.0.0.1:5111/api/feedback/health"
echo ""
echo "=== Done! Test: curl https://lp.scalefox.ai/api/feedback/health ==="
