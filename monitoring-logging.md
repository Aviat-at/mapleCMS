# 📊 MapleCMS Monitoring & Logging Guide

This guide explains how to monitor, log, and visualize the performance of MapleCMS using **AWS CloudWatch**, **ECS logging**, and optional **Grafana dashboards**.  
The goal is to maintain observability across both the FastAPI backend and Next.js frontend services.

---

## 🧭 Overview

### Monitoring Layers
| Layer | Service | Purpose |
|--------|----------|----------|
| Application | FastAPI + Next.js | Request performance, errors, response times |
| Infrastructure | ECS, RDS, S3 | Container health, CPU/memory, DB performance |
| Network | CloudFront + ALB | Latency, throughput, connection errors |
| Logs | CloudWatch Logs | Centralized log aggregation |

---

## ⚙️ 1. AWS CloudWatch Setup

### ECS Container Logging
Each container (frontend + backend) streams logs to CloudWatch via AWS Logs driver.

**`task_definition.json` (excerpt):**
```json
"logConfiguration": {
  "logDriver": "awslogs",
  "options": {
    "awslogs-group": "/ecs/maplecms",
    "awslogs-region": "us-east-1",
    "awslogs-stream-prefix": "ecs"
  }
}
```

### Log Groups
| Service | Log Group |
|----------|------------|
| Backend (FastAPI) | `/ecs/maplecms-backend` |
| Frontend (Next.js) | `/ecs/maplecms-frontend` |
| Database (RDS) | `/aws/rds/instance/maplecms/postgresql` |

All log groups retain data for **30 days** (configurable).

---

## 🧾 2. Application Metrics

### FastAPI Custom Metrics
You can expose Prometheus metrics or custom CloudWatch metrics from FastAPI using **boto3** or **aioboto3**.

**Example:**
```python
import boto3
import time

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def record_api_latency(route: str, latency_ms: float):
    cloudwatch.put_metric_data(
        Namespace='MapleCMS/API',
        MetricData=[{
            'MetricName': 'RequestLatency',
            'Dimensions': [{'Name': 'Route', 'Value': route}],
            'Value': latency_ms,
            'Unit': 'Milliseconds'
        }]
    )
```

This allows dashboards to track:
- API latency per route
- Request counts per minute
- Error rates (4xx / 5xx)

---

### ECS Service Metrics
CloudWatch automatically collects:
- CPUUtilization
- MemoryUtilization
- NetworkIn / NetworkOut
- Task Count (Running / Desired)

Use these metrics to trigger autoscaling or alerts.

### RDS Metrics
Monitored via `AWS/RDS` namespace:
- CPUUtilization
- DatabaseConnections
- FreeStorageSpace
- ReadIOPS / WriteIOPS

---

## 🔔 3. Alerts & Notifications

Create CloudWatch Alarms for key metrics.

### Example Alarms
| Metric | Threshold | Action |
|---------|------------|--------|
| ECS CPUUtilization | > 80% for 5 mins | Scale out + send SNS alert |
| ECS MemoryUtilization | > 75% | Investigate memory leak |
| RDS FreeStorageSpace | < 2 GB | Alert for DB maintenance |
| API Error Rate | > 5% | Send developer alert |

**SNS Topics:**
- `maplecms-alerts-dev` → Email, Slack, or Lambda webhook

**Example Terraform (Alarm + SNS):**
```hcl
resource "aws_cloudwatch_metric_alarm" "ecs_high_cpu" {
  alarm_name          = "maplecms-ecs-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "High CPU usage on MapleCMS ECS service"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions = {
    ClusterName = var.ecs_cluster_name
  }
}
```

---

## 🧠 4. Optional — Grafana Dashboard

### Setup
You can connect **Amazon Managed Grafana** or a self-hosted Grafana instance to CloudWatch.

**Recommended Dashboards:**
- API request latency (MapleCMS/API namespace)
- ECS service CPU and memory trends
- RDS performance metrics
- CloudFront latency & error rate

**Sample Query:**
```
Namespace: MapleCMS/API
Metric: RequestLatency
Dimension: Route
Statistic: Average
```

Grafana visualizations can be embedded in the MapleCMS admin dashboard in future releases.

---

## 🧩 5. Frontend Logging (Next.js)

Use a centralized logger for frontend events:
```ts
export const logClientEvent = async (message: string, data?: any) => {
  await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs/frontend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, data, timestamp: new Date().toISOString() }),
  });
};
```

FastAPI receives and stores these logs in CloudWatch under `/ecs/maplecms-frontend`.

---

## 🔐 6. Security & Access Control
- CloudWatch access restricted via IAM roles.
- Logs encrypted at rest (KMS-managed keys).
- Only admins can view production logs.
- Alarms routed through verified SNS topics.

---

## 🚀 7. Local & Dev Monitoring
For local development:
- Use `uvicorn --reload --log-level debug` for FastAPI logs.
- Use `next dev` with browser console for frontend.
- Optional: integrate **Prometheus + Grafana Docker** stack for local insights.

**Docker Compose Example:**
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - 9090:9090
  grafana:
    image: grafana/grafana
    ports:
      - 3001:3000
```

---

## 🧭 Summary
- Centralized logs and metrics in **CloudWatch**.
- Alerts via **SNS** and autoscaling triggers.
- Optional **Grafana dashboards** for deep observability.
- Secure, role-based access to all monitoring data.

> MapleCMS monitoring ensures full visibility — from API latency to ECS performance — keeping deployments reliable, measurable, and secure.
