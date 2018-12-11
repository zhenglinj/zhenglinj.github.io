---
typora-root-url: ../
title: "Spring Boot + React.js Web Application"
categories: "technology"
tags:
  - spring-boot
  - reactjs
---


Spring Boot作为后端框架，React.js作为前端框架的单页面网站示例，Web Application微服务

---

## Spring Boot + React.js

Spring Boot是目前流行的Java后端框架，相比于SpringMVC配置更简单，习惯约定的默认配置。  
React.js是目前流行的前端框架，相比于Vue.js更适合写大型项目。  

### 前后端分离Maven工程结构

工程的目录结构按照前端、后端分开。`backend`, `frontend`

```
boot-react
├───backend
│   ├───pom.xml
│   └───
├───frontend
│   ├───pom.xml
│   └───
└───pom.xml
```

根目录的POM文件：`boot-react/pom.xml`

- 配置parent为 `spring-boot-starter-parent`
- 包含子modules `frontend` `backend`，同时 `frontend` 要在 `backend` 前包含，从而会先执行 `frontend` 子module

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.zhenglinj</groupId>
  <artifactId>boot-react</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <name>web</name>
  <url>http://maven.apache.org</url>

  <properties>
    <java.version>1.8</java.version>
  </properties>

  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>1.5.4.RELEASE</version>
  </parent>

  <modules>
    <module>frontend</module>
    <module>backend</module>
  </modules>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.ssgx</groupId>
        <artifactId>frontend</artifactId>
        <version>${project.version}</version>
      </dependency>
    </dependencies>
  </dependencyManagement>

</project>
```

后端POM文件：`boot-react/backend/pom.xml`
- 配置parent为 `com.zhenglinj.boot-react`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.zhenglinj</groupId>
    <artifactId>boot-react</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>

  <artifactId>backend</artifactId>
  <packaging>jar</packaging>

  <properties>
    <java.version>1.8</java.version>
    <start-class>com.zhenglinj.web.Application</start-class>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
  </properties>

  <dependencies>
    <!-- frontend -->
    <!-- 
    <dependency>
      <groupId>com.ssgx</groupId>
      <artifactId>frontend</artifactId>
    </dependency>
    -->

    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
        <executions>
          <execution>
            <goals>
              <goal>repackage</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <artifactId>maven-failsafe-plugin</artifactId>
        <executions>
          <execution>
            <goals>
              <goal>integration-test</goal>
              <goal>verify</goal>
            </goals>
          </execution>
        </executions>
      </plugin>

    </plugins>
  </build>

</project>
```

`boot-react/frontend/pom.xml`
- 配置parent为 `com.zhenglinj.boot-react`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>com.zhenglinj</groupId>
    <artifactId>boot-react</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>

  <artifactId>frontend</artifactId>
  <packaging>jar</packaging>

  <build>
    <plugins>
    <!-- ... -->
    </plugins>
  </build>
</project>
```

### 后端介绍

- [Spring Boot](https://spring.io/projects/spring-boot) Spring Boot官方网站教程  

由于前端React.js框架写的单页面网页，后端要相应配置资源请求定向到更目录URL。配置代码如下：

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.util.StringUtils;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import org.springframework.web.servlet.resource.ResourceResolver;
import org.springframework.web.servlet.resource.ResourceResolverChain;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;

/**
 * Redirects every page to index.html
 * Used to handle the router
 */
@Configuration
public class SinglePageAppConfig extends WebMvcConfigurerAdapter {

  @Override
  public void addResourceHandlers(ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/**")
      .addResourceLocations("classpath:/static/")
      .resourceChain(false)
      .addResolver(new PushStateResourceResolver());
  }

  private class PushStateResourceResolver implements ResourceResolver {
    private Resource index = new ClassPathResource("/static/index.html");
    private List<String> handledExtensions = Arrays.asList("html", "js", "json", "csv", "css", "png", "svg", "eot", "ttf", "woff", "appcache", "jpg", "jpeg", "gif", "ico");
    private List<String> ignoredPaths = Arrays.asList("api");

    @Override
    public Resource resolveResource(HttpServletRequest request, String requestPath, List<? extends Resource> locations, ResourceResolverChain chain) {
      return resolve(requestPath, locations);
    }

    @Override
    public String resolveUrlPath(String resourcePath, List<? extends Resource> locations, ResourceResolverChain chain) {
      Resource resolvedResource = resolve(resourcePath, locations);
      if (resolvedResource == null) {
        return null;
      }
      try {
        return resolvedResource.getURL().toString();
      } catch (IOException e) {
        return resolvedResource.getFilename();
      }
    }

    private Resource resolve(String requestPath, List<? extends Resource> locations) {
      if (isIgnored(requestPath)) {
        return null;
      }
      if (isHandled(requestPath)) {
        return locations.stream()
          .map(loc -> createRelative(loc, requestPath))
          .filter(resource -> resource != null && resource.exists())
          .findFirst()
          .orElseGet(null);
      }
      return index;
    }

    private Resource createRelative(Resource resource, String relativePath) {
      try {
        return resource.createRelative(relativePath);
      } catch (IOException e) {
        return null;
      }
    }

    private boolean isIgnored(String path) {
      return ignoredPaths.contains(path);
    }

    private boolean isHandled(String path) {
      String extension = StringUtils.getFilenameExtension(path);
      return handledExtensions.stream().anyMatch(ext -> ext.equals(extension));
    }
  }
}
```

### 前端介绍

- [React](https://facebook.github.io/react/)是基本框架  
- [Redux](http://redux.js.org/)(a predictable state container for JavaScript apps)，用于保存页面状态  
- [React + Redux react-redux-universal-hot-example](https://github.com/erikras/react-redux-universal-hot-example) GitHub上教科书一般的示例，值得深入学习  

## Spring Boot + React.js 完整代码

[SpringBoot+Reactjs boot-react](https://github.com/zhenglinj/boot-react)

