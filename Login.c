#include <stdio.h>
#include <stdlib.h>
#include <string.h>


//Prints out Catalog.html but adds a hidden field containing 
//the username of the user that just logged in
int printCatalogue(char* username){

    FILE* catalogue = fopen("Catalogue.html", "r");

    //the longest line in Catalog.html has around 350 characters. 400 was taken to be safe
    char* buffer = malloc(400);

    fgets(buffer, 400, catalogue);

    while(feof(catalogue)==0){

	if(strcmp(buffer,"        <input type=\"hidden\" name=\"username\" value=\"\"/>\n")==0){
	    printf("        <input type=\"hidden\" name=\"username\" value=\"%s\"/>\n", username);
	}
	else{
	    puts(buffer);
	}

	fgets(buffer, 400, catalogue);

    }

    return EXIT_SUCCESS;

}

//Adds the user to LoggedIn.csv if isn't logged in already
int login(char* username){

	FILE* logList = fopen("LoggedIn.csv", "r");
	char* line = malloc(102);
	int isSignedIn=1;

	fgets(line, 102, logList);
	line[strlen(line)-1]='\0';

	while(feof(logList)==0){

	    if(strcmp(line,username)==0){
		    isSignedIn=0;
		    break;
	    }	
	    fgets(line, 102, logList);
	    line[strlen(line)-1]='\0';
	}

	fclose(logList);

        if(isSignedIn==1){
	    logList = fopen("LoggedIn.csv", "a");
	    fputs(username, logList);
	    fputc(10,logList);
	    fclose(logList);
	}
}

//redirects the user to an error page for incorrect logins
int displayError(){

	puts("<html><head>");
	puts("<meta http-equiv=\"refresh\" content=\"0; url=LoginError.html\" />");
	puts("</html></head>");
	return EXIT_SUCCESS;

}



int main(void){

    printf("%s\n\n","Content-Type: text/html;charset=us-ascii");

    //first we're going to scan the querry submitted by Login.html
    //and parse it to get the username and password subimitted by the user
    int n = atoi(getenv("CONTENT_LENGTH"));
    char* querry = malloc(n+1);
    fgets(querry, n+1, stdin);

    //max username and password length is set to 100 by the html page
    //one extra space is left for the /0 terminating the string
    char* username = malloc(101);
    char* password = malloc(101);

    //querry has the format: Username=[username]&Password=[password]
    //which means that the second and fourth fields are the desired ones
    strtok(querry, "=");
    username = strtok(NULL, "&");
    strtok(NULL, "=");
    password = strtok(NULL, "&");

    free(querry);

    if(username==NULL || password==NULL){
	displayError();
	return EXIT_SUCCESS;
    }


    //now we'll compare username and password to the list in Members.csv
    FILE* registeredUsers = fopen("Members.csv", "r");

    //the aUser variable will be used to read Members.csv line by line
    //304 char leaves space for fullname, username, password, comas separating the fields and /n at the end
    char* aUser=malloc(304);
    int isValid=1; //will be set to 0 if correct information is found in Members.csv
    char* token=malloc(102);

    fgets(aUser, 304, registeredUsers);

    while(feof(registeredUsers)==0){

	strtok(aUser, ","); //gets rid of the full name field which we don't need
	token = strtok(NULL, ","); //token contains username of aUser

	if(strcmp(username, token)==0){

	    token = strtok(NULL, ",");//token contains password of aUser
	    token[strlen(token)-1]='\0';//gets rid of the /n

	    if(strcmp(password, token)==0){
		isValid=0;
		break;
	    }
	}

	fgets(aUser, 304, registeredUsers);
    }

    fclose(registeredUsers);
    free(aUser);

    if(isValid==0){//Username and password were found
	login(username);
	printCatalogue(username);
    }
    else{ //Username and password not found
	displayError();
    }

    free(username);
    free(password);
    return EXIT_SUCCESS;

}

