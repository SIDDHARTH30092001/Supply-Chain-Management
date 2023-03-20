#Libs
import hashlib as hasher
import datetime as date

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import pkcs1_15

import random
import time

import tkinter as tk

#Globals
supply_blockchain=[]
utxo_array=[]
manufacturers_list=[]
other_users_list=[]
global_index=0
pow_proof=int(0)


class Supply_Block:
    #The initialisation function allows the setting up of a block
    def __init__(self, index, timestamp, supply_data, previous_hash):
        self.index=index
        self.timestamp=timestamp
        self.supply_data=supply_data
        self.previous_hash=previous_hash
        self.proof_of_work=int(generate_pow())
        self.hash=self.hash_block()

    def hash_block(self):
        sha=hasher.sha256()
        sha.update((str(self.index)+
                    str(self.timestamp)+
                    str(self.supply_data)+
                    str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

#Algorithm generating PoW (based on BitCoin PoW)
#The algorithm requires to find SHA256 of a natural number (string) such that has the first three positions as '000' and ends with '00'
def generate_pow():
    start_time=time.time()
    global pow_proof
    initial_start=pow_proof+1

    while(1):
        sha=hasher.sha256()
        sha.update(str(initial_start).encode('utf-8'))
        hash_value=sha.hexdigest()
        initial_start=int(initial_start)+1

        if(hash_value[0]=='0' and hash_value[1]=='0' and hash_value[2]=='0' and hash_value[-1]=='0' and hash_value[-2]=='0'):
            end_time=time.time()
            pow_proof=initial_start-1
            
            gblock1.config(text=hash_value)
            gblock2.config(text=str(pow_proof))
            gblock3.config(text=str((end_time-start_time)))

            #print('\n The required Hash Value : '+hash_value)
            #print('The PoW Number : '+str(pow_proof))
            #print('The Total Time : '+str((end_time-start_time)))

            break
    return pow_proof

class Transaction:
    #The initialisation function for a single transaction
    def __init__(self, supplier_puk, receiver_puk, item_id, timestamp, signature):
        self.supplier_puk=supplier_puk
        self.receiver_puk=receiver_puk
        self.item_id=item_id
        self.timestamp=timestamp
        self.signature=signature

#This funcion is used to cr8 genesis block
def create_genesis_block():
    global global_index
    global_index=global_index+1
    genesisblock.config(text='The genesis block is being created.')
    #print('\n The genesis block is being created \n')

    return Supply_Block(0,date.datetime.now(),"GENESIS BLOCK","0")

#This function is used for viewing all the blocks and the transactions in the blockchain
def view_blockchain():
    operation_name.grid(row=5,column=0)
    operation_op.grid(row=7,column=0)
    operation_name.config(text='The list of blocks are: \n')
    #print('\n The list of blocks are: \n')

    for block in supply_blockchain:
        operation_op.config(text='\n- - - - - - - - - - - - - - - - - - - -\n'+str(block.index)+'\n'+str(block.timestamp)+'\n'+str(block.supply_data)+'\n'+str(block.proof_of_work)+'\n'+str(block.hash)+'\n'+str(block.previous_hash)+'\n- - - - - - - - - - - - - - - - - - - -\n')
        #print('\n---------------------------------------------------------------')
        #print(block.index)
        #print(block.timestamp)
        #print(block.supply_data)
        #print(block.proof_of_work)
        #print(block.hash)
        #print(block.previous_hash)
    #print('---------------------------------------------------------------------')
    #print('\n')

#This fumction is used to view all the unspend transaction outputs
def view_UTXO():
    print('\n The list of UTXO are: \n')
    for transaction in utxo_array:
        print('\n---------------------------------------------------------------')
        print(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))
        print(transaction.receiver_puk)
        print(transaction.item_id)
        print(transaction.timestamp)
        print(transaction.signature)
    print('---------------------------------------------------------------------')
    print('\n')

#This function is used to generate a transaction
def make_transaction():
    #Selection function for the keys and the item ID
    #selection=input('\n Select type of key (M/O) for supplier: ')
    
    operation_name.config(text=' Select type of key (M/O) for supplier: MAKE_TRANSACTION \n')
    btn1=tk.Button(root, text="M",command=pass1)
    #btn2=tk.Button(root, text="S",command=pass2)
    btn1.grid(row=5,column=3)
    btn2.grid(row=5,column=4)

def pass1():
    operation_name.config(text='There are a total of ' + str(len(manufacturers_list))+' users. Enter your selection PASS1: ')

    operation_ip_btn=tk.Button(root, text="->",command=pass11)
    operation_ip.grid(row=6,column=1)
    operation_ip_btn.grid(row=6,column=2)
    
def pass11():
    index=int(operation_ip.get())-1
    #index=int(input('There are a total of ' + str(len(manufacturers_list))+' users. Enter your selection: '))-1
    
    #operation_ip_btn=tk.Button(root, text="->",command=pass11)
    #operation_ip.grid(row=6,column=1)
    #operation_ip_btn.grid(row=6,column=2)
    
    supplier_key=manufacturers_list[index]

    operation_name.config(text=' Select type of key (M/O) for supplier PASS11: \n')
    btn3=tk.Button(root, text="M",command=pass3(supplier_key))
    btn4=tk.Button(root, text="S",command=pass4(supplier_key))
    btn3.grid(row=5,column=5)
    btn4.grid(row=5,column=6)

def pass3(supplier_key):
    supplier_key=supplier_key
    #operation_name.config(text=' Select type of key (M/O) for supplier: \n')

    operation_name.config(text='There are a total of ' + str(len(manufacturers_list))+' users. Enter your selection: PASS3')

    op3=tk.Button(root, text="->",command=pass31(supplier_key))
    op3.grid(row=7,column=1)
    op3.grid(row=7,column=2)

def pass31(supplier_key):
    supplier_key=supplier_key
    index=int(operation_ip.get())-1
    #index=int(input('There are a total of ' + str(len(manufacturers_list))+' users. Enter your selection: '))-1
    
    operation_ip_btn=tk.Button(root, text="->",command=done(supplier_key,receiver_key))
    operation_ip.grid(row=6,column=1)
    operation_ip_btn.grid(row=6,column=2)
    
    receiver_key=other_users_list[index]
    done(supplier_key,receiver_key)
    

    
 


def pass41(supplier_key):
    operation_name.config(text='There are a total of '+str(len(other_users_list))+' users. Enter your selection: ')
    #index=int(operation_ip.get())-1
    #operation_ip_btn.Button(root, text= "->")
    #operation_ip_btn.wait_variable(1)
        #index=int(input('There are a total of '+str(len(other_users_list))+' users. Enter your selection: '))-1
    #receiver_key=other_users_list[index]
    #done(supplier_key,receiver_key)
    
def pass4(supplier_key):
    supplier_key=supplier_key
    operation_name.config(text=' Select type of key (M/O) for supplier: \n')

    btn3=tk.Button(root, text="M",command=pass41(supplier_key))
    btn4=tk.Button(root, text="S",command=pass31(supplier_key))
    btn3.grid(row=5,column=5)
    btn4.grid(row=5,column=6)
   

    

def done(supplier_key,receiver_key):
    supplier_key=supplier_key
    receiver_key=receiver_key

    operation_ip_btn=tk.Button(root, text="->",command=idpass(supplier_key,receiver_key))
    operation_ip.grid(row=6,column=1)
    operation_ip_btn.grid(row=6,column=2)
    
   
    operation_name.config(text='Enter the ID of the tracked item: ')
    

def idpass(supplier_key,receiver_key):
    supplier_key=supplier_key
    receiver_key=receiver_key
    
    receiver_puk=receiver_key.publickey().exportKey("PEM").decode('utf-8')

    item_id=int(operation_ip.get())
    #item_id=input('Enter the ID of the tracked item: ')

    #Acquiring the details of the transactions
    supplier_puk=supplier_key.publickey()
    timestamp=date.datetime.now()

    #Generating the message text and the signature
    message=str(supplier_puk.exportKey("PEM").decode('utf-8'))+str(receiver_puk)+str(item_id)+str(timestamp)
    hash_message=SHA256.new(message.encode('utf-8'))

    supplier_prk=RSA.import_key(supplier_key.exportKey("DER"))
    signature=pkcs1_15.new(supplier_prk).sign(hash_message)

    #Creating a new transaction
    new_transaction=Transaction(supplier_puk, receiver_puk, item_id, timestamp, signature)
    utxo_array.append(new_transaction)

    print("done")

    

#The function for mining the block in the supply blockchain
def mine_block():
    global global_index
    max_range=len(utxo_array)
    transaction_amount=random.randint(0,max_range)
    transaction_array=[]

    print('\n The number of selected transactions for the block is: '+str(transaction_amount))

    if(transaction_amount):
        for index in range(0,transaction_amount):
            #All verifications for the transactions
            if(verify_trasaction(utxo_array[0])):
                print('\n The sign verification for transaction #'+str(index+1)+' was true!')
                if(check_item_code(utxo_array[0])):
                    print('The item code has been found. Checking the previous owner details')
                    if(check_previous_owner(utxo_array[0])):
                        print('Verification of previous owner has been done!')
                        transaction_array.append(utxo_array[0])
                    else:
                        print('Verification of prvious owner has failed!')
                else:
                    print('The item code was not found on blockchain. Checking for manufacturer credentials.')
                    if(check_manufacturer_credentials(utxo_array[0])):
                        print('The new item has been added under the manufacturer.')
                        transaction_array.append(utxo_array[0])
                    else:
                        print('The transaction key is not authorised as a manufacturer!')
            else:
                print('The sign verification for transaction #'+str(index+1)+' was false!')
            utxo.array.pop(0)
        if(len(transaction_array!=0)):
            new_block=Supply_Block(global_index,date.datetime.now(),transaction_array,supply_blockchain[global_index-1].hash)
            global_index=global_index+1
            supply_blockchain.append(new_block)
    else:
        #Prevent addition of blocks with no transactions
        print('No transactions have been selected and therefore no block has been added!')

#This function is used for the verifying the signature of the transaction
def verify_transaction(self):
    supplier_puk=RSA.import_key(self.supplier_puk.exportKey("DER"))
    message=str(self.supplier_puk.exportKey("PEM").decode('utf-8'))+str(self.receiver_puk)+self.item_id+str(self.timestamp)
    hash_message=SHA256.new(message.encode('utf-8'))

    try:
        pkcs1_15.new(supplier_puk).verify(hash_message.self.signature)
        return True
    except(ValueError,TypeError):
        return False

#Smart contract for checking if the input item code is available on the blockchain and checking the previous owner of the consignment
def check_item_code(self):
    found_flag=False
    temp_blockchain=supply_blockchain[::-1]

    for block in temp_blockchain[:-1:]:
        for transaction in block.supply_data:
            if(transaction.item_id==self.item_id):
                found_flag=True
    return found_flag

#Smart contract for checking the previous owner of the commodity
def check_previous_owner(self):
    found_flag=False
    temp_blockchain=supply_blockchain[::-1]

    for block in temp_blockchain[:-1:]:
        for transaction in block.supply_data:
            if(transaction.item_id==self.item_data):
                if(transaction.receiver_puk==self.supplier_puk.exportKey("PEM").decode('utf-8')):
                    return True
                else:
                    return False

#Smart contract for checking if the user is an authorised manufacturer
def check_manufacturer_credentials(self):
    for item in manufacturers_list:
        if str(self.supplier_puk.exportKey("PEM").decode('utf-8'))==str(item.publickey().exportKey("PEM").decode('utf-8')):
            return True
    return False

#The function would verify all the blocks in the given blockchain
def verify_blockchain():
    previous_block=supply_blockchain[0]
    count=1

    for block in supply_blockchain[1:]:
        print('\n For the block #'+str(count)+': ')
        for transaction in block.supply_data:
            print('The item ID is '+str(transaction.item_id)+' and the associated timestamp is '+str(transaction.timestamp))

        if(str(previous_block.hash)==str(block.previous_hash)):
            print('The hash values have been verified.')

        sha=hasher.sha256()
        sha.update(str(int(block.proof_of_work)).encode('utf-8'))
        hash_value=sha.hexdigest()
        print('The PoW number is '+str(block.proof_of_work)+' and the aassociated hash is '+hash_value)
    print('--------------------------------------------------------------------------------------')
    print('\n')

#Function for generating manufaturer keys
def generate_manufacturer_keys():
    for item in range(0,int(manufacturers.get())):
        manufacturers_list.append(RSA.generate(1024,Random.new().read))
    #print(manufacturer_list)
    result_label.config(text='The manufacturer keys have been generated.')
    add_button2.config(state='normal')
    #print('\n The manufacturer keys have been generated')

#Function for generating stakeholder keys
def generate_other_keys():
    for item in range(0,int(stakeholders.get())):
        other_users_list.append(RSA.generate(1024,Random.new().read))
    #print(other_users_list)

    result_label2.config(text='The stakeholder keys have been generated.')

    num1_label.after(5000,num1_label.grid_remove())
    manufacturers.grid_remove()
    num2_label.grid_remove()
    stakeholders.grid_remove()
    add_button.grid_remove()
    result_label.grid_remove()
    add_button2.grid_remove()
    result_label2.grid_remove()

    supply_blockchain.append(create_genesis_block())

    lab1.grid(row=0,column=0, sticky="w")
    genesisblock.grid(row=0, column=1)
    lab2.grid(row=1,column=0, sticky="w")
    gblock1.grid(row=1, column=1)
    lab3.grid(row=2,column=0, sticky="w")
    gblock2.grid(row=2, column=1)
    lab4.grid(row=3,column=0, sticky="w")
    gblock3.grid(row=3, column=1)

	
    #print('\nThe stakeholder keys have been generated.')

    operations.grid(row=4,column=0)
    operation.grid(row=4,column=1)
    operation_button.grid(row=4,column=2)
    
    

#Function for tracking an item
def track_item(item_code):
    not_fount_flag=True

    for block in supply_blockchain[1:]:
        for transaction in block.supply_data:
            if(item_code==transaction.item_id):
                if(not_found_flag):
                    print('\n The item (' + item_code + ') has been found and tracking details are: ')
                    not_found_flag=False
                    
                manufacturer_supplier=False
                manufacturer_receiver=False

                supplier_count=0
                supplier_not_found_flag=True

                for item in manufacturers_list:
                    supplier_count=supplier_count+1

                    if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))==str(item.publickey().exportKey("PEM").decode('utf-8')):
                        supplier_not_found_flag=False
                        manufacturer_supplier=True
                        break

                if(supplier_not_found_flag):
                    supplier_count=0

                    for item in other_users_list:
                        supplier_count=supplier_count+1

                        if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))==str(item.publickey().exportKey("PEM").decode('utf-8')):
                            supplier_not_found_flag=False
                            break

                receiver_count=0
                receiver_not_found_flag=True

                for item in manufacturers_list:
                    receiver_count=receiver_count+1

                    if str(transaction.receiver_puk)==str(item.publicKey().exportKey("PEM").decode('utf-8')):
                        receiver_not_found_flag=False
                        manufacturer_receiver=True
                        break

                if(receiver_not_found_flag):
                    receiver_count=0

                    for item in other_users_list:
                        receiver_count=receiver_count+1

                        if str(transaction.receiver_puk)==str(item.publickey().exportKey("PEM").decode('utf-8')):
                            receiver_not_found_flag=True
                            break

                final_result=""

                if(manufacturer_supplier):
                    final_result=final_result+"Manufacturer #"+str(supplier_count)+" transferred the asset to "
                else:
                    final_result=final_result+"Stakeholder #"+str(supplier_count)+" transferred the asset to "

                if(manufacturer_receiver):
                    final_result=final_result+"Manufacturer #"+str(receiver_count)+" at "+str(transaction.timestamp)
                else:
                    final_result=final_result+"Stakeholder #"+str(receiver_count)+" at "+str(transaction.timestamp)

                print(final_result)

            def hide_me(event):
                event.widget.pack_forget()

                #if(not_found_flag):
	#	print('\nThe item code was not found in the blockchain.')

