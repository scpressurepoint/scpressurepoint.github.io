# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a static website for **Peak Pressure Washing Co.**, a student-owned pressure washing business in Columbia, SC. The site is hosted on GitHub Pages and serves as the primary business website with contact forms, service information, and business documentation.

### Architecture

- **Static HTML Website**: Pure HTML/CSS/JavaScript with no build process
- **GitHub Pages Hosting**: Direct deployment from the main branch
- **Frontend Stack**: 
  - Vanilla HTML5/CSS3/JavaScript
  - TailwindCSS (via CDN)
  - Font Awesome icons (via CDN)
  - FormSubmit for form handling

### Core File Structure

```
├── index.html           # Main landing page with services, gallery, contact form
├── thank-you.html       # Post-form submission confirmation page  
├── estimate.html        # Dedicated estimate request form
├── form.html           # Standalone contact form
├── flyer.html          # Printable business flyer/marketing material
├── invoice.html        # Invoice generation tool for business operations
└── assets/             # Images (Before1.png, After1.png, Logo.png, etc.)
```

## Development Commands

### Local Development
```bash
# Serve locally (any HTTP server)
python -m http.server 8000
# OR
npx serve .
# OR  
php -S localhost:8000
```

### Git Operations
```bash
# Deploy to GitHub Pages (pushes to main branch auto-deploy)
git add .
git commit -m "Update website content"
git push origin main

# Check deployment status
git log --oneline -5
```

## Key Technical Details

### Form Handling System
- Uses **FormSubmit.co** for server-side form processing with file attachments
- Photo uploads supported up to 10MB per file
- FormSubmit endpoint handles file attachments and redirects to `thank-you.html`

### Interactive Components
- **Before/After Image Slider**: Custom JavaScript implementation with drag/touch support
- **FAQ Accordion**: Toggle functionality for service questions
- **Mobile Photo Upload**: iOS-optimized file selection and preview
- **Mobile Navigation**: Collapsible hamburger menu

### Styling Architecture
- **TailwindCSS**: Primary CSS framework loaded via CDN
- **Custom CSS**: Embedded in `<style>` tags within each HTML file
- **Color Scheme**: 
  - Primary: `#0ea5e9` (sky blue)
  - Secondary: `#38bdf8` 
  - Dark: `#0f172a` (slate)
  - Accent: `#06b6d4` (cyan)

## Business Tools

### Invoice Generator (`invoice.html`)
- Calculates costs based on square footage, labor hours, and materials
- Fixed rates: Gas ($3.50/gal), Chemical ($15.00/gal)
- Supports additional line items and discounts
- Generates printable invoices with company branding

### Marketing Flyer (`flyer.html`)
- Print-optimized business flyer (8.5" x 11")
- Contains service areas, pricing info, contact details
- Responsive design that stacks on mobile

## Deployment Notes

- **Live URL**: `https://peakpressureco.github.io/`
- **Auto-deployment**: Any push to `main` branch triggers GitHub Pages rebuild
- **DNS**: Currently using default GitHub Pages subdomain
- **HTTPS**: Automatically enabled by GitHub Pages

## Content Management

### Service Updates
- Update service listings in the `#services` section of `index.html`
- Pricing information is in the `#pricing` section
- FAQ content is in the dedicated FAQ accordion section

### Gallery Updates
- Replace image URLs in the `#gallery` section
- Images hosted on GitHub: `https://github.com/peakpressureco/peakpressureco.github.io/blob/main/[filename]?raw=true`
- Before/after slider images: `Before1.png` and `After1.png`

### Contact Information Updates
- Business phone: `(803) 200-2027`
- Service areas include Columbia, SC and surrounding areas
- Instagram: `@peakpressureco`

## Development Guidelines

### Form Testing
- Verify FormSubmit.co endpoint receives submissions correctly
- Test photo upload functionality across different devices/browsers

### Mobile Optimization
- All pages are mobile-first responsive
- Touch targets meet minimum 44px requirement
- Photo upload specifically optimized for iOS Safari

### Performance Considerations
- External CDN dependencies: TailwindCSS, Font Awesome
- Image optimization: Use WebP format when possible
- Minimize inline CSS where practical for maintainability

### Local Testing Checklist
1. Form submissions work correctly
2. Before/after sliders are interactive
3. Mobile navigation toggles properly
4. Photo upload shows previews correctly
5. Invoice generator calculates totals accurately

## Business Context

This website serves a student-owned pressure washing business specializing in:
- Driveway cleaning
- Sidewalk/walkway cleaning  
- Patio and deck cleaning
- Brick and stone cleaning
- Entryway cleaning

The business operates in Columbia, SC and surrounding areas with competitive square-footage-based pricing typically ranging from $0.15-0.30 per square foot depending on job complexity.