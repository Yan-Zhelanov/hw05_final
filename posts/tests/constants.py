from django.urls import reverse

USERNAME = 'TestUser-1'
USERNAME2 = 'TestUser-2'

GROUP_NAME = 'Test Group-1'
GROUP_SLUG = 'test-group-1'
GROUP_DESCRIPTION = 'Test description for group 1.'

GROUP2_NAME = 'Test Group-2'
GROUP2_SLUG = 'test-group-2'
GROUP2_DESCRIPTION = 'Test description for group 2.'

POST_TEXT = 'No changed test text'

INDEX_URL = reverse('posts:index')
GROUP_URL = reverse('posts:group', args=[GROUP_SLUG])
PROFILE_URL = reverse('posts:profile', args=[USERNAME])
FOLLOW_URL = reverse('posts:follow_index')
PROFILE_FOLLOW_URL = reverse("posts:profile_follow", args=[USERNAME])
PROFILE_UNFOLLOW_URL = reverse('posts:profile_unfollow', args=[USERNAME])
NEW_POST_URL = reverse('posts:new_post')

IMAGE = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x054'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
