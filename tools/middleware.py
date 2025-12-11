from django.conf import settings
import time
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
import re
import traceback


def format_sql(sql):
    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'ORDER BY', 'GROUP BY', 'LIMIT']
    sql = sql.strip()
    for kw in keywords:
        sql = re.sub(r'\s+' + kw + r'\s+', f'\n{kw} ', sql, flags=re.IGNORECASE)
    return sql.strip()

def PrintDetails(queries):
    print('='*60)
    for i, query in enumerate(queries, 1):
        sql = query['sql']
        time_taken = query.get('time', '?.??')
        # where the sql triggered
        
        print(f"\n--- Query {i} ({time_taken}s) ---")
        print(sql)
        print(format_sql(sql))


def print_duplicated_query_details(duplicated_queries, all_queries):
    """
    Prints the details for queries that were identified as duplicates.
    """
    print("=" * 25 + " DUPLICATE QUERIES " + "=" * 25)

    # Keep track of printed SQL to avoid re-printing the header for the same query
    printed_sql = set()

    for i, query in enumerate(all_queries):
        sql = query['sql']
        # Check if this specific SQL is in our list of duplicates and hasn't been detailed yet
        if sql in duplicated_queries and sql not in printed_sql:
            count = duplicated_queries[sql]

            print(f"\n--- Query executed {count} times ---")
            print(format_sql(sql))

            # Now find all occurrences of this query to show their individual tracebacks
            print("\nLocations:")
            location_number = 1
            for inner_query in all_queries:
                if inner_query['sql'] == sql:
                    stack_trace = inner_query.get('stack_trace', [])
                    time_taken = inner_query.get('time', 'N/A')

                    if stack_trace:
                        # The last item in the filtered stack is usually the most relevant application code
                        relevant_call = stack_trace[-1]
                        print(f"  {location_number}. (Took {time_taken}s) {relevant_call.filename}, line {relevant_call.lineno}, in {relevant_call.name}")
                    else:
                        print(f"  {location_number}. (Took {time_taken}s) Stack trace not available.")
                    location_number += 1

            printed_sql.add(sql)
        
    
    
class QueryCountDebugMiddleware(MiddlewareMixin):
    """
    This middleware logs duplicate database queries during a request-response cycle.
    It captures the stack trace at the point of execution to identify the origin of each query.
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def _capture_stack_trace(self, execute, sql, params, many, context):
        """
        This method is a wrapper around the database query execution.
        It captures a stack trace and filters it to find the relevant
        application code that triggered the query.
        """
        stack = traceback.extract_stack()
        # Filter out frames from Django's own database wrappers to find the app-level code
        filtered_stack = [
            frame for frame in stack 
            if 'django/db' not in frame.filename and 'middleware' not in frame.filename
        ]
        context['stack_trace'] = filtered_stack
        return execute(sql, params, many, context)

    def __call__(self, request):
        if not settings.DEBUG:
            return self.get_response(request)

        start_time = time.time()

        # Use the execute_wrapper to run our _capture_stack_trace method for every query
        with connection.execute_wrapper(self._capture_stack_trace):
            response = self.get_response(request)

        duration = time.time() - start_time
        queries = connection.queries
        query_count = len(queries)

        # Count occurrences of each query
        query_frequency = defaultdict(int)
        for query in queries:
            print(query['sql'])
            query_frequency[query['sql']] += 1

        duplicated_queries = {sql: count for sql, count in query_frequency.items() if count > 1}

        # Overall summary
        if query_count > 0:
            print('=' * 30)
            print(f"==> Total Queries: {query_count} | Duplicates: {len(duplicated_queries)} | Duration: {duration:.2f}s Request: {request.method} {request.path}")

            if duplicated_queries:
                # If there are duplicates, print their detailed information
                print_duplicated_query_details(duplicated_queries, queries)

            print('=' * 30)

        return response