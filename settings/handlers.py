from logging import Handler
from django.core.exceptions import AppRegistryNotReady
import traceback
from django.utils import timezone
import re
import uuid


class DBHandler(Handler):
    def emit(self, record):
        try:
            from error_logger.models import Log

            if record.exc_info:
                path = None
                line_number = None
                error_message = None
                traceback_log = None
                error_line = None
                method = None
                status_code = None
                user_id = None

                traceback_details = traceback.format_tb(record.exc_info[2])
                pattern = r'File "(.*)", line (\d+),'
                traceback_error_line=traceback_details[-1].strip()
                match = re.search(pattern, traceback_error_line)
                error_line = traceback_error_line.split('\n')[-1].strip()
                if match:
                    path = match.group(1)
                    line_number = match.group(2)
                error_message=str(record.exc_info[1]) if record.exc_info[1] else None
                traceback_log=''.join(traceback_details).strip()

                if hasattr(record, 'request') and hasattr(record.request, 'method'):
                    method = record.request.method
                    user_id = int(uuid.UUID(str(record.request.user.id)).int) if record.request.user.is_authenticated else None
                    status_code = record.status_code
                # create log object
                log = Log(
                    user_id=user_id,
                    level=record.levelname,
                    log_message=record.getMessage(),
                    error_message=error_message,
                    error_line=error_line,
                    traceback=traceback_log,
                    path=path,
                    line_number=line_number,
                    method=method,
                    status_code=status_code,
                    time=timezone.now()
                )
                # save log
                log.save()
        except AppRegistryNotReady:
            pass
