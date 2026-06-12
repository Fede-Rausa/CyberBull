

def showtable(tablename, myclient):
    response = myclient.table(tablename).select("*").execute()
    return response

def count_rows(table_name, myclient):
    res = myclient.rpc('get_row_count', {'table_name': table_name}).execute()
    return res


def try_to_add_user(username, password, myclient):
    '''returns False if the username is already used'''
    data = {'candidate_username':username, 'candidate_password':password}
    response = myclient.rpc('register_user', data).execute()
    return response

def try_to_login(username, password, myclient):
    data = {'candidate_username':username, 'candidate_password':password}
    response = myclient.rpc('login_user', data).execute()
    return response

def get_chat(userA,userB, myclient):
    response = myclient.rpc('get_private_chat', {'user_a':userA, 'user_b':userB}).execute()
    return response

def send_message(sender, receiver, content, myclient):
    data = {'sender_name':sender, 'receiver_name':receiver, 'message_content':content}
    response = myclient.rpc('send_message', data).execute()
    return response

def send_post(sender, content, myclient):
    data = {'sender_name':sender, 'content':content}
    response = myclient.rpc('make_post', data).execute()
    return response

def get_user_posts(username, myclient):
    response = myclient.rpc('get_user_posts', {'username': username}).execute()
    return response

def get_all_posts(myclient):
    response = myclient.table('posts').select("*").execute()
    return response

def get_user_preferences(username, myclient):
    response = myclient.rpc('get_user_preferences', {'username': username}).execute()
    return response

def set_user_preferences(username, food, animal, myclient):
    data = {'username': username, 'food_favor': food, 'animal_favor': animal}
    response = myclient.rpc('set_user_preferences', data).execute()
    return response

def follow(sender, receiver, myclient):
    data = {'sender': sender, 'receiver':receiver}
    response = myclient.rpc('make_friendship', data).execute()
    return response

def unfollow(sender, receiver, myclient):
    data = {'sender': sender, 'receiver':receiver}
    response = myclient.rpc('break_friendship', data).execute()
    return response    


def get_user_profile(username, myclient):
    response = myclient.rpc('get_user_profile', {'username': username}).execute()
    return response

def set_user_profile(username, description, myclient):
    myclient.rpc('set_user_profile', {'username': username, 'content': description}).execute()


def get_all_users(myclient):
    response = myclient.rpc('get_all_users').execute()
    return response

def get_all_users_info(myclient):
    response = myclient.rpc('get_users_des').execute()
    return response

def get_friends_of(username, myclient):
    response = myclient.rpc('get_friends_of', {'userlogged': username}).execute()
    return response

def get_following(username, myclient):
    response = myclient.rpc('get_following', {'userlogged': username}).execute()
    return response

def get_follower(username, myclient):
    response = myclient.rpc('get_follower', {'userlogged': username}).execute()
    return response

def delete_user(username, myclient):
    response = myclient.rpc('delete_user_data', {'target_username': username}).execute()
    return response

# def add_user(username, password):
#     data = {'userid':username, 'pswd':password}
#     response = myclient.table("accounts").insert(data).execute()
#     return response
