# Task 4 - Pointers to derived classes: forensics

## 4.1 Defects

Account::rate is nonvirtual, so Account* selects Account::rate at compile time and both calls return 3.5. Deleting a SeniorAccount through an Account* whose destructor is nonvirtual is undefined behavior. In the observed run the derived destructor was skipped, so its allocated history was not released. The language does not guarantee that particular symptom. `Account copy = SeniorAccount()` copies only the Account subobject, losing SeniorAccount's state and dynamic behavior (slicing). The temporary SeniorAccount is still destroyed normally at the semicolon.

## 4.2 Actual evidence and limitation

broken.cpp adds destructor messages to the supplied example and is run in an isolated process with -fsanitize=address -g -fno-omit-frame-pointer. The observed rates are 3.5 and 3.5; the two pointer deletions print only ~Account. The later temporary used for slicing prints ~SeniorAccount and ~Account, followed by Sliced rate=3.5 and the copy's ~Account. That later ~SeniorAccount does not mean the earlier heap senior was released.

ASan exited 0 with empty stderr in this environment: that does not prove correct deletion or absence of leaks. A separate ASAN_OPTIONS=detect_leaks=1 probe terminates with `AddressSanitizer: detect_leaks is not supported on this platform.` (run status -6 in subprocess). Consequently a leak-detector report of the unfreed 100 doubles could not be obtained locally. The history allocation requests 100*sizeof(double)=800 bytes, excluding allocator overhead. The observed destructor trace and the nonvirtual-delete rule establish the ownership defect; the tool did not detect it. Raw stdout/stderr, flags and exit classifications are retained separately.

## 4.3 Repair

repaired.cpp makes rate virtual and the base destructor virtual, and marks derived functions override. It demonstrates both correctly deleted raw Account pointers and vector<unique_ptr<Account>>. Senior history is an array member, so it is released automatically. A reference to the senior account preserves its dynamic type. Correct rates are 3.5 and 4.0; each senior destruction now prints ~SeniorAccount then ~Account. ASan exits 0 with empty stderr for the repair; local leak detection remains unsupported.

## 4.4 Prevention

Use a public virtual destructor for a base intended for polymorphic deletion. Declare overriding operations with override, and design ownership around RAII instead of manual owning raw pointers. Preserve polymorphic objects through references or owning base pointers rather than by-value base containers. A polymorphic base can additionally prohibit copying to make slicing harder.

## Prediction

Saved predicted output: `3.5 4 3.5` followed by newline. Actual output matches. p->rate() uses the static Account type because rate is nonvirtual. p->vrate() dispatches at run time to SeniorAccount. copy.vrate() dispatches on a complete Account object after slicing and returns 3.5. Default stream formatting prints 4 rather than 4.0.

## unique_ptr alternative and complexity

The implemented vector<unique_ptr<Account>> owns each object and releases it during destruction, including exception unwinding. Processing n accounts takes O(n); each fixed-size rate call takes O(1). Container storage is O(n), plus the same underlying objects as an owning raw-pointer design. A default-deleter unique_ptr commonly occupies one pointer but this size is not guaranteed. Vector capacity and allocator bookkeeping add overhead in either heap-based collection.

unique_ptr alone does not make rate virtual and does not repair a nonvirtual base destructor: both wrong dispatch and undefined polymorphic deletion remain possible. The vector of unique_ptr prevents value slicing within that container, but an explicit Account copy elsewhere still slices. Smart ownership and a correct virtual interface solve different problems.
