# Certificate Generator Web Application

A Python-based web application that allows users to generate and send personalized certificates via email.

## Features

- Clean and modern web interface
- Multiple certificate templates
- Automatic email delivery
- Form validation
- Responsive design

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd certificate_generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key-here
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Note: If using Gmail, you'll need to generate an App Password for your account.

## Running the Application

1. Generate the certificate templates:
```bash
python create_templates.py
```

2. Start the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Fill in the recipient's details:
   - Name
   - Email address
   - Event/Course name
   - Completion date

2. Select a certificate template

3. Click "Generate & Send Certificate"

4. The certificate will be generated and sent to the recipient's email address

## Project Structure

```
certificate_generator/
├── app.py                 # Main Flask application
├── create_templates.py    # Script to generate certificate templates
├── static/
│   ├── images/           # Certificate templates
│   └── generated/        # Generated certificates
├── templates/
│   └── index.html        # Main web interface
└── README.md             # Project documentation
```

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables for sensitive information
- Generate a strong SECRET_KEY for your application
- Use app-specific passwords for email accounts

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
