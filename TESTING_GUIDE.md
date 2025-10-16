# Testing Guide for Photo Organiser

This document provides comprehensive test cases to verify all functionality of the Photo Organiser application.

## Pre-Testing Setup

1. Ensure both backend and frontend servers are running
2. Open the application in a web browser at http://localhost:3000
3. Open browser developer tools (F12) to monitor console for errors

---

## Test Suite 1: Album Management

### Test 1.1: Create Single Album
**Steps:**
1. Click "Create Album" button
2. Enter album name: "Vacation Photos"
3. Enter description: "Summer vacation 2024"
4. Click "Create"

**Expected Result:**
- ✅ Album appears in the grid
- ✅ Album name and description are displayed correctly
- ✅ No errors in console

### Test 1.2: Create Multiple Albums
**Steps:**
1. Create 5 albums with the following names:
   - "Family Events"
   - "Nature Photography"
   - "Urban Landscapes"
   - "Food & Cooking"
   - "Pets"

**Expected Result:**
- ✅ All 5 albums appear in the grid
- ✅ Albums are displayed in a responsive grid layout
- ✅ Each album card is properly styled

### Test 1.3: Edit Album
**Steps:**
1. Hover over "Vacation Photos" album
2. Click the edit (pencil) icon
3. Change name to "Summer Vacation 2024"
4. Change description to "Beach trip and mountain hiking"
5. Click "Update"

**Expected Result:**
- ✅ Album name and description update immediately
- ✅ Modal closes after update
- ✅ Changes persist after page refresh

### Test 1.4: Delete Album
**Steps:**
1. Hover over "Pets" album
2. Click the delete (trash) icon
3. Confirm deletion in the dialog

**Expected Result:**
- ✅ Album is removed from the grid
- ✅ Smooth removal animation
- ✅ Album stays deleted after page refresh

### Test 1.5: Empty State
**Steps:**
1. Delete all albums
2. Observe the empty state

**Expected Result:**
- ✅ Empty state message appears
- ✅ "Create Your First Album" button is visible
- ✅ Clicking button opens album creation modal

---

## Test Suite 2: Photo Upload - File Formats

### Test 2.1: Upload PNG Images
**Steps:**
1. Open any album
2. Click or drag PNG image(s) to upload area
3. Wait for upload to complete

**Expected Result:**
- ✅ PNG images upload successfully
- ✅ Images appear in the photo grid
- ✅ Images display correctly

### Test 2.2: Upload JPEG Images
**Steps:**
1. Upload JPEG/JPG format images
2. Try both .jpg and .jpeg extensions

**Expected Result:**
- ✅ JPEG images upload successfully
- ✅ Both .jpg and .jpeg extensions work
- ✅ Image quality is acceptable

### Test 2.3: Upload HEIC Images
**Steps:**
1. Upload HEIC images (iOS format)
2. If HEIC images not available, skip this test

**Expected Result:**
- ✅ HEIC images are converted and uploaded
- ✅ Images display as JPEG in browser
- ✅ No conversion errors

### Test 2.4: Upload Invalid Format
**Steps:**
1. Try to upload a PDF, Word document, or video file

**Expected Result:**
- ✅ Invalid files are rejected
- ✅ User sees appropriate error message
- ✅ No errors in console

---

## Test Suite 3: Photo Upload - Multiple Files

### Test 3.1: Multiple File Selection
**Steps:**
1. Click upload area
2. Select 5-10 images at once using file picker
3. Click "Open"

**Expected Result:**
- ✅ All images upload successfully
- ✅ Upload progress is visible
- ✅ All images appear in grid after upload

### Test 3.2: Drag and Drop Multiple Files
**Steps:**
1. Select 5-10 images in file explorer
2. Drag them to the upload area
3. Release to drop

**Expected Result:**
- ✅ Drag overlay appears during drag
- ✅ All images upload successfully
- ✅ Images appear in correct order

### Test 3.3: Large Batch Upload
**Steps:**
1. Upload 20+ images at once

**Expected Result:**
- ✅ All images upload successfully
- ✅ No timeout errors
- ✅ UI remains responsive during upload

---

## Test Suite 4: Image Compression

