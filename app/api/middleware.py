from app.core.app_state import AppState


def cache(request, next, **kwargs):
    app_data: AppState = request.app_data

    uri = request.uri
    method = request.method
    body = request.body

    key = f"{method}/{uri}/{body}"
    if response := app_data.caches.get(key, None):
        return response
    else:
        response = next(request, **kwargs)
        app_data.caches[key] = response
        return response
