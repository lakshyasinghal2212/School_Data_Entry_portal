# SchoolDataEntry
Make a school data entry project, in which only a teacher can access the database/table. 
Firstly, a teacher needs to create his account and enter his basic details which will be stored in the database and those details will be used at the time of login.
So, a login page has to be made, a sign-up page has to be made and after signing-up a confirmation mail has to be sent to the specificied email-id of the teacher, stating that "your account has been created successfully".
Thus, whenever a new teacher registers to the system he will receive an email.
After that when the teacher will login to the system using his details, then a window will open in front of him in which there will be several options like:
1) Enter new student details
2) Update a student details
3) Delete student
4) Show all students

And all of these options will be buttons which will take that teacher to a new page accordingly.
Then depending upon the option he chooses changes in the database will be made through query execution in python.
Note that One teacher can have many students but one student can have only one teacher this means that students can not have duplicate values.

When a teacher wants to display all records of students, then he will be displayed only those students who are entered by him in the database, this can be implemented by using the "where" clause.
