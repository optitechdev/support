#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import functools
import logging

# Konfigurera performance logging
perf_logger = logging.getLogger('performance')
perf_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('⚡ %(asctime)s - %(message)s')
handler.setFormatter(formatter)
perf_logger.addHandler(handler)

def monitor_performance(func_name=None):
    """Decorator för att mäta funktionsprestation"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                
                name = func_name or func.__name__
                if duration > 10:  # Varna för långsamma anrop
                    perf_logger.warning(f"🐌 LÅNGSAM: {name} tog {duration:.2f}s")
                elif duration > 5:
                    perf_logger.info(f"⚠️  {name} tog {duration:.2f}s")
                else:
                    perf_logger.info(f"✅ {name} tog {duration:.2f}s")
                
                return result
            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                name = func_name or func.__name__
                perf_logger.error(f"❌ {name} misslyckades efter {duration:.2f}s: {str(e)}")
                raise
        return wrapper
    return decorator

class PerformanceTracker:
    """Klass för att spåra AI-prestanda"""
    
    def __init__(self):
        self.response_times = []
        self.error_count = 0
        self.total_requests = 0
    
    def log_response_time(self, duration, success=True):
        """Logga svarstid för AI-anrop"""
        self.total_requests += 1
        if success:
            self.response_times.append(duration)
        else:
            self.error_count += 1
    
    def get_stats(self):
        """Få prestandastatistik"""
        if not self.response_times:
            return {
                "avg_response_time": 0,
                "success_rate": 0,
                "total_requests": self.total_requests,
                "error_count": self.error_count
            }
        
        avg_time = sum(self.response_times) / len(self.response_times)
        success_rate = (len(self.response_times) / self.total_requests) * 100
        
        return {
            "avg_response_time": round(avg_time, 2),
            "success_rate": round(success_rate, 1),
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "fastest": round(min(self.response_times), 2),
            "slowest": round(max(self.response_times), 2)
        }
    
    def print_stats(self):
        """Skriv ut prestandastatistik"""
        stats = self.get_stats()
        print(f"\n📊 AI Prestandastatistik:")
        print(f"   Genomsnittlig svarstid: {stats['avg_response_time']}s")
        print(f"   Framgångsfrekvens: {stats['success_rate']}%")
        print(f"   Totala förfrågningar: {stats['total_requests']}")
        print(f"   Fel: {stats['error_count']}")
        if stats['avg_response_time'] > 0:
            print(f"   Snabbaste: {stats['fastest']}s")
            print(f"   Långsammaste: {stats['slowest']}s")

# Global prestandaspårare
tracker = PerformanceTracker()
