def safe_run(function, *args, fallback=None, **kwargs):
    try:
        return function(*args, **kwargs)

    except Exception as e:
        return fallback or {
            "error": True,
            "reason": str(e)
        }