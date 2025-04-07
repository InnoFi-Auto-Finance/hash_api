#!/bin/bash

set -e

AWSACCOUNTID=692859937553
IMAGE_URI="$AWSACCOUNTID.dkr.ecr.us-east-1.amazonaws.com/hash-api:latest"

echo "ensure you are logged into docker"

echo "🔨 Building image..."
docker build -t hash-api .

echo "📦 Tagging image..."
docker tag hash-api:latest $IMAGE_URI

echo "🚀 Pushing image..."
docker push $IMAGE_URI


arn=$(aws apprunner list-services --query "ServiceSummaryList[*].[ServiceName,ServiceArn]" --output table | grep -F 'hash-api' | cut -d'|' -f3 | sed 's/  //g')
arn=$(echo "$arn" | xargs)
echo "detected arn ${arn}"


echo "📤 About to update App Runner service..."
while ! aws apprunner update-service \
  --service-arn "$arn" \
  --source-configuration file://source-config.json
do
  aws apprunner describe-service --service-arn "${arn}" | jq '.Service.Status'
  echo "Service is busy, retrying in 15 seconds..."
  sleep 15
done


echo "⏳ Waiting for App Runner service to reach status 'RUNNING'..."

max_wait_seconds=600   # 10 minutes
check_interval=60      # check every 60 seconds
elapsed=0

sleep $check_interval

while true; do
  status=$(aws apprunner describe-service --service-arn "$arn" | jq -r '.Service.Status')
  echo "🔁 Status: $status (elapsed: ${elapsed}s)"

  if [ "$status" == "RUNNING" ]; then
    echo "✅ Service is now RUNNING!"
    break
  fi

  if [ "$elapsed" -ge "$max_wait_seconds" ]; then
    echo "⏱ Timeout: Service did not reach 'RUNNING' within 10 minutes."
    exit 1
  fi

  sleep $check_interval
  elapsed=$((elapsed + check_interval))
done