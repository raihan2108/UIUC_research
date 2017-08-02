#include <iostream>
#include <fstream> //lib for read files/write
#include <string>
#include <cstring>
#include <vector>
#include <sstream>
#include <map>

using namespace std;
using std:: string;

void fwrite_file(int n){
	ofstream myfile;
	myfile.open ("example.txt");
	for (int i=0; i< n; i++){
		myfile << i << "\t" << i+1 << "\n";
	  	// myfile << "\n";
	}
	myfile.close();

}

void fread_file(){
	ifstream myfile ("example1.txt");
	string line;
	ofstream wrt_file;
	wrt_file.open ("read.txt");
	
	while (getline (myfile,line))
    {
    	vector<int> vct;
    	int value;
    	stringstream linestream(line); //get the line to split
    	while (linestream >> value){
    		vct.push_back(value);
    	}
    	for (int j = 0; j < vct.size(); j++){
    		wrt_file << vct[j] << "\t";
    	}
    	wrt_file << "\n";
    	cout << "vector size:" << vct.size() << endl;
    	cout << vct[1] << endl;

    	/*---get one item from a  list
    	string data;
    	// int v1, v2;
    	getline(linestream, data, '\t'); //get one element.
    	linestream >> v1 >> v2;
    	cout << v2 << '\n';
    	*/
    }
    myfile.close();
    wrt_file.close();
	// return NULL;
}

//--below is the main function
int main () {
	// fwrite_file(2);
	std::map<char, string> dict;
	dict['1'] = "good";
	dict['2'] = "hel ggg";

	cout << dict['1'] << '\n';
	for (map<char,string>::iterator it = dict.begin(); it!= dict.end(); it++){
		cout << it->first << " => " << it->second << '\n';
	}

	// fread_file();
	return 0;
}