# Generating keys for manufactures and other users
#number_manufacturers = int(input('\nEnter the number of manufacturers: '))
#generate_manufacturer_keys(number_manufacturers)
	
#number_other_users = int(input('\nEnter the number of stakeholders: '))
#generate_other_keys(number_other_users)

# Inserting a genesis block into blockchain
#supply_blockchain.append(create_genesis_block())
#print('\n\nWelcome to the supply blockchain.')

# Menu driven program for the supply blockchain
#while(1):
#	print('\nThe following options are available to the user: ')
#	print('1. View the blockchain. ')
#	print('2. Enter a transaction. ')
#	print('3. View the UTXO array. ')
#	print('4. Mine a block. ')
#	print('5. Verify the blockchain. ')
#	print('6. Generate RSA keys. ')
#	print('7. Track an item.')
#	print('8. Exit.')
	
#	choice = int(input('Enter your choice: '))
	
#	if(choice == 1):
#		view_blockchain()
#	elif(choice == 2):
#		make_transaction('','','')
#	elif(choice == 3):
#		view_UTXO()
#	elif(choice == 4):
#		mine_block()
#	elif(choice == 5):
#		verify_blockchain()
#	elif(choice == 6):
#		number_manufacturers = int(input('\nEnter the number of manufacturers: '))
#		generate_manufacturer_keys(number_manufacturers)
#		number_other_users = int(input('Enter the number of stakeholders: '))
#		generate_other_keys(number_other_users)
#	elif(choice == 7):
#		item_code = input('Enter the item code: ')
#		track_item(item_code)
#	elif(choice == 8):
#		break
#	else:
#		print('This is an invalid option.')

