# TorusGuard Skill Reference: Java & Spring Security

> **Loaded When:** A project is identified as a Java/Kotlin application (`pom.xml`, `build.gradle`, Spring Boot detected).

---

## 🛡️ Key Inspection Areas & Rules

### 1. Spring Security & CSRF
* `TG-CSRF-001`: Prohibit `.csrf().disable()` or `AbstractHttpConfigurer::disable` on state-changing browser routes.
* `TG-PLATFORM-001`: Avoid `@CrossOrigin(origins = "*")` with `allowCredentials = "true"`.

### 2. JPA & Hibernate SQL Injection
* `TG-INPUT-002`: Use named parameters (`:param`) or `CriteriaBuilder`. Never concatenate strings into JPQL queries.
* `TG-DB-004`: Enforce tenant isolation via `@Filter` or explicit where clauses.

### 3. Insecure Deserialization & XML
* Prohibit `ObjectInputStream.readObject()` on untrusted input without look-ahead verification.
* Disable external entity resolution (`setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`).

---

## 🛠️ Safe Patterns Summary

```java
// Safe JPA Query
@Query("SELECT u FROM User u WHERE u.id = :id AND u.tenantId = :tenantId")
Optional<User> findByIdAndTenantId(@Param("id") Long id, @Param("tenantId") String tenantId);

// Safe Spring Security Configuration
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated()
        );
    return http.build();
}
```
