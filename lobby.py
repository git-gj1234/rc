from identification import go_online, go_offline, set_username
from find_users import find_online_users
from game import game_server, game_client


def main():

    # sample menu program
  while True:

    # print online users
    
    users=find_online_users()
    username = input('Enter your username: ')
    while True:
      for i in users:
        if i['username']==username:
          print('Username already exists')
          username = input('Enter your a different username: ')
        else:
          break
      break
    set_username(username)
      

    # get input
    user_input = input('--MENU--\n(1) Go Online (wait for incoming connections)\n(2) Play against an Online Player\n(3) Refresh\n-->')
    while user_input != '1' and user_input != '2' and user_input != '3':
      print('Invalid input. Please try again.')

    if user_input == '1':
      go_online()
      game_server()
      go_offline()
    
    elif user_input == '2':
      print('LOGIC FOR PRINTING ONLINE USERS LIST')
      print('online users:')
      # print('SOME LOGIC FOR PRINTING ONLINE USERNAMES')
      if len(users) == 0:
        print('No users online')
      else:
        for i in users:
          print(i['username'])
      print('LOGIC FOR ASKING USERNAME WHO THEY WANT TO PLAY AGAINST')
      user_chosen = input('Enter the username of the player you want to play against: ')
      print('LOGIC FOR VERIFYING THE INPUT OF THE USER')
      while True:
        for i in users:
          if i['username']==user_chosen:
            break
          else:
            print('Username not found')
            user_chosen = input('Enter a different username: ')
        break
      print('LOGIC FOR GETTING THE IP ADDRESS OF THE USERNAME FROM ONLINE USERS LIST')
      for i in users:
        if i['username']==user_chosen:
          chosen_opponent = i['ip_address']
      game_client(chosen_opponent)

    elif user_input == '3':
        # next iteration will print the new online users
      continue
  
if __name__ == '__main__':
  main()