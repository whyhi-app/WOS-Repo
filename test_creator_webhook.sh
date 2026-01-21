#!/bin/bash
# Test the creator capture webhook

echo "Testing webhook with sample URL..."
curl -X POST "https://n8n.whyhi.app/webhook/wos/intent/creator_capture_v0" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://twitter.com/elonmusk"}' \
  --max-time 30
