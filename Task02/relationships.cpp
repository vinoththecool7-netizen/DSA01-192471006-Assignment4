#include <cassert>
#include <iostream>
#include <string>
#ifndef NONVIRTUAL
#define VIRTUAL virtual
#else
#define VIRTUAL
#endif
class Address {
 std::string city;
public:
 explicit Address(std::string c): city(c) { std::cout << "Address(" << city << ") "; }
 ~Address() { std::cout << "~Address "; }
};
class Course {
 std::string title;
public:
 explicit Course(std::string t):title(t) { std::cout << "Course(" << title << ") "; }
 ~Course() { std::cout << "~Course "; }
};
class Person {
 std::string name;
 int id;
 std::string phone;
 Address address;
public:
 Person(std::string n,int i,std::string p,std::string city):name(n),id(i),phone(p),address(city) {
 std::cout << "Person(" << name << ") ";
 }
 virtual ~Person() { std::cout << "~Person "; }
 const std::string& getName() const { return name; }
 int getId() const { return id; }
 const std::string& getPhone() const { return phone; }
};
class Student : VIRTUAL public Person {
 std::string programme;
 double cgpa;
 Course course;
public:
 Student(std::string n,int i,std::string p,std::string city,std::string prog,double g,std::string title)
 :Person(n,i,p,city),programme(prog),cgpa(g),course(title) { std::cout << "Student "; }
 double getCGPA() const { return cgpa; }
 ~Student() override { std::cout << "~Student "; }
};
class Staff : VIRTUAL public Person {
 std::string department;
 double salary;
public:
 Staff(std::string n,int i,std::string p,std::string city,std::string d,double s)
 :Person(n,i,p,city),department(d),salary(s) { std::cout << "Staff "; }
 double getSalary() const { return salary; }
 ~Staff() override { std::cout << "~Staff "; }
};
class TeachingAssistant : public Student, public Staff {
public:
 TeachingAssistant(std::string n,int i,std::string p,std::string city)
#ifndef NONVIRTUAL
 :Person(n,i,p,city),
#else
 :
#endif
 Student(n,i,p,city,"MSc",9,"OOP"),Staff(n,i,p,city,"CSE",15000) { std::cout << "TA "; }
 ~TeachingAssistant() override { std::cout << "~TA "; }
};
class ResearchScholar : public Student {
 double fellowship;
public:
 ResearchScholar(std::string n,int i,std::string p,std::string city,double f)
#ifndef NONVIRTUAL
 :Person(n,i,p,city),
#else
 :
#endif
 Student(n,i,p,city,"PhD",9.5,"Research"),fellowship(f) {}
 double getFellowship() const { return fellowship; }
};
// Composition deliberately stores two distinct identities.
struct ComposedTA { Student student; Staff staff; };
int main() {
 std::cout << "Student: "; { Student s("Kavya",1,"9000000000","Salem","BSc",9,"OOP"); }
 std::cout << "\nStaff: "; { Staff s("Bala",2,"9000000001","Chennai","CSE",40000); }
 std::cout << "\nTeachingAssistant: "; { TeachingAssistant ta("Anu",3,"9000000002","Salem");
#ifndef NONVIRTUAL
 assert(ta.getName()=="Anu");
#endif
 }
 std::cout << "\nsizeof Person=" << sizeof(Person) << " Student=" << sizeof(Student)
 << " Staff=" << sizeof(Staff) << " TA=" << sizeof(TeachingAssistant)
 << " ComposedTA=" << sizeof(ComposedTA) << '\n';
}
