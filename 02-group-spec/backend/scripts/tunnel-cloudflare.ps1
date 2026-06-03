# Expose local API (port 8000) via Cloudflare Quick Tunnel
# Requires: cloudflared installed — https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/downloads/
$port = $env:API_PORT
if (-not $port) { $port = "8000" }

Write-Host "Tunneling http://127.0.0.1:$port ..."
Write-Host "Paste the https://....trycloudflare.com URL into VITE_VINWONDERS_API if frontend is not using Vite proxy."
cloudflared tunnel --url "http://127.0.0.1:$port"
