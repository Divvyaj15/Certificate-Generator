from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField
from wtforms.validators import DataRequired, Email
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

class CertificateForm(FlaskForm):
    recipient_name = StringField('Recipient Name', validators=[DataRequired()])
    recipient_email = EmailField('Recipient Email', validators=[DataRequired(), Email()])
    event_name = StringField('Event/Course Name', validators=[DataRequired()])
    completion_date = DateField('Date of Completion', validators=[DataRequired()])

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h

def generate_certificate(form_data):
    # Certificate image size
    width, height = 1200, 900
    background_color = (255, 255, 255)
    border_color = (44, 62, 80)
    text_color = (44, 62, 80)
    accent_color = (231, 76, 60)
    
    # Create image
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_width = 10
    draw.rectangle([(border_width, border_width), (width-border_width, height-border_width)], outline=border_color, width=border_width)
    
    # Load fonts (ensure you have these fonts or use default)
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
        name_font = ImageFont.truetype("arialbd.ttf", 48)
        text_font = ImageFont.truetype("arial.ttf", 32)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Certificate number
    certificate_number = str(uuid.uuid4())[:8].upper()
    
    # Draw seal
    seal_radius = 60
    seal_x, seal_y = width - 120, 120
    draw.ellipse([(seal_x-seal_radius, seal_y-seal_radius), (seal_x+seal_radius, seal_y+seal_radius)], fill=accent_color)
    draw.text((seal_x-35, seal_y-20), "SEAL", font=small_font, fill=(255,255,255))
    
    # Draw certificate number
    draw.text((60, 60), f"Certificate No: {certificate_number}", font=small_font, fill=(120,120,120))
    
    # Draw title
    title = "CERTIFICATE OF ACHIEVEMENT"
    w, h = get_text_size(draw, title, title_font)
    draw.text(((width-w)//2, 160), title, font=title_font, fill=text_color)
    
    # Subtitle
    subtitle = "This is to certify that"
    w, h = get_text_size(draw, subtitle, subtitle_font)
    draw.text(((width-w)//2, 260), subtitle, font=subtitle_font, fill=(127,140,141))
    
    # Recipient name
    name = form_data['recipient_name']
    w, h = get_text_size(draw, name, name_font)
    draw.text(((width-w)//2, 320), name, font=name_font, fill=text_color)
    
    # Completion text
    completion_text = "has successfully completed the course"
    w, h = get_text_size(draw, completion_text, text_font)
    draw.text(((width-w)//2, 400), completion_text, font=text_font, fill=text_color)
    
    # Event/Course name
    event = f"Course Name: {form_data['event_name']}"
    w, h = get_text_size(draw, event, text_font)
    draw.text(((width-w)//2, 460), event, font=text_font, fill=text_color)
    
    # Date of completion
    date = f"Date of Completion: {form_data['completion_date']}"
    w, h = get_text_size(draw, date, text_font)
    draw.text(((width-w)//2, 510), date, font=text_font, fill=text_color)
    
    # Issue date
    issue_date = f"Date: {datetime.now().strftime('%B %d, %Y')}"
    w, h = get_text_size(draw, issue_date, small_font)
    draw.text(((width-w)//2, 560), issue_date, font=small_font, fill=text_color)
    
    # Signatures
    draw.line([(300, 700), (500, 700)], fill=border_color, width=3)
    draw.text((340, 710), "Course Director", font=small_font, fill=text_color)
    draw.line([(700, 700), (900, 700)], fill=border_color, width=3)
    draw.text((760, 710), "Institution Head", font=small_font, fill=text_color)
    
    # Save image
    output_path = os.path.join(app.root_path, 'static', 'generated', f"certificate_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

def send_certificate_email(recipient_email, certificate_path):
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Your Certificate of Achievement'
    body = """
    Dear Recipient,\n\nCongratulations! Your certificate has been generated successfully.\nPlease find your certificate attached to this email.\n\nBest regards,\nCertificate Generator Team
    """
    msg.attach(MIMEText(body, 'plain'))
    with open(certificate_path, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype='png')
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(certificate_path))
        msg.attach(attach)
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email credentials and ensure you're using an App Password if using Gmail.")
        return False
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CertificateForm()
    if form.validate_on_submit():
        form_data = {
            'recipient_name': form.recipient_name.data,
            'recipient_email': form.recipient_email.data,
            'event_name': form.event_name.data,
            'completion_date': form.completion_date.data.strftime('%B %d, %Y')
        }
        try:
            certificate_path = generate_certificate(form_data)
            if send_certificate_email(form_data['recipient_email'], certificate_path):
                flash(f'Certificate sent successfully to {form_data["recipient_email"]}', 'success')
            else:
                flash('Error sending email. Please try again.', 'error')
        except Exception as e:
            flash(f'Error generating certificate: {str(e)}', 'error')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) 