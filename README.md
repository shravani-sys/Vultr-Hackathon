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

### Setup Instructions

#### Step 1: Clone the Repository

```bash
git clone https://github.com/shravani-sys/Vultr-Hackathon.git
cd Vultr-Hackathon
```

#### Step 2: Install Python Requirements

If your Python app requires dependencies, install them using `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

#### Step 3: Run Python Application

Run the Python app to confirm it’s working (assuming `app.py` is the entry point):

```bash
python3 app.py
```

#### Step 4: Set Up Laravel Application

1. Move to the Laravel directory and create the project (if not already included):

   ```bash
   cd /var/www
   composer create-project --prefer-dist laravel/laravel chatbot-app
   cd chatbot-app
   ```

2. Configure the environment file:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with necessary environment variables:
     ```dotenv
     APP_NAME=Chatbot
     APP_ENV=production
     APP_KEY=base64:YourGeneratedAppKey
     APP_DEBUG=false
     APP_URL=http://your_server_ip
     ```

#### Step 5: Add Chatbot API Route in Laravel

Open `routes/api.php` and add an API route for chatbot inference:

```php
use App\Http\Controllers\ChatbotController;
Route::post('/infer', [ChatbotController::class, 'infer']);
```

#### Step 6: Create Chatbot Controller

Generate the controller and add code to call the serverless function for inference:

```bash
php artisan make:controller ChatbotController
```

Update `app/Http/Controllers/ChatbotController.php`:

```php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ChatbotController extends Controller
{
    public function infer(Request $request)
    {
        $userMessage = $request->input('message');

        // Call to Vultr Serverless Function
        $response = Http::post('YOUR_SERVERLESS_URL', [
            'message' => $userMessage,
        ]);

        return response()->json($response->json());
    }
}
```

Replace `YOUR_SERVERLESS_URL` with the URL of your Vultr serverless function.

#### Step 7: Configure Nginx for PHP and Python Applications

Create and edit a new Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/vultr-app
```

Paste the following configuration:

```nginx
server {
    listen 80;
    server_name your_server_ip;

    # Laravel app
    location / {
        root /var/www/chatbot-app/public;
        index index.php index.html;
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    # Python app
    location /python {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

Enable the configuration and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/vultr-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Step 8: Test the Application

Use `curl` or Postman to test the Laravel chatbot API endpoint:

```bash
curl -X POST http://your_server_ip/api/infer -H "Content-Type: application/json" -d '{"message": "Hello"}'
```

### Technical Documentation

For more information on system architecture, API documentation, and component details, refer to the `documentation.pdf` file included in this repository.

