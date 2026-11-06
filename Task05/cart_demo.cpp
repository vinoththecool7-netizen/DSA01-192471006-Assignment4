#include <iomanip>
#include <iostream>
#include <string>
class Cart {
 std::string items[10];
 double prices[10];
 int n = 0;
 double discount = 0; // percent
public:
 Cart& add(const std::string& item, double price) {
     if (n < 10) { items[n] = item; prices[n] = price; ++n; }
     return *this;
 }
 Cart& setDiscount(double discount) {
     this->discount = discount;
     return *this;
 }
 double total() const {
 double t = 0;
 for (int i = 0; i < n; ++i) t += prices[i];
 return t * (100 - discount) / 100;
 }
};

Cart* highest(Cart* const* carts, std::size_t n) {
 Cart* best = nullptr;
 for (std::size_t i=0;i<n;++i)
     if (carts[i] && (!best || carts[i]->total()>best->total())) best=carts[i];
 return best;
}
int main() {
 Cart c; c.add("Rice",60);
 Cart* p=&c; p->add("Dal",120);
 Cart& ref=c; ref.setDiscount(10);
 Cart* heap=new Cart; heap->add("Oil",180);
 Cart* active[]={&c,nullptr,heap};
 std::cout << std::fixed << std::setprecision(2);
 std::cout << "Direct/pointer/reference total=" << c.total() << '\n';
 std::cout << "Highest=" << highest(active,3)->total() << '\n';
 if(highest(nullptr,0)!=nullptr) return 1;
 Cart full; for(int i=0;i<11;++i) full.add("item",1);
 if(full.total()!=10) return 2;
 full.setDiscount(100); if(full.total()!=0) return 3;
 delete heap;
 std::cout << "Empty array, null entry, capacity and 100% discount checks passed\n";
}
