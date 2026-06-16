
# AI Bridge Local - Composer submit guard 0.5.11

## Objective
Prevent ChatGPT UI buttons such as Share/Compartilhar from being mistaken for the message submit button.

## Behavior
- Rejects unsafe submit candidates such as Share, Compartilhar, Copy Link, Cancel and modal buttons.
- Closes blocking share dialogs before injection and before submit attempts.
- Keeps delivery confirmation dependent on composer clear behavior.
