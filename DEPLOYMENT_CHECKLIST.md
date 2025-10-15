# Deployment Checklist

Use this checklist to ensure a smooth deployment of the Zibtek AI Chatbot.

## Pre-Deployment

### 1. Environment Setup

- [ ] Obtain OpenAI API key with sufficient credits
- [ ] Create `.env` file from `backend/env.template`
- [ ] Set `OPENAI_API_KEY` in `.env`
- [ ] Configure `CORS_ORIGINS` for production domain
- [ ] Review and adjust RAG parameters (chunk size, similarity threshold)

### 2. Code Review

- [ ] Review all configuration in `backend/app/core/config.py`
- [ ] Verify security settings in `backend/app/core/security.py`
- [ ] Check system prompts in `backend/app/services/langchain_rag.py`
- [ ] Ensure proper error handling in all endpoints

### 3. Testing

- [ ] Run all tests from `TESTING.md`
- [ ] Test prompt injection protection
- [ ] Verify out-of-scope question handling
- [ ] Test multi-turn conversation flow
- [ ] Check conversation management (create, load, delete)
- [ ] Verify all API endpoints work correctly
- [ ] Test error scenarios (invalid input, API failures)

### 4. Docker Preparation

- [ ] Ensure Docker and Docker Compose are installed
- [ ] Review `docker-compose.yml` for production settings
- [ ] Check resource limits in Docker configurations
- [ ] Verify port mappings don't conflict

## Deployment Steps

### 5. Initial Deployment

- [ ] Clone repository to production server
- [ ] Create production `.env` file
- [ ] Build containers: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Monitor logs: `docker-compose logs -f`
- [ ] Wait for data ingestion to complete (5-10 minutes)

### 6. Verification

- [ ] Check all containers are running: `docker-compose ps`
- [ ] Verify backend health: `curl http://localhost:8000/health`
- [ ] Check Qdrant collection exists: Visit dashboard at `:6333/dashboard`
- [ ] Test frontend loads: Visit `http://localhost:3000`
- [ ] Send test query and verify response

### 7. Production Configuration

#### Reverse Proxy (nginx example)