### Test 4.1: Verify Compression Ratio
**Steps:**
1. Note original size of a large image (e.g., 5MB)
2. Upload the image
3. Navigate to `backend/uploads/album_X/` directory
4. Check compressed file size

**Expected Result:**
- ✅ Compressed file is significantly smaller (50-70% reduction)
- ✅ Image quality remains acceptable
- ✅ File is in JPEG format

### Test 4.2: Multiple Image Compression
**Steps:**
1. Upload 10 large images (total > 30MB)
2. Check total size of compressed images in uploads folder

**Expected Result:**
- ✅ Total compressed size is much smaller than original
- ✅ All images maintain acceptable quality
- ✅ Storage savings are significant

### Test 4.3: PNG with Transparency
**Steps:**
1. Upload a PNG image with transparent background
2. View the uploaded image

**Expected Result:**
- ✅ Image uploads successfully
- ✅ Transparency is replaced with white background
- ✅ Image displays correctly

---

## Test Suite 5: Photo Management

### Test 5.1: Delete Single Photo
**Steps:**
1. Open an album with photos
2. Hover over a photo
3. Click delete icon
4. Confirm deletion

**Expected Result:**
- ✅ Photo is removed from grid
- ✅ Smooth removal animation
- ✅ Photo stays deleted after refresh

### Test 5.2: View Photo Details
**Steps:**
1. Hover over any photo
2. Observe the overlay information

**Expected Result:**
- ✅ Original filename is displayed
- ✅ Delete button appears
- ✅ Overlay has smooth transition

### Test 5.3: Empty Album State
**Steps:**
1. Delete all photos from an album
2. Observe empty state

**Expected Result:**
- ✅ Empty state message appears
- ✅ Upload area still visible
- ✅ "No photos yet" message displayed

---

## Test Suite 6: Navigation & Routing

### Test 6.1: Navigate to Album
**Steps:**
1. From album list, click on any album
2. Observe URL change

**Expected Result:**
- ✅ URL changes to `/album/[id]`
- ✅ Album view loads with correct photos
- ✅ Back button appears

### Test 6.2: Back Navigation
**Steps:**
1. From album view, click "Back to Albums"
2. Return to album list

**Expected Result:**
- ✅ Returns to album list view
- ✅ All albums still visible
- ✅ URL changes to `/`

### Test 6.3: Browser Back Button
**Steps:**
1. Navigate to album view
2. Use browser back button

**Expected Result:**
- ✅ Returns to album list
- ✅ No errors occur
- ✅ State is preserved

