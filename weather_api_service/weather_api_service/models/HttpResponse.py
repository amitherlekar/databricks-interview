class HttpResponse:
    status: int
    message: str
    data: any
    has_more: bool
    totalCount: int
    session_token: str

    def __init__(self, message = None, status = None, data = None, has_more = False, totalCount = None, session_token = None) -> None:
        self.message = message
        self.status = status
        self.data = data
        self.has_more = has_more
        self.totalCount = totalCount
        self.session_token = session_token
    