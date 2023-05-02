from logging import Handler
from django.core.exceptions import AppRegistryNotReady
import traceback
from django.utils import timezone
import re
import uuid


class DBHandler(Handler):
    def emit(self, record):
        level = record.levelname
        # if level =='INFO':
        #     self.saveInfoLog(record, level)

        # elif level in ['ERROR', 'WARNING']:
        #     self.saveErrorLog(record, level)
        if level == 'ERROR':
            self.saveErrorLog(record, level)

    def saveErrorLog(self, record, level):
        try:
            from error_logger.models import Log
            path = None
            line_number = None
            error_message = None
            traceback_log = None
            error_line = None
            method = None
            status_code = None
            user_id = None

            if hasattr(record, 'exc_info'):
                if record.exc_info:
                    traceback_details = traceback.format_tb(record.exc_info[2])
                    pattern = r'File "(.*)", line (\d+),'
                    traceback_error_line = traceback_details[-1].strip()
                    match = re.search(pattern, traceback_error_line)
                    error_line = traceback_error_line.split('\n')[-1].strip()

                    if match:
                        path = match.group(1)
                        line_number = match.group(2)

                    error_message = str(record.exc_info[1]) if record.exc_info[1] else None
                    traceback_log = ''.join(traceback_details).strip()

            if hasattr(record, 'request'):
                if hasattr(record.request, 'method'):
                    method = record.request.method

                if hasattr(record.request, 'user') and record.request.user.is_authenticated:
                    user_id = record.request.user

            if hasattr(record, 'status_code'):
                status_code = record.status_code

            log = Log(
                user_id=user_id,
                level=level,
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

            log.save()
        except Exception as e:
            print(e)

    # def saveInfoLog(self, record, level):
    #     try:
    #         from error_logger.models import Log
    #         path = record.pathname
    #         line_number = record.lineno
    #         error_message = None
    #         traceback_log = record.args[0]
    #         error_line = None
    #         method = None
    #         status_code = None
    #         user_id = None

    #         if hasattr(record, 'request'):
    #             if hasattr(record.request, 'method'):
    #                 method = record.request.method

    #             if hasattr(record.request, 'user') and record.request.user.is_authenticated:
    #                 user_id = int(uuid.UUID(str(record.request.user.id)).int) if record.request.user.is_authenticated else None
    #         if hasattr(record, 'status_code'):
    #             status_code = record.status_code

    #         log = Log(
    #             user_id=user_id,
    #             level=level,
    #             log_message=record.getMessage(),
    #             error_message=error_message,
    #             error_line=error_line,
    #             traceback=traceback_log,
    #             path=path,
    #             line_number=line_number,
    #             method=method,
    #             status_code=status_code,
    #             time=timezone.now()
    #         )
    #         log.save()

    #     except Exception as e:
    #         print(e)
