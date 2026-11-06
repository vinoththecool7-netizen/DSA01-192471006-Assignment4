# Task 3 - Constructors, member objects and lifetime

## 3.1 Base constructor arguments

hierarchy.cpp implements Student, Staff and TeachingAssistant with initializer lists. Student initializes Person(name,id,phone,city) and its programme, CGPA and Course. Staff initializes Person, department and salary. TA explicitly initializes Person first, then Student and Staff. Intermediate Person initializers are ignored while constructing TA. Otherwise two branches could supply conflicting identity arguments; C++ gives responsibility to the most-derived class. ResearchScholar also directly initializes Person. No default Person constructor is needed.

## 3.2 Composition

Person declares an Address address member constructed from city. Student declares a Course course member constructed from its title. These are member objects (has-a), not nested class declarations or inherited roles. Their constructors and destructors print messages to make the lifetime visible. The separate supplied complete.cpp initializes the Person base, regNo, then home Address. The pasted assignment's comment and Address data declaration were separated onto intended lines; the TODO replacement is the only behavioural addition.

## 3.3 Observed order

Student: Address, Person body, Course, Student body; destruction is Student body, Course, Person body, Address. Staff: Address, Person, Staff; destruction is Staff, Person, Address. TA: Address, shared Person, Course, Student, Staff, TA; destruction is TA, Staff, Student, Course, Person, Address. Full messages with values are in evidence/hierarchy.stdout.txt.

Virtual bases are constructed first (depth-first left-to-right across base declarations), then direct nonvirtual bases in declaration order, then member objects in declaration order, and finally the derived constructor body. A Person's Address is constructed before the Person body. Destruction reverses completed construction: derived destructor body, members in reverse order, direct bases in reverse order, virtual bases last. The textual order in an initializer list does not change this.

## 3.4 Nonvirtual experiment

Compiling the same source with -DNONVIRTUAL removes virtual inheritance. TA then constructs Student's Address/Person, Course/Student, Staff's Address/Person, Staff and TA. Destruction reverses this. Observed sizeof(TA) changes from 192 to 264 bytes; Person=88, Student=152/144 and Staff=128/120 (virtual/nonvirtual). The nonvirtual version duplicates Person but omits virtual inheritance metadata in each role. sizeof is ABI-specific, not a C++ guarantee.

## Supplied prediction and completed code

Prediction: `Vehicle Engine Car | ~Car ~Engine ~Vehicle ` followed by newline. Actual stdout matches exactly. Vehicle is the direct base; Engine is a member. The Car destructor body precedes the member and base destructors. The supplied TODO program prints exactly `192311001 Kavya (19) Salem-636001` followed by newline. A separately compiled initializer list ordered home, regNo, Person emits -Wreorder-ctor; it still constructs Person, regNo, home. Full warning and successful output are in diagnostics/evidence.

## Dynamic Address alternative

address_pointer.cpp demonstrates raw owning Address*, allocated in the constructor and deleted in the destructor. A deep-copy constructor allocates an independent Address, a move constructor transfers ownership and nulls the source, and copy-and-swap assignment handles copying, self-assignment and exceptions. An implicit copy would alias the same allocation and risk double deletion. Constructor allocation may throw; a failed new does not create a completed owner. The by-value assignment parameter is constructed before the noexcept body; a copy allocation failure leaves the target unchanged. The null moved-from state is explicitly supported.

Member storage avoids a separate heap allocation, pointer indirection and custom ownership functions. Pointer storage adds sizeof(Address*) to Student and a separately allocated sizeof(Address) payload plus allocator overhead; it may reduce sizeof(Student), but does not reduce total live storage automatically. On this 64-bit target the pointer alone is 8 bytes. Construction/copy costs O(L) for an L-character address, plus allocator cost A for the pointer version; do not assume the allocator has a guaranteed O(1) worst case. Fixed short addresses are commonly treated as O(1). Destruction releases member or heap storage; the pointer version also deallocates. ASan and assertions passed independent copy, assignment, self-assignment, move and empty-copy cases.
