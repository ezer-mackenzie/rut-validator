# Security Policy

## Supported Versions

We take security seriously. The following versions of rut-validator are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in rut-validator, please report it to us as follows:

1. **Do not** create a public GitHub issue for the vulnerability
2. Email security concerns to: ramirez.ruiz.eliezer.reuven@gmail.com
3. Include detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Process

1. We will acknowledge receipt of your report within 48 hours
2. We will investigate and provide an initial assessment within 7 days
3. We will keep you updated on our progress throughout the process
4. Once resolved, we will publicly disclose the vulnerability after providing you time to upgrade

## Security Considerations

This library validates Chilean RUT (tax identification) numbers. While the validation algorithm itself is not security-sensitive, consider the following:

- **Input validation**: Always validate RUTs on both client and server side
- **Data storage**: Consider encrypting sensitive RUT data at rest
- **Privacy**: RUT numbers are considered personal data under Chilean law
- **Rate limiting**: Implement rate limiting on RUT validation endpoints to prevent abuse

## Responsible Disclosure

We kindly ask that you:

- Give us reasonable time to fix the issue before public disclosure
- Avoid accessing or modifying user data without permission
- Act in good faith to minimize harm to users

Thank you for helping keep rut-validator and its users secure!