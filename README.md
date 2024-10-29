# Emotion-Aware AI Chatbot

This project is an **Emotion-Aware AI Chatbot** designed to provide empathetic and predictive customer service. Built with **Laravel** for backend processing and **Vultr Serverless Functions** for real-time inference, this chatbot can analyze user sentiment and respond accordingly. The chatbot also uses **Vultr Object Storage** to maintain user interaction history, enabling data-driven insights and personalized responses.

## Project Structure

1. **Client Interface**: JavaScript-powered frontend that enables user interactions with the chatbot.
2. **Backend (Laravel)**: Manages user interactions, calls the serverless inference API, and handles data storage.
3. **Serverless Function**: Executes sentiment and emotion analysis using Hugging Face API.
4. **Object Storage**: Stores interaction history for data insights.

## Getting Started

### Prerequisites

- **Vultr Account**: Provision a compute instance, with access to Serverless Functions and Object Storage.
- **Server Software**: Ensure PHP, Python, Composer, and Nginx are installed on the server.

Here's an updated **Build and Deployment Instructions** section for your README file:

---

### Build and Deployment Instructions

Follow these steps to build, deploy, and launch the Emotion-Aware AI Chatbot on your Vultr server.

#### Step 1: Clone the Repository

1. Clone the project repository from GitHub:

   ```bash
   git clone https://github.com/shravani-sys/Vultr-Hackathon.git
   cd Vultr-Hackathon
   ```

#### Step 2: Set Up and Run the Python Application

1. Install dependencies required by the Python application:

   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the Python application to ensure it’s working correctly (replace `app.py` with your main file):

   ```bash
   python3 app.py
   ```

#### Step 3: Set Up and Configure Laravel Application

1. Navigate to the Laravel project folder and install dependencies if required:

   ```bash
   cd /var/www/chatbot-app
   composer install
   ```

2. Configure environment settings:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with database, API keys, and server URLs.

3. Generate an application key for Laravel:

   ```bash
   php artisan key:generate
   ```

#### Step 4: Set Up Serverless Function on Vultr

1. Deploy your sentiment and emotion analysis function on Vultr Serverless.
2. Note the function’s URL endpoint and update the `ChatbotController` in Laravel with this URL.

#### Step 5: Configure the Nginx Server

1. Set up an Nginx configuration for the Laravel and Python applications.
2. Paste and save the configuration, then restart Nginx:

   ```bash
   sudo ln -s /etc/nginx/sites-available/vultr-app /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

#### Step 6: Test the Application

Test the API endpoints using tools like `curl` or Postman to ensure responses are as expected.

