```markdown
# Event Registration Portal Test Cases

## 1. TC-001: Successful Registration with Valid Details
### Precondition:
User is on the Event Registration Portal login page.

### Test Steps:
1. Enter a valid email address in the "Email" field.
2. Enter a valid password in the "Password" field.
3. Click on the "Register" button.

### Expected Result:
- A confirmation message appears: "Registration successful!"
- The user is redirected to the registration page where they can enter event details.

**Status:** Pending

## 2. TC-002: Registration with Empty Email Field
### Precondition:
User is on the Event Registration Portal login page.

### Test Steps:
1. Leave the "Email" field empty.
2. Enter a valid password in the "Password" field.
3. Click on the "Register" button.

### Expected Result:
- An error message appears: "Email is required."
- The user remains on the registration page.

**Status:** Pending

## 3. TC-003: Registration with Invalid Email Format
### Precondition:
User is on the Event Registration Portal login page.

### Test Steps:
1. Enter an invalid email address (e.g., "user@domain") in the "Email" field.
2. Enter a valid password in the "Password" field.
3. Click on the "Register" button.

### Expected Result:
- An error message appears: "Invalid email format."
- The user remains on the registration page.

**Status:** Pending

## 4. TC-004: Registration with Empty Password Field
### Precondition:
User is on the Event Registration Portal login page.

### Test Steps:
1. Enter a valid email address in the "Email" field.
2. Leave the "Password" field empty.
3. Click on the "Register" button.

### Expected Result:
- An error message appears: "Password is required."
- The user remains on the registration page.

**Status:** Pending

## 5. TC-005: Successful Event Registration
### Precondition:
User is logged in to the Event Registration Portal.

### Test Steps:
1. Click on the "Register for Event" button.
2. Select an event from the list of available events.
3. Fill in all required details (e.g., name, contact number).
4. Click on the "Submit" button.

### Expected Result:
- A confirmation message appears: "Event registered successfully!"
- The user is redirected to the dashboard showing their registered events.

**Status:** Pending

## 6. TC-006: Attempt to Register for an Event Without Logging In
### Precondition:
User is not logged in to the Event Registration Portal.

### Test Steps:
1. Click on the "Register for Event" button.
2. Select an event from the list of available events.
3. Fill in all required details (e.g., name, contact number).
4. Click on the "Submit" button.

### Expected Result:
- An error message appears: "Please log in to register for an event."
- The user is redirected back to the login page.

**Status:** Pending

## 7. TC-007: Event Registration with Invalid Date Format
### Precondition:
User is logged in to the Event Registration Portal and on the Event Registration page.

### Test Steps:
1. Select an event from the list of available events.
2. Enter an invalid date format (e.g., "32/12/2023") in the "Date" field.
3. Fill in all other required details.
4. Click on the "Submit" button.

### Expected Result:
- An error message appears: "Invalid date format."
- The user remains on the registration page.

**Status:** Pending

## 8. TC-008: Event Registration with Past Date
### Precondition:
User is logged in to the Event Registration Portal and on the Event Registration page.

### Test Steps:
1. Select an event from the list of available events.
2. Enter a past date (e.g., "01/01/2023") in the "Date" field.
3. Fill in all other required details.
4. Click on the "Submit" button.

### Expected Result:
- An error message appears: "Event date must be in the future."
- The user remains on the registration page.

**Status:** Pending
```