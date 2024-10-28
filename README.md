# Vultr-Hackathon
Project Overview
This project is an Emotion-Aware AI Chatbot designed to provide empathetic and predictive customer service. Built on Laravel with Vultr Serverless Functions for real-time inference, this chatbot can analyze user sentiment and respond appropriately. Additionally, it uses Vultr Object Storage to maintain user interaction history, enabling data-driven insights.

#Project Structure
Client Interface: JavaScript-powered frontend.
Backend (Laravel): Manages interactions and calls serverless inference.
Serverless Function: Processes inference using Hugging Face API.
Object Storage: Stores user interactions.
Getting Started
Prerequisites
Vultr Account: Compute instance and access to Serverless and Object Storage.
Server Software: PHP, Python, Composer, Nginx.
Setup Instructions
Clone the Repository:

git clone https://github.com/shravani-sys/Vultr-Hackathon.git
cd Vultr-Hackathon
Install Python Requirements:


pip3 install -r requirements.txt
Run Python Application:


python3 app.py
Set Up Laravel Application:

Move to Laravel directory:

cd /var/www
composer create-project --prefer-dist laravel/laravel chatbot-app
cd chatbot-app
Configure .env with the necessary environment settings:
dotenv

APP_NAME=Chatbot
APP_ENV=production
APP_URL=http://your_server_ip
Add Chatbot API Route in Laravel:

Open routes/api.php and add:

Route::post('/infer', [ChatbotController::class, 'infer']);
Create Chatbot Controller:

Generate the controller and update ChatbotController.php to use Vultr’s serverless function for inference:

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ChatbotController extends Controller
{
    public function infer(Request $request)
    {
        $userMessage = $request->input('message');
        $response = Http::post('YOUR_SERVERLESS_URL', [
            'message' => $userMessage,
        ]);

        return response()->json($response->json());
    }
}
Configure Nginx for PHP and Python Applications:

Create and configure /etc/nginx/sites-available/vultr-app:

server {
    listen 80;
    server_name your_server_ip;

    location / {
        root /var/www/chatbot-app/public;
        index index.php index.html;
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    location /python {
        proxy_pass http://127.0.0.1:5000;
    }
}
Restart Nginx:

sudo systemctl restart nginx
Testing the Application:

Send a POST request to test the /api/infer endpoint:

curl -X POST http://your_server_ip/api/infer -H "Content-Type: application/json" -d '{"message": "Hello"}'

#Technical Documentation
See the PDF documentation for architecture details, setup instructions, and API specifications.
