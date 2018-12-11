---
layout: post
title: "Java Courses -- Java Fundamentals, Part 2"
excerpt: "Java Courses -- Java Fundamentals, Part 2"
category: "technology"
draft: false
analytics: true
comments: true
tags: [java, notes]
---
{% include JB/setup %}

Notes for [Java Courses 2](https://app.pluralsight.com/library/courses/java2/table-of-contents)

---

## Exceptions

- Way to handle errors
- Special object that indicates an error
- Exceptions that are not dealt with crash the application
- Cleaner than error codes

## try, catch, finally

```java
try {
    throw new Exception("Exception message");
} catch (Exception ex) {
    System.out.println(ex.getMessage());
    return;
} finally {
    print("Reach the finally step even returned in catch block.")
}
```

## Checked and Unchecked Exceptions

