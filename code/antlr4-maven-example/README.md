## Tutorial

[ANTLR 4简明教程](https://dohkoos.gitbooks.io/antlr4-short-course/content/)


## Example

[array-example](https://github.com/antlr/antlr4/blob/master/doc/java-target.md)

```shell
find . -type f
mvn package
java -cp target/array-init-1.0-jar-with-dependencies.jar org.examples.app.App
```

And let's feed it the following input:

```$xslt
{1,2,3}
^D
```

The ^D signals the end of the input to the standard input stream and gets the rest of the application going. You should see the following output:

```$xslt
(init { (value 1) , (value 2) , (value 3) })
```
