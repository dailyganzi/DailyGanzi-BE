from fastapi import Body: FastAPI의 Body 모듈은 요청 본문(body)에 있는 데이터를 처리하는 데 사용됩니다. HTTP POST 또는 PUT 요청과 함께 전달된 데이터를 읽어오는 데에 쓰이며, FastAPI의 경로 연산자로 사용될 수 있습니다.

from fastapi import Request: FastAPI의 Request 모듈은 HTTP 요청(request)에 대한 정보를 다루는 데 사용됩니다. 클라이언트로부터 받은 요청의 헤더, 쿼리 매개변수, 요청 본문 등의 정보를 접근하는데 활용됩니다.

from fastapi import HTTPException: FastAPI의 HTTPException 모듈은 예외 처리를 위해 사용됩니다. 예외 상황이 발생할 때, 즉각적으로 사용자에게 HTTP 응답을 반환하는데 사용됩니다. 예를 들어, 올바르지 않은 요청을 받았을 때 400 Bad Request, 권한이 없는 요청일 때 403 Forbidden 등의 상태 코드와 함께 예외를 발생시켜 사용자에게 적절한 응답을 제공할 수 있습니다.

from fastapi import status: FastAPI의 status 모듈은 HTTP 상태 코드를 정의하는 데 사용됩니다. 예를 들어, status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND와 같은 상태 코드들이 있으며, 이를 사용하여 HTTP 응답을 생성할 수 있습니다.