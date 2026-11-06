#include <cassert>
#include <iomanip>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
class Staff {
    std::string name;
    int id;
public:
    Staff(std::string n, int i) : name(n), id(i) {}
    virtual ~Staff() = default;
    const std::string& getName() const { return name; }
    int getId() const { return id; }
    virtual double pay() const = 0;
};
class SalariedStaff : public Staff {
    double basic;
protected:
    static constexpr double DA_RATE = 0.42;
    double salaryWithDA() const { return basic * (1 + DA_RATE); }
public:
    SalariedStaff(std::string n, int i, double b) : Staff(n,i), basic(b) {}
};
class Professor : public SalariedStaff {
    double research;
public:
    Professor(std::string n,int i,double b,double r) : SalariedStaff(n,i,b),research(r) {}
    double pay() const override { return salaryWithDA() + research; }
};
class LabAssistant : public SalariedStaff {
public:
    using SalariedStaff::SalariedStaff;
    double pay() const override { return salaryWithDA(); }
};
class GuestFaculty : public Staff {
    double hours, rate;
public:
    GuestFaculty(std::string n,int i,double h,double r) : Staff(n,i),hours(h),rate(r) {}
    double pay() const override { return hours * rate; }
};
struct TaggedStaff {
    enum class Type { Professor, LabAssistant, GuestFaculty } type;
    std::string name;
    int id;
    double basic, research, hours, rate;
    double pay() const {
        switch(type) {
        case Type::Professor: return basic * 1.42 + research;
        case Type::LabAssistant: return basic * 1.42;
        case Type::GuestFaculty: return hours * rate;
        }
        return 0;
    }
};
int main() {
    std::vector<std::unique_ptr<Staff>> staff;
    staff.push_back(std::make_unique<Professor>("Anu",1,50000,5000));
    staff.push_back(std::make_unique<LabAssistant>("Bala",2,20000));
    staff.push_back(std::make_unique<GuestFaculty>("Chitra",3,20,800));
    const double expected[] = {76000,28400,16000};
    std::cout << std::fixed << std::setprecision(2);
    for (std::size_t i=0;i<staff.size();++i) {
        assert(staff[i]->pay() == expected[i]);
        std::cout << staff[i]->getId() << ' ' << staff[i]->getName() << ' ' << staff[i]->pay() << '\n';
    }
    TaggedStaff tagged{TaggedStaff::Type::Professor,"Anu",1,50000,5000,0,0};
    assert(tagged.pay()==76000);
    GuestFaculty zero("Zero",4,0,800); assert(zero.pay()==0);
    std::cout << "sizeof Professor=" << sizeof(Professor) << " LabAssistant=" << sizeof(LabAssistant)
              << " GuestFaculty=" << sizeof(GuestFaculty) << " TaggedStaff=" << sizeof(TaggedStaff) << '\n';
}
