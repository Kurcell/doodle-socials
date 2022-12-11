from src.models.models import Post

def test_post_create(client):
    """
    GIVEN a post data model
    WHEN a post's create function is called
    THEN check that the function leads to the creation of a post if the request is proper
    """
    post = Post.create(2,3)

    assert post.user_id == 2 and post.doodle_id == 3


def test_post_update(client):
    """
    GIVEN a post data model
    WHEN a post's update function is called
    THEN check that the function leads to the modification of a post if the request is proper
    """
    post = Post.update(1, 1, 4)

    assert post.pid == 1 and post.user_id == 1 and post.doodle_id == 4
    

def test_post_delete(client):
    """
    GIVEN a post data model
    WHEN a post's delete function is called
    THEN check that the function leads to the deletion of a post if the request is proper
    """

    post = Post.delete(1)

    assert post.pid == 1
