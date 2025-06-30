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

---

## 🔧 Tech Stack

* **Frontend:** HTML5, CSS3, and Vanilla JavaScript (no frameworks).
* **Data:** A simple `schedule.json` file serves as the database.
* **Web Server:** [Nginx](https://www.nginx.com/) (inside a Docker container).
* **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/).
* **Deployment:** [Cloudflare Tunnel](https://www.cloudflare.com/products/zero-trust/tunnel/) (`cloudflared`).

---

## 🚀 Getting Started

Follow these instructions to get the application running on your own server.

### Prerequisites

* A server with **Docker** and **Docker Compose** installed.
* A **Cloudflare account**.
* A **domain name** registered and managed through your Cloudflare account.

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

**3. Configure Your Local Environment**

The project uses an environment file to securely store your tunnel token.

1. Copy the example environment file. This command works on Linux/macOS:

    ```bash
    cp .env.example .env
    ```

2. Open the new `.env` file with a text editor.
3. Paste the Cloudflare Tunnel token you copied in the previous step.

    ```

    # ./.env

    TUNNEL_TOKEN=eyJhIjoi...<your-long-secret-token-here>...wMiJ9
    ```

**4. Launch the Application**

With the token configured, you can now launch both the application and the tunnel using Docker Compose.

```bash
docker-compose up -d --build
```

Your application is now live! You can access it at the public URL you configured (e.g., `https://cycle.mydomain.com`). The Cloudflare Tunnel dashboard should show the tunnel status as "HEALTHY".

---

## 📁 Project Structure

```
.
├── docker-compose.yml   # Defines the app and cloudflared services
├── Dockerfile           # Builds the Nginx container for the app
├── nginx.conf           # Nginx configuration file
├── src/                 # Contains all frontend code and data
│   ├── app.js           # Main application logic
│   ├── index.html       # Main HTML file
│   ├── schedule.json    # The schedule data file (edit this to customize)
│   └── style.css        # All application styles
├── .env.example         # Template for environment variables
└── README.md            # This file
```

---

## ✍️ Customization

To change the schedule, simply edit the **`src/schedule.json`** file. You can add, remove, or modify entries for dates, medications, and appointments. The application will automatically reflect the changes the next time you load it.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
