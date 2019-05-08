logs_urlparterns = []


from .urls.log_view_urls import logsearch_urlparterns
logs_urlparterns.extend(logsearch_urlparterns)


from .urls.seclog_search_url import seclog_search_urlparterns
logs_urlparterns.extend(seclog_search_urlparterns)