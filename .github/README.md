# GitHub Actions CI/CD Setup Complete! 🎉

This project now includes automated GitHub Actions workflows for building and pushing Docker images to Docker Hub and optional private registries.

## Quick Start (5 minutes)

### 1. Add Docker Hub Credentials to GitHub

**Option A: Using GitHub Web UI**
1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these secrets:
   - `DOCKER_HUB_USERNAME` = your Docker Hub username
   - `DOCKER_HUB_PASSWORD` = your Docker Hub Personal Access Token

> **Get Docker Hub Token:** Go to hub.docker.com/settings/security → Create token

**Option B: Using GitHub CLI**
```bash
# Install GitHub CLI from https://cli.github.com

# Login to GitHub
gh auth login

# Run setup script
# On Windows:
.\.github\setup-secrets.bat

# On Linux/Mac:
chmod +x .github/setup-secrets.sh
./.github/setup-secrets.sh
```

### 2. Enable Workflow Permissions

1. Settings → Actions → General
2. Select "Read and write permissions"
3. ✅ "Allow GitHub Actions to create and approve pull requests"

### 3. Push to Trigger Build

```bash
git commit --allow-empty -m "Trigger CI/CD"
git push
```

✅ Done! Watch your build in the **Actions** tab.

---

## Workflow Files

| File | Purpose | Trigger |
|------|---------|---------|
| `build-and-push.yml` | Build and push to Docker Hub | Push to main/develop, manual |
| `pull-request.yml` | Validate PR builds | Pull requests |
| `security-scan.yml` | Scan for vulnerabilities | Daily + manual |
| `deploy.yml` | Deploy services | After successful build |

---

## What Gets Built

Each service gets its own Docker image with automatic tags:

```
docker.io/your-username/nagp-auth-service:latest
docker.io/your-username/nagp-cart-service:main
docker.io/your-username/nagp-order-service:develop
docker.io/your-username/nagp-product-service:abc1234
docker.io/your-username/nagp-frontend:v1.0.0
```

**Services:**
- ✅ Auth Service (port 8000)
- ✅ Product Service (port 8001)
- ✅ Cart Service (port 8002)
- ✅ Order Service (port 8003)
- ✅ Frontend (port 3000)

---

## Documentation

- **[CI/CD Guide](./.github/CI-CD-GUIDE.md)** - Complete workflow documentation
- **[GitHub Secrets Setup](./.github/SECRETS.md)** - How to add credentials
- **[Private Registry Options](./.github/PRIVATE-REGISTRY-SETUP.md)** - Azure, AWS, GCP, Self-Hosted

---

## Manual Workflow Triggers

To manually trigger a workflow:

1. Go to **Actions** tab
2. Select the workflow
3. Click **"Run workflow"**
4. Choose branch and click **"Run workflow"**

---

## Monitoring

### View Build Logs
1. Actions tab → Select workflow run → Click job → View logs

### View Built Images
```bash
docker search your-username/nagp
docker pull your-username/nagp-auth-service:latest
```

### Security Reports
Go to Security → Vulnerabilities to view Trivy scan results

---

## Environment Variables

Update these in docker-compose.yml after pushing to Docker Hub:

```yaml
services:
  auth-service:
    image: your-username/nagp-auth-service:latest
    
  product-service:
    image: your-username/nagp-product-service:latest
    
  cart-service:
    image: your-username/nagp-cart-service:latest
    
  order-service:
    image: your-username/nagp-order-service:latest
    
  frontend:
    image: your-username/nagp-frontend:latest
```

---

## Troubleshooting

### Build Fails
```bash
# Check logs in Actions tab
# Common issues:
# - Invalid Dockerfile
# - Missing dependencies
# - Python version mismatch
```

### Push Fails
```bash
# Verify credentials:
# - Correct Docker Hub username
# - Valid Personal Access Token (not password)
# - Token not expired
```

### Images Not Appearing
- Wait 1-2 minutes for Docker Hub to update
- Verify secrets are set correctly
- Check GitHub Actions logs for errors

---

## Best Practices

1. **Use Semantic Versioning**
   ```bash
   git tag v1.0.0
   git push --tags
   ```

2. **Add Branch Protection Rules**
   - Settings → Branches → Add rule
   - Require status checks to pass

3. **Monitor Image Size**
   - Use Alpine Linux for smaller images
   - Multi-stage builds reduce size
   - Remove build dependencies

4. **Keep Dependencies Updated**
   - Security scans run daily
   - Review and fix vulnerabilities
   - Update requirements.txt regularly

5. **Document Your Setup**
   - Keep CI/CD guide updated
   - Document custom environment variables
   - Share credentials securely

---

## Next Steps

### Recommended
- [ ] Setup Docker Hub account
- [ ] Add GitHub secrets
- [ ] Enable workflow permissions
- [ ] Make first commit to trigger build
- [ ] Verify images on Docker Hub

### Advanced
- [ ] Setup private registry (ACR/ECR/GCR)
- [ ] Configure automatic deployments
- [ ] Add notification alerts
- [ ] Setup branch protection rules
- [ ] Configure auto-scaling

### Security
- [ ] Enable branch protection
- [ ] Require code reviews
- [ ] Setup security scans
- [ ] Rotate credentials periodically
- [ ] Use least-privilege IAM roles

---

## File Structure

```
.github/
├── workflows/
│   ├── build-and-push.yml           # Main workflow
│   ├── pull-request.yml             # PR validation
│   ├── security-scan.yml            # Vulnerability scanning
│   ├── deploy.yml                   # Deployment (optional)
│   └── build-and-push-private-registry.yml.example
├── CI-CD-GUIDE.md                   # Complete guide
├── SECRETS.md                       # Secret setup
├── PRIVATE-REGISTRY-SETUP.md        # Private registry options
├── setup-secrets.sh                 # Linux/Mac setup script
└── setup-secrets.bat                # Windows setup script
```

---

## Support & Resources

- **GitHub Actions Documentation:** https://docs.github.com/en/actions
- **Docker Hub Documentation:** https://docs.docker.com/docker-hub/
- **GitHub CLI:** https://cli.github.com/
- **Docker Security Best Practices:** https://docs.docker.com/engine/security/

---

## License

This CI/CD configuration is part of the NAGP project.

---

## Questions?

1. Check the documentation files in `.github/`
2. Review GitHub Actions logs in Actions tab
3. Consult Docker Hub documentation
4. Check GitHub Actions community discussions

**Happy building! 🚀**