- [ ] Install nginx
- [ ] Configure SSL certificate (Let's Encrypt)
- [ ] Set up proxy to backend on port 8000
- [ ] Set up proxy to frontend on port 3000
- [ ] Enable HTTPS redirect
- [ ] Configure rate limiting

Example nginx config:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Environment Variables for Production

- [ ] Update `CORS_ORIGINS` to production domain
- [ ] Set `NEXT_PUBLIC_API_URL` to production API URL
- [ ] Consider using `gpt-4` for better responses (higher cost)
- [ ] Adjust `SIMILARITY_THRESHOLD` based on testing

### 8. Security Hardening

- [ ] Enable firewall (UFW/iptables)
- [ ] Restrict access to ports 6333, 6334 (Qdrant)
- [ ] Set up fail2ban for brute force protection
- [ ] Configure Docker security options
- [ ] Enable Docker logging driver
- [ ] Set up intrusion detection (optional)
- [ ] Regular security updates: `apt update && apt upgrade`

### 9. Monitoring Setup

- [ ] Set up log rotation for Docker logs
- [ ] Configure monitoring (Prometheus/Grafana optional)
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure error alerting
- [ ] Monitor OpenAI API usage and costs
- [ ] Track response times
- [ ] Monitor disk space for logs and database

### 10. Backup Strategy

- [ ] Set up automated backups for SQLite database
- [ ] Backup Qdrant volume data
- [ ] Store `.env` file securely (encrypted)
- [ ] Document backup restoration procedure
- [ ] Test backup restoration process

Example backup script:

```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup SQLite
cp backend/data/chatbot.db $BACKUP_DIR/chatbot_$DATE.db

# Backup Qdrant
docker run --rm \
  -v qdrant_data:/qdrant/storage \
  -v $BACKUP_DIR:/backup \
  qdrant/qdrant \
  tar czf /backup/qdrant_$DATE.tar.gz -C /qdrant/storage .

# Keep only last 7 days
find $BACKUP_DIR -mtime +7 -delete
```

## Post-Deployment

### 11. Smoke Tests

- [ ] Create a new conversation
- [ ] Send valid Zibtek questions
- [ ] Send out-of-scope questions
- [ ] Test prompt injection attempts
- [ ] Load previous conversations
- [ ] Delete a conversation
- [ ] Check query logs in database

### 12. Performance Optimization

- [ ] Monitor response times
- [ ] Check Docker resource usage
- [ ] Optimize database queries if needed
- [ ] Adjust `TOP_K_RESULTS` for performance vs accuracy
- [ ] Consider caching frequently asked questions
- [ ] Monitor Qdrant performance

### 13. Documentation

- [ ] Document production URL and credentials
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures
- [ ] Create incident response plan
- [ ] Document scaling procedures
- [ ] Update team on deployment

### 14. User Acceptance Testing

- [ ] Have stakeholders test the system
- [ ] Collect feedback on responses
- [ ] Verify response accuracy
- [ ] Check UI/UX on different devices
- [ ] Test on different browsers
- [ ] Verify mobile responsiveness

## Maintenance Schedule

### Daily

- [ ] Check uptime status
- [ ] Monitor error logs
- [ ] Check OpenAI API usage

### Weekly

- [ ] Review query logs for improvements
- [ ] Check disk space
- [ ] Review response quality
- [ ] Monitor costs

### Monthly

- [ ] Update dependencies (security patches)
- [ ] Review and optimize system prompts
- [ ] Analyze user queries for patterns
- [ ] Update Zibtek website data (re-scrape)
- [ ] Review and rotate logs
- [ ] Check backup integrity

### Quarterly

- [ ] Full security audit
- [ ] Performance optimization review
- [ ] Consider model upgrades (GPT-4, new embeddings)
- [ ] Review and update documentation
- [ ] Disaster recovery drill

## Rollback Plan

### If Deployment Fails

1. Stop new services:

   ```bash
   docker-compose down
   ```

2. Restore from backup:

   ```bash
   cp /backups/chatbot_LATEST.db backend/data/chatbot.db
   ```

3. Start previous version:

   ```bash
   git checkout <previous-tag>
   docker-compose up -d
   ```

4. Verify services are running
5. Investigate and fix issues
6. Plan re-deployment

## Troubleshooting

### Common Issues

#### Container won't start

```bash
# Check logs
docker-compose logs backend

# Common fixes:
- Verify .env file exists and is valid
- Check port conflicts
- Ensure Docker has sufficient resources
```

#### Data ingestion fails

```bash
# Check if website is accessible
curl https://www.zibtek.com

# Manual re-run
docker-compose exec backend python -m app.ingest_data
```

#### Frontend can't reach backend

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in .env
# Update NEXT_PUBLIC_API_URL if needed
```

## Production-Specific Settings

### Docker Compose for Production

Consider adding to `docker-compose.yml`:

```yaml
services:
  backend:
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 4G
```

### Environment Variables

```env
# Production settings
OPENAI_MODEL=gpt-4  # Better quality
CHUNK_SIZE=800      # Smaller for better precision
TOP_K_RESULTS=3     # Fewer for faster responses
SIMILARITY_THRESHOLD=0.75  # Higher for more accuracy
```

## Success Criteria

Deployment is successful when:

- [ ] All containers running stable for 24 hours
- [ ] No critical errors in logs
- [ ] Response time < 5 seconds average
- [ ] 100% uptime over monitoring period
- [ ] All security checks pass
- [ ] Backups completing successfully
- [ ] User acceptance tests pass
- [ ] Cost within budget

## Contact & Escalation

### For Issues:

1. Check logs: `docker-compose logs`
2. Review documentation
3. Check GitHub issues (if applicable)
4. Contact system administrator
5. Contact OpenAI support (API issues)

### Emergency Contacts:

- DevOps Team: [contact info]
- OpenAI Support: https://help.openai.com
- Qdrant Support: https://qdrant.tech/documentation

---

**Deployment Date**: ******\_\_\_******  
**Deployed By**: ******\_\_\_******  
**Verified By**: ******\_\_\_******  
**Production URL**: ******\_\_\_******

## Sign-off

- [ ] Development Team Lead
- [ ] QA Team Lead
- [ ] DevOps Engineer
- [ ] Product Owner
- [ ] Security Officer

