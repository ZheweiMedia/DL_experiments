//* * * * * * * * * * * * * * * * * * * * * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * 
//
//   program:     Homework 3 Caesar Cypher
//   Name  :      Weizhen (Wendy) Cai
//   Email :      wc513313@ohio.edu
//   Description: This program encrypts/decrypt a file using Caesar cypher.
//                The program should be able to encrypt and decrypt all characters
//                excluding new line characters. Every line is encryed/decryted with different
//		  key value. The key value increases one each line. The key value is reset to its
//		  original value every five lines. 
//   Date  :      06/02/2017
//
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 


#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <fstream>
#include <string>

using namespace std;

void displayMenu();	// a fuction dispaly menu
void obtain_key_value(int &key_value);	// a fuction obtain key value from user
void two_files(string &in_file, string &out_file, ifstream &in_stream, ofstream &out_stream);	// a function obtain two open stream associated with input/output file
void encryption(int &key_value, ifstream &in_stream, ofstream &out_stream);	// function encryt a message
void decryption(int &key_value, ifstream &in_stream, ofstream &out_stream);	// function decrypte a message


int main()
{
  // declare a variable to ask user to choose a option according to menu displayed
  int choice;

  int key_value = 100; // declare and initialize key_value to judge whether  user has set the key_value  or not

  // declare variables of files objects
  string file1, file2;

  // declare variables of two open streams of input/output files
  ifstream in_stream;
  ofstream out_stream;

  displayMenu();
  cout << "Please enter your choice: ";	//promote user to input choice
  cin >> choice;

  // choice 1 is setting the shift key value
  if (choice == 1)

	obtain_key_value(key_value);

  // choice 2 is encrypting a message
  if (choice == 2){

	// if  user hasn't set the key value, promots the user's input as key value
	if (key_value == 100){	// key_value is 100 means user hasn't set the shift key value yet,then ask user to set it first.
		obtain_key_value(key_value);
		two_files(file1,file2,in_stream, out_stream);
		encryption(key_value, in_stream, out_stream);
		return 0;
	}
	else{
		two_files(file1,file2,in_stream, out_stream);
		encryption(key_value, in_stream, out_stream);
		return 0;
	}
  }
  if (choice == 3){

	// if user hasn't  set key value, then ask the user to input a int as key value
	if (key_value == 100){  // key_value is 100 means user hasn't set the shift key value yet,then ask user to set it first.
        	obtain_key_value(key_value);
        	two_files(file1,file2,in_stream, out_stream);
        	decryption(key_value, in_stream, out_stream);	//decrpts a message 
        	return 0;
        }
        else{
        	two_files(file1,file2,in_stream, out_stream);
        	decryption(key_value, in_stream, out_stream);
        	return 0;
	}
  }

  // choice 4 means quit the program
  if (choice == 4)
	return 0;

return 0;
}


// function that displays a menu
void displayMenu(){
  cout << "1. Set the shift key value" << endl;
  cout << "2. Encrypt a message" << endl;
  cout << "3. Decrypt a message" << endl;
  cout << "4. Quit" << endl;

}


// function obtain key value only between 1- 10, otherwise continue asks for a valid input int
void obtain_key_value(int &key_value)
{
    do {
	cout << "Please input a valid key value (1-10): ";
	cin >> key_value;
     }while(key_value < 1 || key_value > 10);

}


// function obtain two openned streams connected to input/output file, keep asks for a valid file name until the file is successfully opened
void two_files(string &in_file, string &out_file, ifstream &in_stream, ofstream &out_stream)
{

do
{
 cout << "Please input valid input filename: ";
 cin >> in_file;
 in_stream.open(in_file.c_str());
}while (in_stream.fail());


do
{
 cout << "Please input valid output file name: ";
 cin >> out_file;
 out_stream.open(out_file.c_str());
}while(out_stream.fail());


}

// encryt a file
void encryption(int &key_value, ifstream &in_stream, ofstream &out_stream)
{

  int original_key_value = key_value;
  char ch;


  while (!in_stream.eof()){	// when not reach the end of file

	// get message letter by letter
	in_stream.get(ch);

      // if the char read is not a new line char, encrpts it with the right key value(i.e. first line-original key value, second-original key value + 1...)
      if (ch != '\n'){
	ch = int (ch);
	ch += key_value;
	ch = char (ch);
	out_stream << ch;

	}

      // if the read char is a new line('\n'), do not encrypt it, keep it the same in the output file, adding 1 to the original key value
      else
      {
	 out_stream  << '\n';

	// key value loop every 5 lines;
        if((key_value - original_key_value)== 4)
	{
		key_value = original_key_value;

	}
	else
	{
		key_value += 1;

	}

    }

}

//close files
in_stream.close();
out_stream.close();

}

// a function decrypting a message, a reverse function of encrypt function
void decryption(int &key_value, ifstream &in_stream, ofstream &out_stream)
{

  int original_key_value = key_value;
  char ch;


  while (!in_stream.eof()){

        in_stream.get(ch);

      if (ch != '\n'){
        ch = int (ch);
        ch -= key_value;  // decrypts a message letter by letter. The only difference between encryt/decrypt function
        ch = char (ch);
        out_stream << ch;

        }
      else
      {
         out_stream  << '\n';

        // key value loop every 5 lines;
        if((key_value - original_key_value)== 4)
        {
                key_value = original_key_value;

        }
        else
        {
                key_value += 1;

        }

    }

}
// close files
in_stream.close();
out_stream.close();

}
