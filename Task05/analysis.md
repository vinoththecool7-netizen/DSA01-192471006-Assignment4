# Task 5 - Object access and this

## 5.1 Four ways

cart_demo.cpp reaches one stack Cart directly as c.add(...), through Cart* p=&c and p->add(...), and through Cart& ref=c and ref.setDiscount(...). A fourth Cart is created with new, reached with ->, and released exactly once by delete. add returns Cart& using return *this; setDiscount uses this->discount=discount to distinguish the member from its parameter. The supplied skeleton is completed separately in complete.cpp and produces exactly 324.00 followed by newline: (60+120+180)*0.90=324.

## 5.2 Highest total

highest scans an array of Cart pointers by index. It skips null entries, retains the first cart with the largest total, and returns nullptr for an empty array or an array with no objects. No pointer is dereferenced unless non-null. Embedded tests cover an empty array, a null entry, a full ten-item cart (the eleventh add is ignored), and 100% discount. The expanded demo gives 162.00 for the shared stack cart and 180.00 for the highest cart. A tie keeps the first encountered cart.

## 5.3 Comparison

| Access | Lifetime and safety | Suitable use |
|---|---|---|
| Named object | automatic scope lifetime; cleanup automatic | ordinary local ownership |
| Borrowed pointer | nullable; may dangle; does not own | optional access and pointer collections |
| Reference | must bind to an object; may still dangle | required alias or parameter |
| new/delete pointer | explicit dynamic lifetime; leaks/double delete possible | raw allocation demonstration; prefer unique_ptr for owning production code |

this is an implicit pointer to the current object in a nonstatic member function. In this Cart's mutating methods it has type Cart*; in total() const it has type const Cart*. *this is an lvalue referring to that same Cart, so returning Cart& keeps all chained operations on one object. Returning Cart by value would copy the whole Cart. Then c.add("Rice",60) would modify c, but later chained Dal and discount operations would modify temporaries. The later p->add("Oil",180) would leave c with Rice and Oil and no discount, so the original main would print 240.00.

## vector alternative and complexity

Pseudocode: STORE Cart values in vector; SET best to no index; FOR each index i, IF best absent OR carts[i].total()>carts[best].total() THEN SET best to i; END IF; END FOR; RETURN best. Initializing vector<Cart> from existing lvalues copies Cart objects; emplacement or moves can avoid those initial copies. A pointer array stores one pointer per cart, but the actual Cart objects still occupy storage elsewhere. Both total memory requirements are O(n) for n carts under the fixed ten-item bound; vectors generally improve locality and manage ownership.

highest is O(n*m) if m items must be summed, hence O(n) here because m<=10, with O(1) extra search space. Copying string items additionally depends on total character count L. Vector growth can reallocate and invalidate all pointers, references and iterators into its elements. An index can be used after reallocation (but erasure can shift indices); reserve avoids reallocations only until capacity is exceeded. A raw pointer array preserves pointee addresses only while the separately owned objects remain alive. The supplied skeleton intentionally keeps its original discount and price semantics; arbitrary negative prices or out-of-range discounts are not newly validated.
