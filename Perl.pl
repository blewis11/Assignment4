#!/usr/bin/perl 
use CGI qw(:standard);
use strict;
use warnings;

#getting data from form
my $full_name = param('full_name');
my $user_name= param('user_name');
my $password = param('password');
my $new_password = param('new_password');

#opening Members.csv for reading
my $file = 'Members.csv';
open(my $csv, '<', $file)  || die "Could not open your file";

#checking that inputs don't contain a comma
my $comma = ',';
my $result = index($full_name, $comma);
my $result1 = index($user_name, $comma);
my $result2 = index($password, $comma);
my $result3 = index($new_password, $comma);

#checking that none of the fields were left empty
if(($full_name eq "") or ($user_name eq "") or ($password eq "") or ($new_password eq "")) {
    print "Location: http://www.cs.mcgill.ca/~amosqu/error_page1.html\n\n";
}
else {
    #checking that none of the fields contain a comma
    if(($result != -1) or ($result1 != -1) or ($result2 != -1) or ($result3 != -1)) {
	print "Location: http://www.cs.mcgill.ca/~amosqu/error_page2.html\n\n";
     }
     else{
     #if passwords don't match, redirect to error message
         if($password ne $new_password){
	     print "Location: http://www.cs.mcgill.ca/~amosqu/error_page3.html\n\n";
         } 
         #checking if username is contained in Members.csv  
         else { 
	    while(my $fields = <$csv>){
                 our @split = split (',', $fields);
		 #making sure username isn't already in Member.csv
	         if($split[1] eq $user_name) {
		     print "Location: http://www.cs.mcgill.ca/~amosqu/error_page4.html\n\n";
		     last;
	         }
	    } 
	    #closing csv file to reopen for appending
	    close $csv;
	    open($csv, '>>', $file);
	    #append all the values onto Members.csv
	    print $csv "$full_name,$user_name,$password,$new_password\n";
            close $csv;
	}
     }
}
#redirect to login page
print "Location: http://www.cs.mcgill.ca/~amosqu/registration.html\n\n";


