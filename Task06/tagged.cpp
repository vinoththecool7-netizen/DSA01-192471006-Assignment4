#include <cassert>
#include <iostream>
#include <string>
struct TaggedVehicle {
 enum class Type { Bicycle, TwoWheeler, Car, ElectricCar, ElectricBus } type;
 std::string registration, serviceDue;
 double dailyRate, level, perLitre, batteryKWh, perKWh;
 int seats;
 double charge(int days,double units) const {
   switch(type) {
     case Type::Bicycle: return days*dailyRate;
     case Type::TwoWheeler:
     case Type::Car: return days*dailyRate+units*perLitre;
     case Type::ElectricCar: return days*dailyRate+units*perKWh;
     case Type::ElectricBus: return days*(dailyRate+50)+units*perKWh;
   }
   return 0;
 }
};
int main() {
 TaggedVehicle v{TaggedVehicle::Type::ElectricBus,"EB1","2026-12-15",3000,95,0,200,10,40};
 assert(v.charge(3,50)==9650);
 std::cout<<"Bus charge before late fee="<<v.charge(3,50)<<" sizeof TaggedVehicle="<<sizeof(v)<<'\n';
}
