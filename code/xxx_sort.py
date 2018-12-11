#!/usr/bin/env python3

import random

# Selection sort
def selection_sort(nums):
    for i in range(0, len(nums)):
        min_idx = i
        for j in range(i, len(nums)):
            if (nums[j] < nums[min_idx]):
                min_idx = j
        nums[i], nums[min_idx] = nums[min_idx], nums[i]
    return

# Bubble sort
def bubble_sort(nums):
    for i in range(len(nums), 1, -1):
        for j in range(1, i):
            if (nums[j-1] > nums[j]):
                nums[j-1], nums[j] = nums[j], nums[j-1]
    return

# Heapsort
def heap_sort(nums):
    pass                        # TODO: too hard

# Quick sort
def quick_sort(nums):
    def _quick_sort(nums, l, r):
        if (l < r):
            key = nums[l]     # TODO
            low, high = l, r
            while (low < high):
                while (low < high and
                       nums[high] >= key):
                    high -= 1
                if (low < high):
                    nums[low], nums[high] = nums[high], nums[low]
                while (low < high and
                       nums[low] <= key):
                    low += 1
                if (low < high):
                    nums[low], nums[high] = nums[high], nums[low]
            print("   "*l, "Devide: ",
                  nums[l:low] if nums[l:low] else "",
                  " ", nums[low], " ",
                  nums[low+1:r+1] if nums[low+1:r+1] else "",
                  sep="")
            _quick_sort(nums, l, low-1)
            _quick_sort(nums, low+1, r)
            print("   "*l, "Concat: ", nums[l:r+1], sep="")
        return

    _quick_sort(nums, 0, len(nums)-1)


# Merge sort
def merge_sort(nums, indent=""):
    if (len(nums) == 1):
        return
    mid = len(nums) // 2
    nums_l = nums[:mid]
    nums_r = nums[mid:]
    print(indent, "Devide: ", nums_l, nums_r, sep="")  # Pretty print
    merge_sort(nums_l, indent+":   ")
    merge_sort(nums_r, indent+":   ")
    idx, l, r = 0, 0, 0
    while (True):
        if (l == len(nums_l) and
            r == len(nums_r)):
            break
        elif (l == len(nums_l)):
            nums[idx] = nums_r[r]
            r += 1
        elif (r == len(nums_r)):
            nums[idx] = nums_l[l]
            l += 1
        else:
            if (nums_l[l] < nums_r[r]):
                nums[idx] = nums_l[l]
                l += 1
            else:
                nums[idx] = nums_r[r]
                r += 1
        idx += 1
    print(indent, "Merge:  ", nums, sep="")  # Pretty print
    return


if __name__ == '__main__':
    # nums0 = [2, 3, 5, 1, 4]
    # nums0 = [6, 2, 7, 3, 8, 9]
    # nums0 = [7, 7, 5, 8, 5, 2, 1]
    nums0 = list(range(0, 10))
    random.shuffle(nums0)

    nums = nums0[:]
    print("\nSelection sort\n", "Origin: ", nums, sep="")
    selection_sort(nums)
    print("Result: ", nums, sep="")

    nums = nums0[:]
    print("\nBubble sort\n", "Origin: ", nums, sep="")
    bubble_sort(nums)
    print("Result: ", nums, sep="")

    nums = nums0[:]
    print("\nQuick sort\n", "Origin: ", nums, sep="")
    quick_sort(nums)
    print("Result: ", nums, sep="")

    nums = nums0[:]
    print("\nMerge sort\n", "Origin: ", nums, sep="")
    merge_sort(nums)
    print("Result: ", nums, sep="")
