# 🔒 MapleCMS Security Policy

This document outlines the **security standards and practices** for the MapleCMS project, ensuring safe development, deployment, and operation across all environments.

---

## 🧭 Overview

MapleCMS follows a **security-by-design** philosophy, emphasizing data protection, access control, and compliance at every level — from API endpoints to cloud infrastructure.

### Core Principles
- **Least privilege:** Each service and user gets only necessary access.
- **Defense in depth:** Multiple security layers across API, database, and network.
- **Encryption everywhere:** HTTPS, TLS, and encrypted storage.
- **Continuous monitoring:** Real-time alerting and auditing through AWS services.

---

## 🔑 1. Authentication & Authorization

### Authentication
- Implemented using **JWT (JSON Web Tokens)**.
- Tokens include user ID, role, and expiration.
- Tokens are signed with `HS256` or `RS256` (recommended for production).
- Refresh tokens (optional) allow seamless re-authentication.

**Example Payload:**
```json
{
  "sub": "user_12345",
  "role": "editor",
  "exp": 1735678900
}
```

### Authorization
- Role-based access control (**RBAC**) enforced at route level.
- Routes are grouped by role (Admin, Editor, Author, Viewer).
- Unauthorized access returns HTTP 403.

**Example:**
```python
@router.post("/articles/", dependencies=[Depends(require_role("author"))])
async def create_article(...):
    ...
```

---

## 🔐 2. Passwords & Credentials

- Passwords are hashed using **Argon2** (preferred) or **bcrypt**.
- Never store raw passwords.
- Password reset links are **time-limited** and **one-time-use**.
- API keys and service credentials are stored only in:
  - AWS Secrets Manager (prod)
  - `.env` file (local dev, ignored in Git)

### Example Hash Policy
```
password_hash = argon2.hash(user_password)
if not argon2.verify(entered_password, password_hash):
    raise HTTPException(status_code=401)
```

---

## 🧱 3. Data Protection

| Layer | Protection |
|--------|-------------|
| Database | Encrypted at rest (AWS RDS encryption) |
| Media Files | Encrypted in S3 using AES-256 SSE |
| API Traffic | HTTPS enforced with AWS ACM certificates |
| Secrets | Stored in AWS Secrets Manager |
| Backups | Encrypted and versioned automatically |

### Sensitive Fields
- `password_hash`
- `access_tokens`
- `refresh_tokens`
- `api_keys`

All sensitive fields are **never logged**, **never sent to frontend**, and **masked in debug tools**.

---

## 🧰 4. API Security

- All endpoints require HTTPS.
- CORS restricted to frontend domain(s) (`https://maplecms.com`).
- Rate limiting enabled (via Starlette middleware or AWS API Gateway if extended).
- Input validation enforced via **Pydantic** schemas.
- Output filtering: only return safe, public fields.

**Example:**
```python
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
```

---

## 🪣 5. File Upload Security

- Validate MIME type and file extension before upload.
- Reject executable files or scripts.
- Sanitize filenames (remove spaces/special characters).
- Upload directly to AWS S3 via presigned URLs.
- Use **signed URLs** for temporary access to private files.

**Example:**
```python
s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'maplecms-assets', 'Key': 'uploads/article1.png'},
    ExpiresIn=3600
)
```

---

## ☁️ 6. AWS Infrastructure Security

- **ECS Services:** run in private subnets with public access only via ALB.
- **Security Groups:** allow minimal inbound/outbound traffic.
- **IAM Roles:** use fine-grained policies for ECS tasks and Lambda functions.
- **CloudWatch Alerts:** for login failures, traffic spikes, or CPU anomalies.
- **CloudTrail Logs:** for full API auditing and compliance.

### Example IAM Policy (ECR Pull Access)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ecr:GetAuthorizationToken", "ecr:BatchGetImage"],
      "Resource": "*"
    }
  ]
}
```

---

## 🧪 7. Security Testing

- **Static Analysis:** ruff, flake8, bandit
- **Dependency Scanning:** `pip-audit`, `npm audit`
- **Penetration Testing:** optional quarterly manual review
- **CI/CD Checks:** automatic scans via GitHub Actions security workflows

---

## 🧮 8. Incident Response

1. Detect issue (via CloudWatch alert or user report)
2. Contain: isolate affected ECS service
3. Investigate logs (CloudTrail + ECS task output)
4. Rotate affected secrets/keys
5. Patch vulnerability
6. Document incident in `SECURITY.md`

---

## 🧭 9. Compliance & Privacy

- GDPR & PIPEDA-friendly: only essential user data collected.
- All user data deletable upon request.
- Data access logs retained for 90 days.
- Backups stored in encrypted S3 with versioning enabled.

---

## 🧾 10. Security Checklist (Pre-Release)
✅ HTTPS enforced for all endpoints  
✅ JWT secrets stored in AWS Secrets Manager  
✅ Argon2 password hashing verified  
✅ Database encryption enabled  
✅ IAM roles reviewed for least privilege  
✅ CORS origins whitelisted  
✅ CloudWatch + CloudTrail logging active

---

> MapleCMS is designed for **trust and transparency** — every request, credential, and file is protected by multiple layers of security from edge to database.
