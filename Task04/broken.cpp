#include <iostream>
class Account {
public:
 double rate() const { return 3.5; }
 ~Account() { std::cout << "~Account\n"; }
};
class SeniorAccount : public Account {
 double* history = new double[100];
public:
 double rate() const { return 4.0; }
 ~SeniorAccount() { std::cout << "~SeniorAccount\n"; delete[] history; }
};
int main() {
 std::cout << std::unitbuf;
 Account* accounts[2] = { new Account, new SeniorAccount };
 for (Account* a : accounts) std::cout << a->rate() << "\n";
 for (Account* a : accounts) delete a; // deliberate undefined behaviour
 Account copy = SeniorAccount();
 std::cout << "Sliced rate=" << copy.rate() << '\n';
}
