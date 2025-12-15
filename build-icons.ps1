# SSRT Icon Generator Script
# Creates all required icons for PWA, iOS, and Android

$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "SSRT Icon Generator"
Write-Host "========================================"
Write-Host ""

# Check if ImageMagick is installed
$magick = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magick) {
    Write-Host "ERROR: ImageMagick not found!"
    Write-Host "Please install ImageMagick: https://imagemagick.org/script/download.php"
    Write-Host ""
    Write-Host "Or create icons manually:"
    Write-Host "  - icon-16.png (16x16)"
    Write-Host "  - icon-32.png (32x32)"
    Write-Host "  - icon-192.png (192x192)"
    Write-Host "  - icon-512.png (512x512)"
    Write-Host "  - apple-touch-icon.png (180x180)"
    exit 1
}

# Create icons directory
$iconsDir = "icons"
if (-not (Test-Path $iconsDir)) {
    New-Item -ItemType Directory -Path $iconsDir | Out-Null
}

# Source icon (create a simple one if doesn't exist)
$sourceIcon = "icon-source.png"
if (-not (Test-Path $sourceIcon)) {
    Write-Host "Creating source icon..."
    # Create a simple green square with SSRT text
    magick -size 512x512 xc:"#10b981" -pointsize 72 -fill white -gravity center -annotate +0+0 "SSRT" $sourceIcon
}

Write-Host "Generating icons from source..."

# Generate all required sizes
$sizes = @(
    @{size=16; name="icon-16.png"},
    @{size=32; name="icon-32.png"},
    @{size=180; name="apple-touch-icon.png"},
    @{size=192; name="icon-192.png"},
    @{size=512; name="icon-512.png"}
)

foreach ($icon in $sizes) {
    Write-Host "  Creating $($icon.name) ($($icon.size)x$($icon.size))..."
    magick $sourceIcon -resize "$($icon.size)x$($icon.size)" "$iconsDir\$($icon.name)"
}

# Copy to root
Write-Host ""
Write-Host "Copying icons to root directory..."
Copy-Item "$iconsDir\*" -Destination "." -Force

Write-Host ""
Write-Host "========================================"
Write-Host "Icons generated successfully!"
Write-Host "========================================"
Write-Host ""
Write-Host "Generated files:"
Get-ChildItem -Path "." -Filter "icon-*.png" | ForEach-Object { Write-Host "  - $($_.Name)" }
Get-ChildItem -Path "." -Filter "apple-touch-icon.png" | ForEach-Object { Write-Host "  - $($_.Name)" }
Write-Host ""


