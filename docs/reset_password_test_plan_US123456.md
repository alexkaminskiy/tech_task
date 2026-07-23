# Test Plan: Reset Password Feature (US #123456)

## Scope

This feature validates that a password reset request is accepted by the application.

Out of Scope:
- Reset Password email content
- Email delivery
- Reset Password page
- Reset token validation
- Reset Password functionality

---

## 1. Positive Testing

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1.1 | Existing registered email | Enter an existing email and click **Send reset link** | Generic success message displayed: **"If the user with this email exists, the Reset Password will be sent to him."** |
| 1.2 | Email case insensitivity | Enter `USER@Example.com` when account exists as `user@example.com` | Request processed successfully |
| 1.3 | Maximum allowed length | Enter a valid email with exactly 255 UTF-8 characters | Request accepted |
| 1.4 | UTF-8 characters | Enter an email containing supported UTF-8 characters | Request processed according to backend validation |
| 1.5 | Multiple consecutive requests | Submit multiple valid requests (within rate limit) | Every request succeeds until rate limit is reached |

---

## 2. Negative Testing

| # | Test Case | Input | Expected Result |
|---|-----------|-------|-----------------|
| 2.1 | Non-existing email | `unknown@example.com` | Same generic success message is displayed (no user enumeration) |
| 2.2 | Empty field | *(empty)* | Validation error shown; request is not sent |
| 2.3 | Whitespace only | `"   "` | Validation error shown |
| 2.4 | Leading whitespace | `" user@example.com"` | Processed exactly as entered (no trimming) |
| 2.5 | Trailing whitespace | `"user@example.com "` | Processed exactly as entered (no trimming) |
| 2.6 | Email longer than 255 characters | >255 characters | Validation error |
| 2.7 | Unsupported encoding | Invalid/non UTF-8 input | Validation error |

> **Note:** Email structure validation (missing `@`, invalid domain, etc.) is intentionally **Out of Scope** for this feature.

---

## 3. Boundary & Rate Limiting Testing (AC5)

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 3.1 | Exactly at limit | Submit 5 requests within 600 seconds | All requests accepted |
| 3.2 | Exceed limit | Submit a 6th request within 600 seconds | Request rejected according to AC |
| 3.3 | Window expiration | Wait until the 600-second window expires and submit again | Request accepted |
| 3.4 | Edge timing | Submit again at 599 seconds | Request still rejected |
| 3.5 | Different client | Another client submits requests | Rate limiting is independent per client endpoint |

---

## 4. Concurrency Testing

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 4.1 | Simultaneous requests | Submit multiple reset requests simultaneously for the same email | All requests processed normally (subject to rate limiting only) |

---

## 5. UI / UX Testing

1. Button remains enabled after submission.
2. Button appearance does not change.
3. Generic success message is displayed after every accepted request.
4. Validation messages are displayed for invalid input.
5. Email field has focus on page load.
6. Button is accessible via keyboard.
7. Layout is responsive across supported devices.

---

## 6. Compatibility Testing

1. Chrome (latest)
2. Firefox (latest)
3. Edge (latest)
4. Safari (latest)
5. Mobile

---

## 7. Exploratory Testing

1. Rapid repeated clicks.
2. Browser refresh during submission.
3. Offline during request.
4. Switching browser tabs while request is in progress.
5. Large UTF-8 input.
6. Different browser language settings.

---

## Assumptions / Clarifications Applied

- Existing and non-existing emails return the same generic success message to prevent user enumeration.
- Email delivery is Out of Scope.
- Reset Password functionality is Out of Scope.
- Email structure validation is handled by another feature.
- Maximum email length is 255 characters.
- UTF-8 characters are supported.
- Email comparison is case-insensitive.
- Whitespace is **not** trimmed.
- Multiple simultaneous requests are allowed except for the defined rate limit.
- SQL Injection and similar security payloads are outside the scope of this feature.