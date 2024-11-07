import pandas as pd
from datetime import datetime
import uuid
from email_sender_new import EmailSender

# Define the CSV file paths
source_csv_path = 'source_data.csv'
target_csv_path = 'target_data.csv'


def transfer_data():
    """Simulate data transfer from source_data.csv to target_data.csv, returning job status, row count, and error message."""
    try:
        # Read data from source CSV
        global source_df
        source_df = pd.read_csv(source_csv_path)

        # Write data to target CSV (overwrite if exists)
        source_df.to_csv(target_csv_path, index=False)

        # Calculate row count and sum of balances
        row_count = source_df.shape[0]
        balance_sum = source_df['Balance'].sum() if 'Balance' in source_df.columns else None

        return True, row_count, "", balance_sum
    except Exception as e:
        # If an error occurs, return failure, None for row count, and the error message
        return False, None, str(e), None


def send_email_notification():
    """Generate job details, send email based on the transfer operation's success or failure, and include table data sample."""
    # Define job details
    job_id = str(uuid.uuid4())[:8]
    #job_name = "Data Transfer Job"
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Attempt data transfer and capture status, row count, balance sum, and any error
    success, row_count, error_message, balance_sum = transfer_data()
    job_status = "Success" if success else "Failed"
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load a 10-row sample of the target table for the email
    target_df = pd.read_csv(target_csv_path)
    #sample_rows_html = target_df.head(10).to_html(index=False)

    # Prepare email configuration and placeholders
    mail_config = {
        "mail_from": "vishwashah1104@gmail.com",
        "mail_to": ["heetshah381997@gmail.com"],
        "smtp_params": {
            "mail_host": "smtp.gmail.com",
            "port": 465,
            "username": "vishwashah1104@gmail.com",
            "password": "vypuwcsdtxxpwsgx"  # Replace with an app-specific password if using Gmail
        },
        "mail_subject": "Data Transfer",
        "send_method": "SMTP",
        "template_name":"success_template.html",
        "templatePlaceHolder": {
            "job_name": "Vijay",
            "job_id": 'hckps2121',
            "job_status": 'Success',
            "job_started_on": start_time,
            "job_ended_on": end_time,
            "row_count": row_count,
            "balance_sum": balance_sum,
            "dataframe": {
                "source_table": source_df,


            }
        }
    }

    # Initialize and send the email
    email_sender = EmailSender(mail_config)
    email_sender.send_email()


# Run the function to send an email notification
if __name__ == "__main__":
    send_email_notification()
