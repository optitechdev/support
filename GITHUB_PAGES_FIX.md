# GitHub Pages 404 Error - Troubleshooting Guide

## Current Status
- ✅ Repository exists and is accessible
- ✅ `index.html` file is present in root
- ✅ `CNAME` file configured for `support.optitech-sverige.se`
- ✅ GitHub Actions workflow added for automatic deployment
- ❌ GitHub Pages returning 404 error

## Quick Fix Steps

### 1. Enable GitHub Pages (REQUIRED)
Go to: https://github.com/optitechdev/support/settings/pages

Configure:
- **Source**: Deploy from a branch
- **Branch**: main
- **Folder**: / (root)
- **Custom domain**: support.optitech-sverige.se
- **Enforce HTTPS**: ✅ Enabled

### 2. Verify DNS Configuration
Your DNS provider should have:
```
CNAME support.optitech-sverige.se -> optitechdev.github.io
```

Or A records pointing to:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 3. Check GitHub Actions
- Go to: https://github.com/optitechdev/support/actions
- Verify the deployment workflow runs successfully
- If it fails, check the logs for errors

### 4. Test URLs
After configuration (wait 5-10 minutes):
- GitHub Pages URL: https://optitechdev.github.io/support/
- Custom domain: https://support.optitech-sverige.se/

## Common Issues and Solutions

### Issue: "There isn't a GitHub Pages site here"
**Solution**: GitHub Pages is not enabled. Follow Step 1 above.

### Issue: DNS_PROBE_FINISHED_NXDOMAIN
**Solution**: DNS not configured. Check Step 2 above.

### Issue: Workflow permission errors
**Solution**: 
1. Go to Settings → Actions → General
2. Set "Workflow permissions" to "Read and write permissions"
3. Enable "Allow GitHub Actions to create and approve pull requests"

### Issue: Custom domain not working
**Solution**:
1. Remove custom domain from Pages settings
2. Wait 2 minutes
3. Re-add custom domain
4. Wait for DNS verification

## Verification Commands
Run these to test:
```bash
# Test GitHub Pages URL
curl -I https://optitechdev.github.io/support/

# Test custom domain
curl -I https://support.optitech-sverige.se/

# Check DNS resolution
nslookup support.optitech-sverige.se
```

## Expected Timeline
- GitHub Pages setup: Immediate
- DNS propagation: 5-15 minutes
- SSL certificate: 15-30 minutes
- Full functionality: Up to 1 hour

## Files Updated
- ✅ `index.html` - Main page content
- ✅ `CNAME` - Custom domain configuration
- ✅ `.github/workflows/deploy.yml` - Automatic deployment
- ✅ Repository pushed to main branch

## Next Steps
1. **IMMEDIATE**: Enable GitHub Pages in repository settings
2. **VERIFY**: Check that workflow runs successfully
3. **WAIT**: Allow 10-15 minutes for propagation
4. **TEST**: Visit https://support.optitech-sverige.se/

---
*Generated: $(date)*
*Repository: https://github.com/optitechdev/support*
