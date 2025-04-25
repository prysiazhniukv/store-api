from fastapi import APIRouter, HTTPException
from src.models.models import (
    UserPost,
    UserPostIn,
    CommentIn,
    Comment,
    UserPostWithComments,
)


router = APIRouter()
post_table = {}
comment_table = {}


@router.get("/{post_id}", response_model=UserPost)
async def find_post(post_id: int):
    post = post_table.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_table[post_id]


@router.post("/", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments(post_id: int):
    post = await find_post(post_id)
    comments = [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]
    return comments


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    return {"post": post, "commnets": await get_comments(post_id)}
