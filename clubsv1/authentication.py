from .models import Student, Faculty
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import jwt


class StudentUserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            print("User inside the authenticate")
            token = get_authorization_header(request).decode("utf-8").split()
            if len(token) == 2:
                de_value = jwt.decode(token[1], "student_key", algorithms=["HS256"])
                admin = Student.objects.filter(id=de_value["id"])
                
                if admin.exists():
                    return admin, de_value["role"]
                else:
                    raise AuthenticationFailed("Token authentication failed.")
            else:
                raise AuthenticationFailed("Token authentication failed.")
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise AuthenticationFailed("Token authentication failed.")
        except Exception:
            raise AuthenticationFailed("Token authentication failed.")
        
class FacultyTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            print("Faculty inside the authenticate")
            token = get_authorization_header(request).decode("utf-8").split()
            if len(token) == 2:
                de_value = jwt.decode(token[1], "faculty_key", algorithms=["HS256"])
                admin = Faculty.objects.filter(id=de_value["id"])
                
                if admin.exists():
                    return admin, de_value["role"]
                else:
                    raise AuthenticationFailed("Token authentication failed.")
            else:
                raise AuthenticationFailed("Token authentication failed.")
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise AuthenticationFailed("Token authentication failed.")
        except Exception:
            raise AuthenticationFailed("Token authentication failed.")
        
class HOCTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            print("HOC inside the authenticate")
            token = get_authorization_header(request).decode("utf-8").split()
            if len(token) == 2:
                de_value = jwt.decode(token[1], "hoc_key", algorithms=["HS256"])
                admin = Faculty.objects.filter(id=de_value["id"])
                
                if admin.exists():
                    return admin, de_value["role"]
                else:
                    raise AuthenticationFailed("Token authentication failed.")
            else:
                raise AuthenticationFailed("Token authentication failed.")
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            raise AuthenticationFailed("Token authentication failed.")
        except Exception:
            raise AuthenticationFailed("Token authentication failed.")