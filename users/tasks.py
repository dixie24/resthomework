from celery import shared_task
import time 
import logging
from django.core.mail import send_mail 

logger = logging.getLogger(__name__)


@shared_task
def process_uploaded_csv(file_path, user_id):

    logger.info(f"Начало обработки файла: {file_path} для пользователя {user_id}")
    
    time.sleep(15) 
    logger.info(f"Файл {file_path} успешно обработан. Результаты сохранены.")
    return f"Обработка завершена для пользователя {user_id}"


@shared_task
def cleanup_expired_sessions(limit):
    deleted_count = 55 
    
    logger.info(f"Очистка завершена. Удалено {deleted_count} устаревших записей. Лимит: {limit}")
    return f"Удалено записей: {deleted_count}"


@shared_task
def send_weekly_report(recipient_email, report_name):
    subject = f"Еженедельный отчет: {report_name}"
    message = f"Здравствуйте, ваш отчет '{report_name}' готов. Вы можете скачать его по ссылке..."
    time.sleep(3) 

    try:
        send_mail(
            subject,
            message,
            'noreply@shopapi.com', 
            [recipient_email],    
            fail_silently=False,
        )
        logger.info(f"Отчет {report_name} успешно отправлен на {recipient_email}")
        return "Email sent successfully"
    except Exception as e:
        logger.error(f"Ошибка при отправке отчета {report_name}: {e}")
        raise