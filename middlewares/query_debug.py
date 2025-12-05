import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.db import connection, reset_queries
from django.conf import settings

class SimpleDebugMiddleware(MiddlewareMixin):
    """
    Middleware đơn giản để debug performance
    In ra console mỗi request
    """

    def process_request(self, request):
        """Bắt đầu đếm thời gian"""
        request._start_time = time.time()
        reset_queries()

    def process_response(self, request, response):
        """In thống kê sau khi response"""

        # Tính thời gian
        if hasattr(request, '_start_time'):
            duration_ms = (time.time() - request._start_time) * 1000

            # Đếm queries
            queries = connection.queries
            num_queries = len(queries)
            query_time_ms = sum(float(q['time']) * 1000 for q in queries)

            # Màu sắc cho output
            if duration_ms < 200:
                color = '\033[92m'  # Green
            elif duration_ms < 500:
                color = '\033[93m'  # Yellow
            else:
                color = '\033[91m'  # Red

            reset = '\033[0m'

            # In ra console
            print(f"\n{'='*70}")
            print(f"{color}[{request.method}] {request.path}{reset}")
            print(f"{'='*70}")
            print(f"⏱️  Response Time: {color}{duration_ms:.0f}ms{reset}")
            print(f"🔍 Queries: {num_queries}")
            print(f"⚡ Query Time: {query_time_ms:.0f}ms")
            print(f"🐍 Python Time: {duration_ms - query_time_ms:.0f}ms")
            print(f"📊 Status: {response.status_code}")

            # Cảnh báo nếu chậm
            if duration_ms > 500:
                print(f"\n⚠️  WARNING: SLOW REQUEST (>{duration_ms:.0f}ms)")

            if num_queries > 20:
                print(f"⚠️  WARNING: TOO MANY QUERIES ({num_queries})")

            # Hiện slow queries (>50ms)
            slow_queries = [q for q in queries if float(q['time']) * 1000 > 50]
            if slow_queries:
                print(f"\n🐢 SLOW QUERIES (>50ms):")
                for i, q in enumerate(slow_queries[:5], 1):
                    time_ms = float(q['time']) * 1000
                    sql = q['sql'][:100] + '...' if len(q['sql']) > 100 else q['sql']
                    print(f"   {i}. [{time_ms:.0f}ms] {sql}")

            # Detect duplicate queries (N+1)
            sql_list = [q['sql'] for q in queries]
            duplicates = {}
            for sql in set(sql_list):
                count = sql_list.count(sql)
                if count > 1:
                    duplicates[sql[:80]] = count

            if duplicates:
                print(f"\n⚠️  DUPLICATE QUERIES DETECTED (Possible N+1):")
                for sql, count in list(duplicates.items())[:3]:
                    print(f"   [{count}x] {sql}...")

            print(f"{'='*70}\n")

        return response