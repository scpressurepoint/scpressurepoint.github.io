# Phone Number Update Guide

## When You Get Your Business Line

**Current Phone**: (803) 351-2333 (Personal - Temporary)
**Future Phone**: [Your Business Line] - Update when ready

### Files to Update:

1. **`index.html`** - Main website file
   - Search for `(803) 351-2333` and replace all instances
   - Search for `8033512333` and replace with new number (no spaces/parentheses)
   - Update the JavaScript constants at the top of the script section

2. **`README.md`** - Documentation
   - Update phone number in contact section

3. **`robots.txt`** - SEO file
   - Update phone number in comments

4. **All files in `pages/` folder**:
   - `thank-you.html`
   - `estimate.html` 
   - `form.html`

### Quick Find & Replace:
- **Display Format**: `(803) 351-2333` → `(Your New Number)`
- **Link Format**: `8033512333` → `YourNewNumberDigitsOnly`
- **SMS Links**: `sms:(803)351-2333` → `sms:(YourNewNumber)`
- **Tel Links**: `tel:(803)351-2333` → `tel:(YourNewNumber)`

### After Updating:
1. Commit changes: `git add . && git commit -m "Update to business phone number"`
2. Push to deploy: `git push`
3. Website will update automatically within 2-3 minutes

### Test After Update:
- [ ] Text buttons work on mobile
- [ ] Call buttons work on mobile  
- [ ] All contact sections show new number
- [ ] Form submissions work properly