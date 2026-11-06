#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
struct ServiceRecord { std::string dueDate; };
class Vehicle {
 std::string registration;
 double dailyRate;
 bool rented=false;
 int agreedDays=0;
protected:
 double baseCharge(int days) const { return days*dailyRate; }
public:
 Vehicle(std::string r,double rate):registration(std::move(r)),dailyRate(rate) {
     if(rate<0) throw std::invalid_argument("negative daily rate");
 }
 virtual ~Vehicle()=default;
 const std::string& reg() const { return registration; }
 bool isRented() const { return rented; }
 virtual double charge(int days,double units) const=0;
 virtual const char* kind() const=0;
 void rent(int days) {
     if(rented || days<=0) throw std::logic_error("unavailable or invalid rental days");
     agreedDays=days; rented=true;
 }
 double returnVehicle(int elapsed,double units) {
     if(!rented || elapsed<=0 || units<0 || !std::isfinite(units))
         throw std::logic_error("invalid return");
     // Policy: actual days plus 25% daily rate for each overdue day.
     double amount=charge(elapsed,units)+baseCharge(std::max(0,elapsed-agreedDays))*0.25;
     rented=false; agreedDays=0; return amount;
 }
};
class Bicycle : public Vehicle {
public:
 using Vehicle::Vehicle;
 double charge(int days,double) const override { return baseCharge(days); }
 const char* kind() const override { return "Bicycle"; }
};
class MotorVehicle : public Vehicle {
 double level;
 ServiceRecord service;
protected:
 MotorVehicle(std::string r,double daily,double level,std::string due)
 :Vehicle(std::move(r),daily),level(level),service{std::move(due)} {
     if(level<0 || level>100) throw std::invalid_argument("level outside 0..100");
 }
public:
 double getLevel() const { return level; }
 const std::string& serviceDue() const { return service.dueDate; }
};
class TwoWheeler : public MotorVehicle {
 double perLitre;
public:
 TwoWheeler(std::string r,double d,double level,std::string due,double p)
 :MotorVehicle(std::move(r),d,level,std::move(due)),perLitre(p) {}
 double charge(int days,double litres) const override { return baseCharge(days)+litres*perLitre; }
 const char* kind() const override { return "TwoWheeler"; }
};
// Car models seating and common motor data. Its fuel rule is overridden by ElectricCar.
class Car : public MotorVehicle {
 int seats;
 double perLitre;
public:
 Car(std::string r,double d,double level,std::string due,int s,double p)
 :MotorVehicle(std::move(r),d,level,std::move(due)),seats(s),perLitre(p) {
     if(s<=0) throw std::invalid_argument("invalid seating");
 }
 int seating() const { return seats; }
 double charge(int days,double litres) const override { return baseCharge(days)+litres*perLitre; }
 const char* kind() const override { return "Car"; }
};
class ElectricCar : public Car {
 double batteryKWh,perKWh;
public:
 ElectricCar(std::string r,double d,double level,std::string due,int seats,double capacity,double price)
 :Car(std::move(r),d,level,std::move(due),seats,0),batteryKWh(capacity),perKWh(price) {
     if(capacity<=0) throw std::invalid_argument("invalid battery capacity");
 }
 double capacity() const { return batteryKWh; }
 double charge(int days,double kWh) const override { return baseCharge(days)+kWh*perKWh; }
 const char* kind() const override { return "ElectricCar"; }
};
// Extension: no existing class changes. Reuses the electric motor/seating contract.
class ElectricBus : public ElectricCar {
public:
 using ElectricCar::ElectricCar;
 double charge(int days,double kWh) const override {
     return ElectricCar::charge(days,kWh)+50*days; // bus cleaning fee
 }
 const char* kind() const override { return "ElectricBus"; }
};
template<std::size_t N>
Vehicle* find(const std::array<Vehicle*,N>& fleet,const std::string& reg) {
 for(auto* v:fleet) if(v && v->reg()==reg) return v;
 return nullptr;
}
int main() {
 Bicycle b("B1",100);
 TwoWheeler t("T1",400,75,"2026-12-01",100);
 Car c("C1",1000,80,"2026-12-05",5,100);
 ElectricCar e("E1",1200,90,"2026-12-10",5,60,10);
 ElectricBus bus("EB1",3000,95,"2026-12-15",40,200,10);
 // The objects own their lifetimes; the required pointer array is a non-owning view.
 std::array<Vehicle*,5> fleet{&b,&t,&c,&e,&bus};
 std::cout << std::fixed << std::setprecision(2);
 std::string command,reg;
 while(std::cin>>command) {
   if(command=="LIST") {
     for(auto* v:fleet) std::cout<<v->reg()<<' '<<v->kind()<<' '<<(v->isRented()?"rented":"available")<<'\n';
     continue;
   }
   std::cin>>reg;
   Vehicle* v=find(fleet,reg);
   int days=0; double units=0;
   if(command=="RENT") std::cin>>days;
   else if(command=="RETURN") std::cin>>days>>units;
   else { std::cout<<"ERROR unknown command\n"; return 1; }
   if(!std::cin) { std::cout<<"ERROR malformed input\n"; return 1; }
   try {
     if(!v) throw std::logic_error("unknown registration");
     if(command=="RENT") { v->rent(days); std::cout<<"RENT "<<reg<<" OK\n"; }
     else { double bill=v->returnVehicle(days,units); std::cout<<"RETURN "<<reg<<" charge="<<bill<<'\n'; }
   } catch(const std::exception& ex) { std::cout<<"ERROR "<<reg<<' '<<ex.what()<<'\n'; }
 }
 assert(!b.isRented() && !t.isRented() && !c.isRented() && !e.isRented() && !bus.isRented());
}
