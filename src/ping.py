from ping3 import ping

def ping_host(host, timeout=2):
    try:
        response = ping(host, timeout=timeout)
        if response is not None:
            return round(response * 1000, 2)
        return None
    except Exception:
        return None