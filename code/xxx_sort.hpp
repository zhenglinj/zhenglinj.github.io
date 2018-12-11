// ************************  sorts.h  ***************************
//                  Generic sorting algorithms
//                overloading of < and = required

#include <cstdlib>

// conflict with <algorithms>, <queue>
template<class T>
inline void swap(T& e1, T& e2) {
    T tmp = e1; e1 = e2; e2 = tmp;
}

template<class T>
void insertion_sort(T data[], size_t n) {
    for (size_t i = 1, j; i < n; i++) {
        T tmp = data[i];
        for (j = i; j > 0 && tmp < data[j-1]; j--)
            data[j] = data[j-1];
        data[j] = tmp;
    }
}

template<class T>
void selection_sort(T data[], size_t n) {
    for (size_t i = 0, least, j; i < n-1; i++) {
        for (j = i+1, least = i; j < n; j++)
            if (data[j] < data[least])
                least = j;
        swap(data[least], data[i]);
    }
}

template<class T>
void bubble_sort(T data[], int n) {
    for (int i = 0; i < n-1; i++)
        for (int j = n-1; j > i; --j)
            if (data[j] < data[j-1])
                swap(data[j], data[j-1]);
}

template<class T>
void shell_sort(T data[], size_t size) {
    register int i, j, h_cnt, h;
    int increments[20], k;
    //  create an appropriate number of increments h
    for (h = 1, i = 0; h < size; i++) {
        increments[i] = h;
        h = 3*h + 1;
    }
    // loop on the number of different increments h
    for (i--; i >= 0; i--) {
        h = increments[i];
        // loop on the number of subarrays h-sorted in ith pass
        for (h_cnt = h; h_cnt < 2*h; h_cnt++) {
            // insertion sort for subarray containing every hth element of array data
            for (j = h_cnt; j < size; ) {
                T tmp = data[j];
                k = j;
                while (k-h >= 0 && tmp < data[k-h]) {
                    data[k] = data[k-h];
                    k -= h;
                }
                data[k] = tmp;
                j += h;
            }
        }
    }
}

template<class T>
void _move_down(T data[], int first, int last) {
    int largest = 2*first + 1;
    while (largest <= last) {
        if (largest < last && // first has two children (at 2*first+1 and
            data[largest] < data[largest+1]) // 2*first+2) and the second
            largest++;                      // is larger than the first;

        if (data[first] < data[largest]) {   // if necessary,
            swap(data[first], data[largest]);// swap child and parent,
            first = largest;                // and move down;
            largest = 2*first+1;
        }
        else largest = last+1;  // to exit the loop: the heap property
    }                           // isn't violated by data[first];
}

template<class T>
void heap_sort(T data[], int size) {
    int i;
    for (i = size/2 - 1; i >= 0; --i)   // create the heap;
        _move_down(data, i, size-1);
    for (i = size-1; i >= 1; --i) {
        swap(data[0], data[i]); // move the largest item to data[i];
        _move_down(data, 0, i-1);  // restore the heap property;
    }
}

template<class T>
void _quick_sort(T data[], int first, int last) {
    int lower = first+1, upper = last;
    swap(data[first], data[(first+last)/2]);
    T bound = data[first];
    while (lower <= upper) {
        while (data[lower] < bound)
            lower++;
        while (bound < data[upper])
            upper--;
        if (lower < upper)
            swap(data[lower++], data[upper--]);
        else lower++;
    }
    swap(data[upper], data[first]);
    if (first < upper-1)
        _quick_sort (data,first,upper-1);
    if (upper+1 < last)
        _quick_sort (data,upper+1,last);
}

template<class T>
void quick_sort(T data[], int n) {
    int i, max;
    if (n < 2)
        return;
    for (i = 1, max = 0; i < n; i++)// find the largest
        if (data[max] < data[i])    // element and put it
            max = i;                // at the end of data[];
    swap(data[n-1], data[max]); // largest el is now in its
    _quick_sort(data, 0, n-2);     // final position;
}

template<class T>
void _merge_sort(T data[], int first, int last, T* temp) {
    if (first < last) {
        int mid = (first + last) / 2;
        _merge_sort(data, first, mid, temp);
        _merge_sort(data, mid+1, last, temp);

        // merge
        int i1 = 0, i2 = first, i3 = mid + 1;
        while (i2 <= mid && i3 <= last)
            if (data[i2] < data[i3])
                temp[i1++] = data[i2++];
            else
                temp[i1++] = data[i3++];
        while (i2 <= mid)
            temp[i1++] = data[i2++];
        while (i3 <= last)
            temp[i1++] = data[i3++];
        for (i1 = 0, i2 = first; i2 <= last; data[i2++] = temp[i1++]);
    }
}

template<class T>
void merge_sort(T data[], size_t size) {
    T* temp = new T[size];
    _merge_sort(data, 0, size-1, temp);
    delete[] temp;
}