### Test 6.4: Direct URL Access
**Steps:**
1. Copy album URL (e.g., http://localhost:3000/album/2)
2. Open in new tab

**Expected Result:**
- ✅ Album view loads correctly
- ✅ Photos are displayed
- ✅ No 404 errors

---

## Test Suite 7: UI/UX & Responsiveness

### Test 7.1: Desktop Layout
**Steps:**
1. View application on desktop (1920x1080)
2. Check all views

**Expected Result:**
- ✅ Grid layouts use available space efficiently
- ✅ Cards are properly sized
- ✅ No horizontal scrolling

### Test 7.2: Tablet Layout
**Steps:**
1. Resize browser to tablet size (768px width)
2. Check all views

**Expected Result:**
- ✅ Layout adjusts appropriately
- ✅ Touch targets are adequate
- ✅ No layout breaks

### Test 7.3: Mobile Layout
**Steps:**
1. Resize browser to mobile size (375px width)
2. Check all views

**Expected Result:**
- ✅ Single column layout
- ✅ All buttons accessible
- ✅ Text is readable

### Test 7.4: Hover Effects
**Steps:**
1. Hover over various interactive elements
2. Check album cards, buttons, photos

**Expected Result:**
- ✅ Smooth color transitions
- ✅ Cursor changes to pointer
- ✅ Visual feedback is clear

### Test 7.5: Dark Mode Colors
**Steps:**
1. Verify color scheme matches Material Design 3

**Expected Result:**
- ✅ Background is #0D0D0D
- ✅ Cards use #1A1A1A
- ✅ Accent color #C82FFF is visible
- ✅ Text is readable (#FFFFFF)

---

## Test Suite 8: Error Handling

### Test 8.1: Backend Offline
**Steps:**
1. Stop the backend server
2. Try to create an album

**Expected Result:**
- ✅ User sees error message
- ✅ No app crash
- ✅ App recovers when backend restarts

### Test 8.2: Invalid Album ID
**Steps:**
1. Navigate to http://localhost:3000/album/999999

**Expected Result:**
- ✅ Error message appears
- ✅ User is redirected to home
- ✅ No console errors

### Test 8.3: Network Issues
**Steps:**
1. Simulate slow network using browser DevTools
2. Upload images

**Expected Result:**
- ✅ Loading states appear
- ✅ User can wait for completion
- ✅ No timeout errors

---

## Test Suite 9: Data Persistence

### Test 9.1: Page Refresh
**Steps:**
1. Create albums and upload photos
2. Refresh the page

**Expected Result:**
- ✅ All albums are still visible
- ✅ All photos are still visible
- ✅ No data loss

### Test 9.2: Browser Restart
**Steps:**
1. Close browser completely
2. Reopen and navigate to application

**Expected Result:**
- ✅ All data persists
- ✅ Albums and photos intact
- ✅ Database remains consistent

### Test 9.3: Server Restart
**Steps:**
1. Stop backend server
2. Restart backend server
3. Refresh frontend

**Expected Result:**
- ✅ All data persists
- ✅ SQLite database preserves all records
- ✅ Uploaded files still accessible

---

## Test Suite 10: Performance

### Test 10.1: Large Album
**Steps:**
1. Upload 100+ photos to a single album
2. Measure page load time

**Expected Result:**
- ✅ Grid loads smoothly
- ✅ Lazy loading works correctly
- ✅ No significant lag

### Test 10.2: Multiple Albums
**Steps:**
1. Create 50+ albums
2. View album list

**Expected Result:**
- ✅ List renders without lag
- ✅ Smooth scrolling
- ✅ No memory issues

### Test 10.3: Concurrent Uploads
**Steps:**
1. Upload multiple images simultaneously to different albums

**Expected Result:**
- ✅ All uploads complete successfully
- ✅ No conflicts or errors
- ✅ Correct album association

---

## Testing Summary Checklist

Use this checklist to track overall testing progress:

**Album Management**
- [ ] Create album
- [ ] Edit album
- [ ] Delete album
- [ ] View empty state

**Photo Upload**
- [ ] Upload PNG
- [ ] Upload JPEG
- [ ] Upload HEIC
- [ ] Multiple file upload
- [ ] Drag and drop

**Compression**
- [ ] Verify size reduction
- [ ] Check image quality
- [ ] Test with large files

**Photo Management**
- [ ] View photos
- [ ] Delete photos
- [ ] Photo grid layout

**Navigation**
- [ ] Album navigation
- [ ] Back button
- [ ] Browser history
- [ ] Direct URLs

**UI/UX**
- [ ] Desktop responsive
- [ ] Tablet responsive
- [ ] Mobile responsive
- [ ] Hover effects
- [ ] Dark mode colors

**Error Handling**
- [ ] Backend offline
- [ ] Invalid data
- [ ] Network issues

**Data Persistence**
- [ ] Page refresh
- [ ] Browser restart
- [ ] Server restart

**Performance**
- [ ] Large albums
- [ ] Many albums
- [ ] Concurrent operations

---

## Bug Reporting Template

If you find any bugs during testing, use this template:

**Bug Title:** [Brief description]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happens]

**Browser/Environment:**
- Browser: [Chrome/Firefox/Safari]
- OS: [Windows/macOS/Linux]
- Screen size: [Desktop/Tablet/Mobile]

**Console Errors:**
```
[Paste any console errors here]
```

**Screenshots:**
[Attach if applicable]

---

## Testing Completion

Once all test suites are completed:
1. Document any issues found
2. Verify all critical functionality works
3. Test on different browsers (Chrome, Firefox, Safari)
4. Test on actual mobile device if possible

**Testing Status:** [ ] Complete  [ ] In Progress  [ ] Not Started

**Tested By:** ________________

**Date:** ________________

**Notes:**
________________________________
________________________________
________________________________

