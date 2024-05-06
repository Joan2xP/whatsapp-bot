# WhatsApp Bot

A script I made with Playwright to send WhatsApp images in bulk.

## Usage

To send the messages, a .ods file containing contacts, another .ods file containing users to send messages and text to put in the final image are needed, add them in a .env. There are example files.

You need to install pip packages:

```
pip install -r requirements.txt
```
> [!IMPORTANT]
> This script only works in spanish WhatsApp web, some DOM elements are selected by their text
## Technologies

- Playwright: Used to interact with WhatsApp Web.
- PIL: Utilized for creating images from text.

## Unique Traces

I aimed to interact with WhatsApp Web as quickly as possible, without relying on uncertain timers. Instead, I used triggers to advance to the next action promptly without unnecessary delays or failures.


