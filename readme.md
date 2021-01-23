# mqttchat
A chat app using mqtt protocol (group or one to one) with paho mqtt python client
including a chatbot(searching on gogle and giving the answer)on the terminal

## how to 
### chat  with another client
  * run the files ``` cli/client.py``` on your terminal the menu will appear.
  * type ```chat``` to go to the chat shell 
  * on the chat shell type  ``` login <your_user_name>```
  * invite the person you want to chat with by typing ``` invite <other_person_user_name>```
  * finally start sending message to the other person


### chat with the chatbot(ask questions to the bot )
 * run the files ``` cli/client.py``` on your terminal the menu will appear.
 * type ```ask``` to go to the chatbot shell
 * finally, start asking questions to the bot



## commands:
### Main Menu
  * ```quit```  quit and exit
  * ```ask```  go to the chatbot shell
  * ```chat```  go to the chat shell
### chat shell
   * ```login <user_name>``` login with your username
   * ```invite <other>``` invite a friend to the chat
   * ```back``` go back to the main menu

  
  
## Todos:
 * Add login and registration functions
 * Add group chat
 * Add files sending
 * Add encryption