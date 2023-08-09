class Status:
    # https://restfulapi.net/http-status-codes/
    # 1xx: Informational – Communicates transfer protocol-level information.
    # 2xx: Success – Indicates that the client’s request was accepted successfully.
    # 3xx: Redirection – Indicates that the client must take some additional action in order to complete their request.
    # 4xx: Client Error – This category of error status codes points the finger at clients.
    # 5xx: Server Error – The server takes responsibility for these error status codes.

    # Usage for flask:
    # return jsonify(Status.OK), Status.OK["code"]

    # Indicates that the request has succeeded.
    OK = {"code": 200, "message": "Ok"}

    # Indicates that the request has been received but not completed yet. 
    # It is typically used in log running requests and batch processing.
    ACCEPTED = {"code": 202, "message": "Accepted"}

    # The server has fulfilled the request but does not need to return a response body.
    NO_CONTENT = {"code": 204, "message": "No Content"}

    # The URL of the requested resource has been changed permanently. 
    # The new URL is given by the Location header field in the response. 
    # This response is cacheable unless indicated otherwise.
    MOVED_PERMANENTLY = {"code": 301, "message": "Moved Permanently"}

    # The response can be found under a different URI and SHOULD be retrieved using a GET method on that resource.
    SEE_OTHER = {"code": 303, "message": "See Other"}

    # The request could not be understood by the server due to incorrect syntax. 
    # The client SHOULD NOT repeat the request without modifications.
    BAD_REQUEST = {"code": 400, "message": "Bad Request"}

    # Indicates that the request requires user authentication information. 
    # The client MAY repeat the request with a suitable Authorization header field
    UNAUTHORIZED = {"code": 401, "message": "Unauthorized"}

    # Reserved for future use. It is aimed for using in the digital payment systems.
    PAYMENT_REQUIRED = {"code": 402, "message": "Payment Required"}

    # Unauthorized request. The client does not have access rights to the content. 
    # Unlike 401, the client’s identity is known to the server.
    FORBIDDEN = {"code": 403, "message": "Forbidden"}

    # The server can not find the requested resource.
    NOT_FOUND = {"code": 404, "message": "Not Found"}

    # The server understands the content type and syntax of the request entity, 
    # but still server is unable to process the request for some reason.
    UNPROCESSABLE_ENTITY = {"code": 422, "message": "Unprocessable Entity"}
    
    # The resource that is being accessed is locked.
    LOCKED = {"code": 423, "message": "Locked"}

    # The user has sent too many requests in a given amount of time (“rate limiting”).
    TOO_MANY_REQUESTS = {"code": 429, "message": "Too Many Requests"}

    # The server encountered an unexpected condition that prevented it from fulfilling the request.
    INTERNAL_SERVER_ERROR = {"code": 500, "message": "Internal Server Error"}

    # The HTTP method is not supported by the server and cannot be handled.
    NOT_IMPLEMENTED = {"code": 501, "message": "Not Implemented"}