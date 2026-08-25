def print_stats(host, last, uptime_1h, uptime_24h):
    if last:
        last_time = last[0]
        last_status = 'OK' if last[1] else 'FAIL'
        last_latency = f"{last[2]} ms" if last[2] is not None else '---'
    print("\n" + "="*50)
    print ()
              