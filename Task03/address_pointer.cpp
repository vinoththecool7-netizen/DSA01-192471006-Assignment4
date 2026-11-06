#include <cassert>
#include <iostream>
#include <string>
#include <utility>
struct Address { std::string city; int pin; };
class Student {
 Address* home;
public:
 Student(std::string c,int p):home(new Address{c,p}) {}
 Student(const Student& s):home(s.home ? new Address(*s.home) : nullptr) {}
 Student(Student&& s) noexcept:home(std::exchange(s.home,nullptr)) {}
 Student& operator=(Student s) noexcept { std::swap(home,s.home); return *this; }
 ~Student() { delete home; }
 void setCity(std::string c) { if(home) home->city=c; }
 std::string city() const { return home ? home->city : ""; }
};
int main() {
 Student a("Salem",636001),b=a; b.setCity("Chennai");
 assert(a.city()=="Salem" && b.city()=="Chennai");
 Student& alias=a; a=alias; assert(a.city()=="Salem"); a=b; assert(a.city()=="Chennai");
 Student c=std::move(a); assert(a.city().empty());
 Student d=a; assert(d.city().empty());
 std::cout << "Deep copy, assignment, self-assignment, move and empty copy passed\n";
}