def ops():
    if(operation.get()=='1'):
        view_blockchain()
    elif(operation.get() == '2'):
        make_transaction()
    elif(operation.get() == 3):
        view_UTXO()
    elif(operation.get() == 4):
        mine_block()
    elif(operation.get() == 5):
        verify_blockchain()

# create the main window
root = tk.Tk()
root.title("Supply Chain Management")



# create the widgets
num1_label = tk.Label(root, text="Enter Number of Manufacturers")
manufacturers = tk.Entry(root)

num2_label = tk.Label(root, text="Enter Number of Stakeholders")
stakeholders = tk.Entry(root)

add_button = tk.Button(root, text="Manufacturers", command=generate_manufacturer_keys)
result_label = tk.Label(root, text="Result:")

add_button2 = tk.Button(root, text="Stakeholders", command=generate_other_keys)
result_label2 = tk.Label(root, text="Result:")

if(manufacturers.get()==""):
        add_button2.config(state='disabled')

lab1=tk.Label(root, text="Genesis Block Status : ")
genesisblock = tk.Label(root)
lab2=tk.Label(root, text="Hash Value : ")
gblock1 = tk.Label(root)
lab3=tk.Label(root, text="PoW Number : ")
gblock2 = tk.Label(root)
lab4=tk.Label(root, text="Total Time Taken : ")
gblock3 = tk.Label(root)

operations=tk.Label(root, text="The following options are available to the user: \n 1. View the blockchain. \n 2. Enter a transaction. \n 3. View the UTXO array. \n 4. Mine a block. \n 5. Verify the blockchain. \n 6. Generate RSA keys. \n 7. Track an item. \n 8. Exit.")
operation = tk.Entry(root)
operation_button=tk.Button(root, text="->", command=ops)

operation_name=tk.Label(root)
operation_op = tk.Label(root)
operation_ip=tk.Entry(root)

num1_label.grid(row=0, column=0, sticky="e")
manufacturers.grid(row=0, column=1)
num2_label.grid(row=1, column=0, sticky="e")
stakeholders.grid(row=1, column=1)
add_button.grid(row=2, column=0)
result_label.grid(row=2, column=1)
add_button2.grid(row=3, column=0)
result_label2.grid(row=3, column=1)
 

root.mainloop()
