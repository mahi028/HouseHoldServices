from flask_excel import make_response_from_query_sets
from application.modals import ServiceRequest, Customer
from flask import jsonify, current_app as app, render_template
from flask_mail import Message
from application import mail
from pdf_reports import write_report
from datetime import date 
from celery import shared_task
from uuid import uuid4
import os, shutil

@shared_task(ignore_result = False)
def makeServiceReport():
    service_requests = ServiceRequest.query.all()
    column_names= [ 'rqst_id', 'cust_id', 'serv_pro_id', 'serv_id', 'status', 'service_msg', 'created_at', 'updated_at', 'completed_at', 'total_cost' ]

    uid = str(uuid4())
    file_name = f'serviceReport_{uid}'
    file_path = f'application/static/reports/{file_name}.csv'
    saved_file_path = f'static/reports/{file_name}.csv'
    excelFile = make_response_from_query_sets(service_requests, column_names=column_names, file_type='csv', status=200, file_name=file_name)

    with open(file_path, "wb") as fh:
        fh.write(excelFile.data)

    return saved_file_path


@shared_task(ignore_result = True)
def sendMonthlyReport():
    """Currently sending emails from https://mailtrap.io/inboxes/3297649/messages ."""

    customers = Customer.query.all()       
    if not customers:
        return jsonify({"msg":"CustomersNotFound"})
    
    with mail.connect() as conn:
        for customer in customers:
            report_date=date.today()     
            html_content = render_template('monthlyReport.html', customer=customer, report_date=report_date)

            report_name = f"application/static/reports/montlyReport_{customer.user.name}_{report_date}.pdf"
            report_path = f"static/reports/montlyReport_{customer.user.name}_{report_date}.pdf"

            write_report(html_content, report_name)
            msg = Message(
                subject=f"hello, {customer.user.name}",
                html= html_content,
                recipients=[customer.user.email],
            )

            #pdf attachments
            with app.open_resource(report_path) as fp:
                msg.attach("Customer Monthly Report", "invoice/pdf", fp.read())

            conn.send(msg)
    
@shared_task(ignore_result = True)    
def sendDailyReminder():
    rqsts = ServiceRequest.query.filter_by(status = "Pending").group_by(ServiceRequest.serv_pro_id).all()
 
    with mail.connect() as conn:
        for rqst in rqsts:
            msg = Message(
                subject=f"Reminder to check new/pending service requests",
                body= f"Hello {rqst.service_pro.user.name}, You have new/pending requests. Please check them.",
                recipients=[rqst.service_pro.user.email],
            )
            conn.send(msg)

@shared_task(ignore_result = True)
def removeReports():
    folder = 'application/static/reports'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')