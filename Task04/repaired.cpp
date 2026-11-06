#include <array>
#include <cassert>
#include <iostream>
#include <memory>
#include <vector>
class Account {
public:
 virtual double rate() const { return 3.5; }
 virtual ~Account() { std::cout << "~Account\n"; }
};
class SeniorAccount : public Account {
 std::array<double,100> history{};
public:
 std::size_t historySize() const { return history.size(); }
 double rate() const override { return 4.0; }
 ~SeniorAccount() override { std::cout << "~SeniorAccount\n"; }
};
int main() {
 {
 Account* accounts[2]={new Account,new SeniorAccount};
 assert(static_cast<SeniorAccount*>(accounts[1])->historySize()==100);
 assert(accounts[0]->rate()==3.5 && accounts[1]->rate()==4.0);
 for(Account* a:accounts) std::cout << a->rate() << '\n';
 Account& senior=*accounts[1]; assert(senior.rate()==4.0);
 for(Account* a:accounts) delete a;
 }
 std::cout << "RAII alternative\n";
 std::vector<std::unique_ptr<Account>> accounts;
 accounts.push_back(std::make_unique<Account>());
 accounts.push_back(std::make_unique<SeniorAccount>());
 for(const auto& a:accounts) std::cout << a->rate() << '\n';
}
