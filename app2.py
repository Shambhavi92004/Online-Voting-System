
import joblib  
import numpy as np;
import pandas as pd;
import pymysql 
pymysql.install_as_MySQLdb()
import MySQLdb
import matplotlib.pyplot  as plt;
from sklearn.model_selection  import train_test_split
from sklearn.linear_model  import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix
import pickle
gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]
import numpy as np;
import pandas as pd;
import matplotlib.pyplot  as plt;
from sklearn.model_selection  import train_test_split
from sklearn.linear_model  import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix
import pickle
from flask import Flask, request, render_template, redirect, url_for
import joblib
 

voted_details=[]
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import binascii
import random
from email_sender import otp_sender
from block1 import protect_data

# Function to load keys from files
def load_keys():
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

    return private_key, public_key


#from recamandation_code import recondation_fn
#from recamandation_code_fh import recondation_fn_fh

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index3.html')  



@app.route('/nextpage')
def nextpage():

    return render_template('login121.html')

@app.route('/nextpage2')
def nextpage2():

    return render_template('login141.html')

#@app.route('/send_text', methods=['POST'])
#def send_text():
    # Send either "yes" or "no" to the client
#   text_to_send = "king"
#    if text_to_send:
#        return text_to_send
#    else:
#        return 'Invalid input'

@app.route('/receive_result', methods=['POST'])
def receive_result():
    result = request.form.get('result')  # Receive result from client
    # Process result as needed
    print("Received result from client:", result)
    return 'Result received'


@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]
   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
              #print(result1)
              #print(gmail1)
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        # Read the CSV file
            # Read the CSV file
            df32 = pd.read_csv('voting_data.csv')

            # Count the occurrences of each class in the "voted" column
            vote_counts = df32['voted'].value_counts()

            # Determine the party with the most votes
            winner = vote_counts.idxmax()

            # Create a bar graph
            plt.figure(figsize=(8, 6))
            vote_counts.plot(kind='bar')
            plt.title('Vote Counts')
            plt.xlabel('Party')
            plt.ylabel('Count')
            plt.xticks(rotation=45)

            # Save the graph as an HTML file
            plt.savefig('static/vote_count.png')

            # Render an HTML template to display the graph and announce the winner
            return render_template('vote_count1.html', winner=winner)    
        #return render_template('vote_count.html')
    else:
        return jsonify({'result':'use proper  gmail and password'})
                  
                                               



                          
                     # print(value1[0:])
    
    
    
    

              
              # int_features3[0]==12345 and int_features3[1]==12345:
               #                      return render_template('index.html')
        
@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list1)
    if logu1 in gmail_list1:
                      return jsonify({'result':'this gmail is already in use '})  
    else:

                  #return jsonify({'result':'this  gmail is not registered'})
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login.html')

                      


    
   






@app.route('/crop')
def crop():
     return render_template('crop.html')



@app.route('/crop/predict1',methods=['POST'])
def predict1():
    '''
    For rendering results on HTML GUI
    '''
    int_features1 = [str(x) for x in request.form.values()]

    print(int_features1)
    #int_features2=['1','2','3','4','5','6']

    a1=int_features1
    # Find the index of 'Jet Airways Business' in the list
    


   # int_features11 = int_features1.reshape(1, -1)
   # output1 = model1.predict([int_features1])

    output1 = a1
   # resultcrop = {value:key for key, value in croplist.items()}
    print("the adhar number is ",output1[0])
    # Load the DataFrame from the CSV file
    aadhar_df = pd.read_csv('adhar_database.csv')

    # Get the user input Aadhar number
    user_aadhar =int(output1[0])

    # Check if the entered Aadhar number is in the DataFrame
    if user_aadhar in aadhar_df['Adhar_numbers'].values:

        # Load the CSV file into a DataFrame
        df1= pd.read_csv('voting_data.csv')

        # Update the DataFrame with a new Aadhar card number
        new_adhar_number =user_aadhar
        # Check if the new Aadhar number already exists in the DataFrame
        if new_adhar_number in df1['adhar_number'].values:
            print(f"{new_adhar_number} has already voted.")
            return render_template('login121.html',alert_text="YOU ALREADY VOTED")
        else:
            # Append the new Aadhar card number to the DataFrame



            #otp1="1234"
            # Generate a random 4-digit number
            random_number = random.randint(1000, 9999)

            # Write the number to a temporary file
            with open('temp_file.txt', 'w') as file:
                file.write(str(random_number))
            otp_sender(random_number)


            voted_details.append(new_adhar_number)
            voted_details.append(random_number)
            #df = df.append({'adhar_number': new_adhar_number, 'otp': otp1, 'voted': False}, ignore_index=True)
            
            # Save the updated DataFrame back to the CSV file
            #df.to_csv('voting_data.csv', index=False)




            #print("OK")
            return render_template('otp_verification1.html')
    else:
        print("NO")

        return render_template('login121.html',alert_text="Use Authonticated Adhar Number")


 
    

    

   # return render_template('otp_verification.html')

