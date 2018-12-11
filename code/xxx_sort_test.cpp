#include <cstdlib>
#include <cstring>
#include <iostream>
#include <array>

#include "xxx_sort.hpp"

using namespace std;

int main(int argc, char *argv[])
{
  std::array<int, 8> arr = { 2, 45, 4, 7, 32, 63, 1, 3 };

  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    insertion_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    selection_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    shell_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    heap_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    quick_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }
  {
    int a[8];
    std::copy(std::begin(arr), std::end(arr), std::begin(a));
    size_t size = sizeof(a)/sizeof(a[0]);

    merge_sort<int>(a, size);

    for (int x : a)
      cout << x << " ";
    cout << endl;
  }

  return 0;
}
