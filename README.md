# Garage-Door-Security-System-(Python)
A program created as a class project for Cybersecurity

The system was built as an academic project to reinforce concepts such as hardware integration, secure authentication, and real-time event handling using Python.

---

## Features
- Secure garage door control using a physical button
- Password authentication with hashing and salting
- Two-factor authentication (2FA) using a time-based email passkey
- Automatic email notifications when the door is opened
- Passkey expiration after 60 seconds
- LED indicators for door state (open/closed)
- Buzzer feedback for door actions
- Temporary button lockout to prevent rapid repeated inputs
- Protection against incorrect password and passkey attempts
  
---

## Technologies Used
- **Language:** Python
- **Hardware:** Raspberry Pi (GPIO)
- **Libraries:**
  - gpiozero (hardware control)
  - smtplib (email communication)
  - hashlib (password hashing)
  - secrets (secure token and salt generation)
  - threading (timers)
  - datetime / time (timing and expiration)
- **Concepts:**
  - Secure authentication (hashing + salting)
  - Two-factor authentication (2FA)
  - Event-driven programming
  - Hardware-software integration
  - Input validation and security checks
  
---

## Program Structure
- GPIO components initialized for:
  - LEDs (door status)
  - Button (user input)
  - Buzzer (feedback)
- **Authentication Flow:**
  - Password is salted and hashed at startup
  - User input is hashed and securely compared
  - If correct, a random 5-digit passkey is generated and emailed
  - User must enter passkey within 60 seconds
- **Core Functions:**
  - open_door() – handles authentication and opening sequence
  - close_door() – handles closing sequence
  - token() – generates and sends passkey
  - send_msg() – sends door open notification
  - salt() / hash_pass() – handle password security
  - door_button() – toggles door state
  - main() – initializes system and event loop
- **Security Features:**
  - Salted password hashing using SHA-256
  - Secure comparison using compare_digest
  - Time-limited passkey validation
  - Button cooldown using threading timer
 
---

## Sample Use Cases
- Press the physical button to trigger the system
- Enter the correct password when prompted
- Receive a passkey via email
- Enter the passkey within 60 seconds
- Garage door opens with LED and buzzer feedback
- Receive an email notification confirming the action
- Press button again to close the door

---

## Learning Outcomes
Through this project, I gained experience with:

- Integrating hardware with Python using GPIO
- Implementing secure authentication systems
- Designing multi-step verification (2FA) workflows
- Working with email protocols (SMTP)
- Handling real-time inputs and timed events
- Writing secure and maintainable Python code

---

## Authors
Conner Brandon
Jacksonville University

---

## Notes
- This program requires a configured emailcred.py file containing email credentials
- Designed to run on a Raspberry Pi with connected GPIO components
- For full implementation details, see the source code:
