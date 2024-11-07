import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import pandas as pd


class EmailSender:
    def __init__(self, mail_config):
        self.mail_config = mail_config
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            undefined=StrictUndefined,
            cache_size=0
        )

    def generate_sample_rows_html(self,df):
        """Generate HTML for the first 10 rows of the DataFrame."""
        sample_df = df.head(10)
        return sample_df.to_html(index=False)

    def render_template(self, template_name):
        try:
            # Load and render the template with placeholders
            template = self.env.get_template(template_name)

            # Generate the sample rows HTML
            source_table = self.mail_config["templatePlaceHolder"]["dataframe"]["source_table"]
            sample_rows_html = self.generate_sample_rows_html(source_table)

            # Merge placeholders with sample_rows_html
            rendered_content = template.render(**self.mail_config,
                                               sample_rows_html=sample_rows_html)

            return rendered_content
        except Exception as e:
            print(f"Error rendering template: {e}")
            raise

    def send_email(self):
        subject = self.mail_config["mail_subject"]
        recipient_list = self.mail_config["mail_to"]
        template_name = self.mail_config['template_name']

        try:
            # Render the template with placeholders
            html_content = self.render_template(template_name)
        except Exception as render_error:
            print(f"Failed to render template due to missing placeholder: {render_error}")
            return

        # Construct the email
        msg = MIMEMultipart()
        msg["From"] = self.mail_config["mail_from"]
        msg["To"] = ", ".join(recipient_list)
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        # Use SMTP server details if provided, otherwise attempt to use local SMTP server
        if self.mail_config["send_method"] == "SMTP":
            smtp_params = self.mail_config["smtp_params"]
            smtp_server = smtp_params["mail_host"]
            smtp_port = smtp_params["port"]
            username = smtp_params["username"]
            password = smtp_params["password"]

            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(username, password)
                    server.sendmail(msg["From"], recipient_list, msg.as_string())
                print("Email sent successfully using external SMTP.")
            except Exception as e:
                print(f"Failed to send email using SMTP. Error: {e}")
        else:
            print("Only SMTP method is supported on Windows.")

