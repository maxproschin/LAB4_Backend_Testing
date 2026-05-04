from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Дозволяє запити з будь-якого сайту (в т.ч. з нашого localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = []
posts_db = []
comments_db = []


class User(BaseModel):
    id: int
    name: str
    email: str


class Post(BaseModel):
    id: int
    title: str
    content: str
    authorId: int
    createdAt: datetime = datetime.now()


class Comment(BaseModel):
    id: int
    text: str
    userId: int
    postId: int


class UserCreate(BaseModel):
    name: str
    email: str


class PostCreate(BaseModel):
    title: str
    content: str
    authorId: int


class CommentCreate(BaseModel):
    text: str
    userId: int


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate):
    new_id = len(users_db) + 1
    new_user = User(id=new_id, **user.model_dump())
    users_db.append(new_user)
    return new_user

class LoginData(BaseModel):
    email: str
    password: str
@app.post("/login")
def login(data: LoginData):
    # Шукаємо користувача за email
    for user in users_db:
        if user.email == data.email:
            # Імітуємо видачу токена (просто повертаємо його ID та фейковий токен)
            return {"access_token": f"fake-token-for-user-{user.id}", "user_id": user.id}
    raise HTTPException(status_code=401, detail="Неправильний email або пароль")


@app.get("/users", response_model=List[User])
def get_users():
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserCreate):
    for user in users_db:
        if user.id == user_id:
            user.name = user_data.name
            user.email = user_data.email
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u.id != user_id]
    return


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate):
    new_id = len(posts_db) + 1
    new_post = Post(id=new_id, **post.model_dump())
    posts_db.append(new_post)
    return new_post


@app.get("/posts", response_model=List[Post])
def get_posts(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        authorId: Optional[int] = None,
        sortBy: str = "createdAt"
):
    result = posts_db.copy()

    if authorId is not None:
        result = [p for p in result if p.authorId == authorId]

    if sortBy == "createdAt":
        result.sort(key=lambda x: x.createdAt, reverse=True)
    elif sortBy == "title":
        result.sort(key=lambda x: x.title)

    start = (page - 1) * limit
    end = start + limit
    return result[start:end]


@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post_data: PostCreate):
    for post in posts_db:
        if post.id == post_id:
            post.title = post_data.title
            post.content = post_data.content
            post.authorId = post_data.authorId
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    global posts_db
    posts_db = [p for p in posts_db if p.id != post_id]
    return


@app.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED, response_model=Comment)
def create_comment(post_id: int, comment: CommentCreate):
    if not any(p.id == post_id for p in posts_db):
        raise HTTPException(status_code=404, detail="Post not found")

    new_id = len(comments_db) + 1
    new_comment = Comment(id=new_id, postId=post_id, **comment.model_dump())
    comments_db.append(new_comment)
    return new_comment


@app.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments_for_post(post_id: int):
    return [c for c in comments_db if c.postId == post_id]


@app.put("/comments/{comment_id}", response_model=Comment)
def update_comment(comment_id: int, comment_data: CommentCreate):
    for comment in comments_db:
        if comment.id == comment_id:
            comment.text = comment_data.text
            return comment
    raise HTTPException(status_code=404, detail="Comment not found")


@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int):
    global comments_db
    comments_db = [c for c in comments_db if c.id != comment_id]
    return