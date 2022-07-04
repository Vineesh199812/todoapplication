# authentication

# login

# view for listing all todos

# view creating a new todo

# view for fetching a specific todo

# list all todos created by authenticated user

# view for updating a specific todo

# logout
from DJANGO__.Todosapp.models import users,todos

def signin_required(fn):
    def wrapper(*args, **kwargs):
        if "user" in session:
            return fn(*args, **kwargs)
        else:
            print("u must login")
    return wrapper

session = {}

def authenticate(**kwargs):
    username = kwargs.get("username")
    password = kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user

class Signinview:
    username: str
    password: str

    def todos(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        user = authenticate(username=username, password=password)
        if user:
            session["user"] = user[0]
            print("success")

        else:
            print("invalid")

class Todosview():
    @signin_required
    def get(self, *args, **kwargs):
        return todos

    @signin_required
    def post(self, *args, **kwargs):
        print(kwargs)
        userId = session["user"]["id"]
        kwargs["userId"] = userId
        todos.append(kwargs)
        print(todos)



class Mytodoslistview():
    @signin_required
    def get(self, *args, **kwargs):
        print(session)
        userId = session["user"]["id"]
        print(userId)
        my_todos = [post for post in todos if post["userId"] == userId]
        return my_todos

class tododetails():
    def get_object(self, todo_id):
        todo = [todo for todo in todos if todo["todoId"] == todo_id]
        return todo

    @signin_required
    def get(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        todo = self.get_object(todo_id)
        return todo

    @signin_required
    def delete(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        data = self.get_object(todo_id)
        if data:
            todo = data[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))
            for t in todos:
                print(t)

    @signin_required
    def put(self, *args, **kwargs):
        todo_id = kwargs.get("todo_id")
        data = kwargs.get("data")
        instance = self.get_object(todo_id)
        if instance:
            todo_obj = instance[0]
            todo_obj.update(data)
            return todo_obj

def logout():
    if "user" in session:
         session.pop("user")
         print("user logged out")
    else:
        print("u must login")

login=Signinview()
login.todos(username="akhil",password="Password@123")
#login.todos(username="nikil",password="Password@123")

view= Mytodoslistview()
print(view.get())

print(session)
data=Todosview()
print(data.get())
data.post(todoId=9,
         task_name="water_bill",
         completed=True)

myposts = Mytodoslistview()
print(myposts.get())

todo_detail = tododetails()
print(todo_detail.get(todo_id=6))

todo_detail = tododetails()
#print(todo_detail.get(todo_id=6))
todo_detail.delete(todo_id=6)

data = {
    "task_name":"newbill",
    "completed":True
}
tododetails = tododetails()
print(tododetails.put(todo_id=1, data=data))

logout()