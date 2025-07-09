# My Cycle Schedule App

A simple, private, and self-hosted web application to visualize a complex medication and appointment schedule. This app was specifically designed to track a fertility treatment cycle but can be customized for any time-based schedule.

It is built to be deployed easily and securely as a Docker container, accessible from anywhere via a Cloudflare Tunnel without exposing any ports on your home server.

---

## ✨ Features

* **Today View:** An at-a-glance summary of today's medications and appointments, plus a preview of tomorrow's schedule.
* **Calendar View:** A full monthly calendar that highlights days with scheduled events. Click any day to see its full details.
* **Legend:** A dedicated view to explain the color-coding and icons for each medication and event type.
* **Video Links:** Medications can include direct links to instruction videos, accessible from both the Legend and the daily schedule views.
* **Responsive Design:** The interface is clean and usable on both desktop and mobile devices.
* **100% Private:** The app runs entirely on your own hardware. The schedule data never leaves your server.
* **Securely Accessible:** Uses a Cloudflare Tunnel to provide secure HTTPS access from any device without opening firewall ports or exposing your IP address.
* **Telegram Reminders:** Get reminders for today's medications and appointments, plus a preview of tomorrow's schedule, sent directly to your Telegram account.

---

## 🔧 Tech Stack

* **Frontend:** HTML5, CSS3, and Vanilla JavaScript (no frameworks).
* **Data:** A simple `schedule.json` file serves as the database.
* **Web Server:** [Nginx](https://www.nginx.com/) (inside a Docker container).
* **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/).
* **Deployment:** [Cloudflare Tunnel](https://www.cloudflare.com/products/zero-trust/tunnel/) (`cloudflared`).
* **Reminders:** Python with `schedule` and `python-telegram-bot`.

---

## 🚀 Getting Started

Follow these instructions to get the application running on your own server.

### Prerequisites

* A server with **Docker** and **Docker Compose** installed.
* A **Cloudflare account**.
* A **domain name** registered and managed through your Cloudflare account.
* A **Telegram account**.

### Installation & Deployment

**1. Clone the Repository**

```bash
git clone <https://github.com/your-username/your-repo-name.git>
cd your-repo-name
```

**2. Create a Cloudflare Tunnel**

This tunnel will create a secure connection between your server and Cloudflare's network.

1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com).
2. On the left sidebar, navigate to **Zero Trust**.
3. Go to **Access -> Tunnels**.
4. Click **Create a tunnel**.
5. Give your tunnel a name (e.g., `cycle-app-server`) and click **Save tunnel**.
6. On the next screen, you will be shown a command to run. You only need the **token**. It's the long string of characters in the command. Copy this token.
7. Click **Next**. You will be taken to the "Route traffic" page. Configure it as follows:
    * **Subdomain:** The subdomain you want to use (e.g., `cycle`).
    * **Domain:** Select your domain from the dropdown.
    * **Service -> Type:** `HTTP`
    * **Service -> URL:** `cycle-app:80` (This points to the Nginx container on its internal Docker network).
8. Click **Save hostname**.

**3. Create a Telegram Bot & Get Credentials**

1. Open the Telegram app and search for the "BotFather" user.
2. Start a chat with the BotFather and send the `/newbot` command.
3. Follow the prompts to give your bot a name and a username.
4. The BotFather will provide you with a **Bot Token**. Copy this token.
5. Open the Telegram app and search for the "userinfobot" user.
6. Start a chat with the userinfobot and send the `/start` command.
7. The bot will reply with your **Chat ID**. Copy this ID.

**4. Set Up a Group Chat for Shared Reminders (Recommended)**

For couples or families who want to share reminders, it's best to create a group chat with your bot. This way, both you and your partner will receive the same reminders in one place.

1. In Telegram, click the **New Message** button (pencil icon).
2. Select **New Group**.
3. Add your partner to the group.
4. Give the group a name (e.g., "Cycle Reminders").
5. Create the group.
6. In the group chat, search for your bot by username and add it to the group.
7. Send a message in the group (any message will do - this activates the bot).
8. To get the group's Chat ID easily, add one of these bots to your group:
    * **@RawDataBot** (recommended) - Search for "@RawDataBot" and add it to your group
    * **@getidsbot** - Search for "@getidsbot" and add it to your group
    * **@userinfobot** - Search for "@userinfobot" and add it to your group
    * Send any message in the group
    * The bot will reply with the group's Chat ID (it will be a negative number)
9. Copy this **Group Chat ID** (the negative number).

**Note:** Group chat IDs start with a minus sign (e.g., `-123456789`). This is how Telegram distinguishes groups from individual users.

**Benefits of Using a Group Chat:**

* **Shared visibility:** Both partners see the same reminders
* **Easy coordination:** No need to forward messages between each other
* **Single source of truth:** All reminders are in one place
* **Reduced complexity:** Only one chat ID to manage instead of multiple individual IDs

**5. Configure Your Local Environment**

The project uses an environment file to securely store your tunnel token and Telegram credentials.

1. Copy the example environment file. This command works on Linux/macOS:

    ```bash
    cp .env.example .env
    ```

2. Open the new `.env` file with a text editor.
3. Paste the Cloudflare Tunnel token and Telegram credentials you copied in the previous steps.

    **For Individual Reminders:**

    ```
    # ./.env

    TUNNEL_TOKEN=eyJhIjoi...<your-long-secret-token-here>...wMiJ9
    TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    TELEGRAM_CHAT_IDS=123456789
    ```

    **For Group Chat Reminders (Recommended):**

    ```
    # ./.env

    TUNNEL_TOKEN=eyJhIjoi...<your-long-secret-token-here>...wMiJ9
    TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    TELEGRAM_CHAT_IDS=-123456789
    ```

    **For Multiple Recipients:**

    ```
    # ./.env

    TUNNEL_TOKEN=eyJhIjoi...<your-long-secret-token-here>...wMiJ9
    TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    TELEGRAM_CHAT_IDS=123456789,-987654321
    ```

**6. Launch the Application**

With the token and credentials configured, you can now launch the application, tunnel, and reminder bot using Docker Compose.

```bash
docker-compose up -d --build
```

Your application is now live! You can access it at the public URL you configured (e.g., `https://cycle.mydomain.com`). The Cloudflare Tunnel dashboard should show the tunnel status as "HEALTHY". You will also receive reminders in your Telegram account (or group chat) at the scheduled times.

---

## 📁 Project Structure

```
.
├── docker-compose.yml   # Defines the app, cloudflared, and reminder services
├── Dockerfile           # Builds the Nginx container for the app
├── nginx.conf           # Nginx configuration file
├── reminder.Dockerfile  # Builds the Python container for the bot
├── send_reminder.py     # Main application logic for reminders
├── reminder_logic.py    # Core business logic for generating reminder content
├── src/                 # Contains all frontend code and data
│   ├── app.js           # Main application logic
│   ├── index.html       # Main HTML file
│   ├── schedule.json    # The schedule data file (edit this to customize)
│   └── style.css        # All application styles
├── .env.example         # Template for environment variables
└── README.md            # This file
```

---

## 🧪 Testing

To test the reminder notifications for a specific date, you can run the reminder service with the `REMINDER_DATE` environment variable. This will send all reminders for the specified date immediately.

```bash
docker-compose run --rm -e REMINDER_DATE=YYYY-MM-DD reminder
```

---

## ✍️ Customization

To change the schedule, simply edit the **`src/schedule.json`** file. You can add, remove, or modify entries for dates, medications, and appointments. The application will automatically reflect the changes the next time you load it and the next time a reminder is sent.

---

## 📜 License

This project is licensed under the MIT License.