@app.route('/crop1/predict5',methods=['POST'])
def predict5():
    '''
    For rendering results on HTML GUI
    '''
    int_features1 = [str(x) for x in request.form.values()]

    print("print  OTP ",int_features1)
    print("voter details",voted_details)
    #int_features2=['1','2','3','4','5','6']

    # Read the number from the temporary file
    with open('temp_file.txt', 'r') as file:
        read_number = file.read()
        print("Read number:", read_number)


    if  int(read_number)==int(int_features1[0]):




                  a1=int_features1
                  # Find the index of 'Jet Airways Business' in the list
                  


                 # int_features11 = int_features1.reshape(1, -1)
                 # output1 = model1.predict([int_features1])

                  output1 = a1
                 # resultcrop = {value:key for key, value in croplist.items()}
                  print("the OTP is ",output1[0])
                  import os
                  os.remove('temp_file.txt')
                  print("Temporary file deleted.")
                  #print(int_features12)

                  return render_template('voting_page1.html')
    else:



      return render_template('otp_verification1.html',alert_text1="Use Proper OTP")





@app.route('/crop2')
def crop2():
    return render_template('crop2.html')



@app.route('/crop2/predict2',methods=['POST'])
def predict2():
    '''
    For rendering results on HTML GUI
    '''
    int_features12 = [str(x) for x in request.form.values()]


    output11 = recondation_fn_fh(int_features12)
   # resultcrop = {value:key for key, value in croplist.items()}
    print(output11)


 
    

    

    return render_template('crop2.html', prediction1_text='Health condition Level is    {}'.format(output11[0]))


@app.route('/crop2/predict2/vote1',methods=['POST'])
def vote1():
    '''
    For rendering results on HTML GUI
    '''
    int_features12 = [str(x) for x in request.form.values()]


    #output11 = recondation_fn_fh(int_features12)
   # resultcrop = {value:key for key, value in croplist.items()}

# Delete the temporary file


    output11=int_features12[0]


    voted_details.append(str(int_features12[0]))

    df1= pd.read_csv('voting_data.csv')


    print("voted details are  ",voted_details)

    import hashlib

    # Password to be hashed
    voted_party = str(voted_details[2])
    print(voted_party)
    # Create a new SHA-512 hash object
    sha512_hash = hashlib.sha512()

    # Update the hash object with the password bytes
    sha512_hash.update(voted_party[0].encode('utf-8'))

    # Get the hexadecimal representation of the hashed password
    hashed_password = sha512_hash.hexdigest()

    # Print the hashed password
    print("SHA-512 Hashed Password:", hashed_password)
    print(voted_details[0:3])


    print(hashed_password)

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization, hashes
    import binascii

    # Load keys from files
    loaded_private_key, loaded_public_key = load_keys()
    #message =hashed_password
    message =hashed_password.encode()  # Convert string to bytes

    # Encrypt using loaded public key
    ciphertext = loaded_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt using loaded private key
    plaintext = loaded_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("Original message:", message.decode())


    result=protect_data(ciphertext)
    #print("Decrypted message:", plaintext.decode())

    print("encrpted and hashed output after all blocks",result)


    
    df1 = df1.append({'adhar_number': voted_details[0], 'otp':voted_details[1], 'voted': voted_details[2],"hashed_encrypted_all_blocks":result}, ignore_index=True)
            
            # Save the updated DataFrame back to the CSV file
    df1.to_csv('voting_data.csv', index=False)


    voted_details.clear()




 
    

    

    return render_template('index3.html')

@app.route('/send_text', methods=['POST'])
def send_text():
    vote="party1"
    int_features12 = vote


    #output11 = recondation_fn_fh(int_features12)
   # resultcrop = {value:key for key, value in croplist.items()}

# Delete the temporary file


    output11=vote


    #voted_details.append(str(int_features12[0]))

    #df1= pd.read_csv('voting_data.csv')


    #print("voted details are  ",voted_details)

    import hashlib

    # Password to be hashed
    voted_party = str(vote)
    print(voted_party)
    # Create a new SHA-512 hash object
    sha512_hash = hashlib.sha512()

    # Update the hash object with the password bytes
    sha512_hash.update(voted_party[0].encode('utf-8'))

    # Get the hexadecimal representation of the hashed password
    hashed_password = sha512_hash.hexdigest()

    # Print the hashed password
    print("SHA-512 Hashed Password:", hashed_password)
    #print(voted_details[0:3])


    #print(hashed_password)

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import serialization, hashes
    import binascii

    # Load keys from files
    loaded_private_key, loaded_public_key = load_keys()
    #message =hashed_password
    message =hashed_password.encode()  # Convert string to bytes

    # Encrypt using loaded public key
    ciphertext = loaded_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt using loaded private key
    plaintext = loaded_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("Original message:", message.decode())


    result=protect_data(ciphertext)
    #print("Decrypted message:", plaintext.decode())

    print("encrpted and hashed output after all blocks",result)


    
    #df1 = df1.append({'adhar_number': voted_details[0], 'otp':voted_details[1], 'voted': voted_details[2],"hashed_encrypted_all_blocks":result}, ignore_index=True)
            
            # Save the updated DataFrame back to the CSV file
    #df1.to_csv('voting_data4.csv', index=False)


    #voted_details.clear()




 
    

    # Send either "yes" or "no" to the client
    text_to_send = result
    if text_to_send:
        return text_to_send
    else:
        return 'Invalid input'

#if __name__ == "__main__":
#    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
