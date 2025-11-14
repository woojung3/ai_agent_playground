---
theme: white
defaultTemplate: "[[tpl-base-no-title]]"
transition: fade
slideNumber: c/t
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap');
.code-block-fixed {  
  display: block;  padding: 5px;  overflow: auto; min-height:100px; max-height: 100%;  word-wrap: normal;
}
.reveal .hljs:not(:first-child).fragment { box-sizing: content-box; }
.reveal, .reveal h1, .reveal h2, .reveal h3, .reveal h4, .reveal h5, .reveal h6 {
  font-family: 'Noto Sans KR', sans-serif;
  text-transform: none;
  margin-bottom: 1px;
}
.reveal p {
  margin: 10px;
}
li:last-of-type {
  margin-bottom: 10px;
}
</style>

<!-- .slide: template="[[tpl-title]]" -->
::: title
Spring Modulith 소개<!-- element style="color: black" -->
:::

::: author
V2X.Platform 그룹
:::

::: date
📆 2024-06-25
:::

---

## 목차
- 모노리스, 마이크로서비스, 모듈화
	- 계층형 구조와 버티컬 슬라이스
- 스프링 모듈리스 개요
	- 역사
	- 버티컬 슬라이스
	- 모듈 분리
	- 작동 원리
- 스프링 모듈리스 상세
	- 모듈화 강제 및 구조 검증 지원
	- 이벤트 시스템
	- 모듈 분리
	- 문서화
	- 분석 기능
	- 타임머신

---

## 모노리스, 마이크로서비스, 모듈화 (1/2)

<split even>
![[bad_monolith.png]]
![[bad_microservice.png]]
</split>

<split even>
![[good_monolith.png]]
![[good_microservice.png]]
</split>

아키텍처는 시스템이 모노리틱 구조로 태어나서 단일 파일로 배포되더라도, 독립적으로 배포 가능한 단위들의 집합으로 성장하고, 또 독립적인 서비스나 마이크로서비스 수준까지 성장할 수 있도록 만들어져야 한다. 좋은 아키텍처라면 상황이 바뀌었을 때 진행 방향을 거꾸로 돌려 모노리틱 구조로 되돌릴 수도 있어야 한다 (클린 아키텍처)

---

## 모노리스, 마이크로서비스, 모듈화 (2/2)
좋은 모노리스 개발은 모듈 사이의 경계가 쉽게 침범되기 때문에 어려움.<br>
모듈 사이 경계를 넘어오지 못하게 선을 그어야 함!

**모노리스:**
- 🟢 리팩터링하기 쉬움
- 🟢 도구 적용이 쉬움
- 🟢 전체 시스템을 테스트하기 쉬움
- 🔴 모듈 경계를 강제하는 등, 엄격한 관리가 수반되지 않는 경우 모듈이 무너지기 쉬움
- 🔴 개별 '제한된 컨텍스트'를 테스트하기 어려움

**마이크로서비스:**
- 🟡 '제한된 컨텍스트'가 별도 모듈로 명확하게 구분됨
- 🟡 개별 모듈을 따로따로 테스트할 수 있음
- 🔴 컨텍스트 경계 조정이 어려움
- 🔴 전체 시스템 테스트가 어려움


---

## 계층형 구조와 버티컬 슬라이스
<split even>
![[layered_architecture.png]]
![[layered_architecture_w_vertical_slice.png]]
</split>

- 계층형 구조만으로는 모듈화가 어렵다. 분리를 통해 응집도와 결합도를 관리할 수 있는 모듈을 끄집어 낼 수 있다면, 계층형 구조에 더해 버티컬 슬라이스를 도입할 수 있다

---

## 단순 계층형 구조의 예시 (비권장)
Oliver Drotbohm:
```bash
src/main/java
├── ... acme.myproject
├── ... acme.myproject.domain
├── ... acme.myproject.persistence
├── ... acme.myproject.service
└── ... acme.myproject.web
```

Maciej Walkowiak:
```bash
.
└── nodddlibrary
    ├── dto
    ├── entity
    │   ├── Book.java
    │   ├── Copy.java
    │   ├── CopyQuality.java
    │   └── User.java
    ├── NoDddLibraryApplication.java
    ├── repository
    ├── service
    └── utils
```

[^1]: Oliver Drotbohm: https://youtu.be/430YOyMNjhs?si=Hg1x7rRm7DhjqmxB
[^2]: Maciej Walkowiak: https://youtu.be/VGhg6Tfxb60?si=kl1af6A8hB5uu1ex

---

## 버티컬 슬라이스의 예시 (1/3)
Oliver Drotbohm:
```bash
src/main/java
├── ... acme.myproject <-- 어플리케이션 클래스는 여기에 위치한다
├── ... acme.myproject.customer <-- '제한된 컨텍스트' 단위의 논리 모듈을 분리한다
│   └── acme.mrproject.customer.internal <-- Spring Modulith에 의해 내부로 격리된다
├── ... acme.myproject.inventory
└── ... acme.myproject.order
```

---

## 버티컬 슬라이스의 예시 (2/3)
박용권:
```bash
.
├── catalogs
│   ├── data
│   ├── domain
│   ├── integrate
│   └── web
├── orders
│   ├── data
│   ├── domain
│   │   ├── entity
│   │   │   ├── Order.java
│   │   │   ├── OrderProduct.java
│   │   │   ├── OrderProductMapper.java
│   │   │   ├── OrderRepository.java
│   │   │   └── ShippingDesk.java
│   │   └── usecase
│   │       ├── OrderProcessing.java
│   │       └── Orders.java
│   ├── integrate
│   └── web
└── shipments
    ├── data
    ├── domain
    ├── integrate
    └── web
```

[^3]: 박용권: https://youtu.be/SrQeIz3gXZg?si=yfHH4R6E_iL1GZwQ

---

## 버티컬 슬라이스의 예시 (3/3)
Maciej Walkowiak:
```bash
.
├── LibraryApplication.java
├── UseCase.java
├── UseCaseLoggingAdvice.java
├── catalog
│   ├── application
│   │   ├── AddBookToCatalogUseCase.java
│   │   ├── BookInformation.java
│   │   ├── BookSearchService.java
│   │   ├── DomainEventListener.java
│   │   └── RegisterBookCopyUseCase.java
│   ├── domain
│   │   ├── BarCode.java
│   │   ├── Book.java
│   │   ├── BookId.java
│   │   ├── BookRepository.java
│   │   ├── Copy.java
│   │   ├── CopyId.java
│   │   ├── CopyRepository.java
│   │   └── Isbn.java
│   └── infrastructure
│       ├── OpenLibraryBookSearchService.java
│       └── OpenLibraryIsbnSearchResult.java
└── lending
    ├── application
    │   ├── RentBookUseCase.java
    │   └── ReturnBookUseCase.java
    └── domain
        ├── CopyId.java
        ├── Loan.java
        ├── LoanClosed.java
        ├── LoanCreated.java
        ├── LoanId.java
        ├── LoanRepository.java
        └── UserId.java
```

---

## 스프링 모듈리스 개요 (1/2)
> [!info] Spring Modulith
> Spring Modulith allows developer to build well-structured Spring Boot applications and guides developers in finding and working with application modules driven by the domain

- Spring Boot가 기술적인 도구들을 제공한다면, Spring Modulith를 설계적인 도구를 제공함

역사:
- Spring Data의 Oliver Drotbohm이 2017년 2월에 moduliths 라는 이름으로 개발 시작
- ArchUnit, Structurizr PlantUML module 등 활용
-  2024년 초기 버전 출시

[^moduliths]: https://github.com/moduliths/moduliths
[^modulith_guide]: https://docs.spring.io/spring-modulith/reference

---
## 스프링 모듈리스 개요 (2/2)
- 검증 기능
	- 아키텍처 경계가 위반되지 않았는지 검증함
- 문서화
	- 아키텍처 구조를 C4 모델로 자동 추출
- 통합
	- 이벤트 기반으로 모듈간, 시스템 간 통합 지원
- 분석
	- Zipkin 기반으로, 이벤트로 연결된 실행 단위 분석

---

## 스프링 모듈리스 개요 - 버티컬 슬라이스
![[spring_modulith.png|1200]]

---

## 스프링 모듈리스 개요 - 모듈 분리
![[spring_modulith_split.png|1200]]

---

## 스프링 모듈리스 개요 - 작동 원리
![[sprint_modulith_detail.png|1200]]

---

## 스프링 모듈리스 상세 - 모듈화 강제 및 구조 검증
**스프링 모듈리스 적용:**
```none
dependencyManagement {
	imports {
		mavenBom 'org.springframework.modulith:spring-modulith-bom:1.2.1'
	}
}
```

**모듈 구조 검증:**
```java
ApplicationModules.of(Application.class).verify();
```

- 타 모듈의 내부 public 클래스 접근 불허
- 모듈 간 싸이클 불허
- (선택 사항) 명시적인 종속성 강제

**exmple.order/package-info.java:**
```java
@org.springframework.lang.NonNullApi
@org.springframework.modulith.ApplicationModule(
	allowedDependencies = { "inventory", "inventory::persistence", "customer" })
package example.order
```

---

## 스프링 모듈리스 상세 - 이벤트 시스템 (1/2)
![[spring_modulith.png|1200]]

---

## 스프링 모듈리스 상세 - 이벤트 시스템 (2/2)
**트리거링:**
```java
@Service
@RequiredArgsConstructor
public class OrderManagement {

  private final ApplicationEventPublisher events;
  private final OrderInternal dependency;

  @Transactional
  public void complete(Order order) {

    // State transition on the order aggregate go here

    events.publishEvent(new OrderCompleted(order.getId()));
  }
}
```

**리스닝:**
```java
@Component
class InventoryManagement {

  @ApplicationModuleListener
  void on(OrderCompleted event) { /* … */ }
}
```

[^jpa]: JPA Entity의 경우, Spring Data의 AbstractAggregateRoot를 적용하여 save 등이 발생하는 순간에 이벤트가 발생하도록 할 수 있음.

---

## 스프링 모듈리스 상세 - 테스트 지원
**이벤트 시나리오 지원:**
```java
// Start with an event publication
scenario.publish(new MyApplicationEvent(…)).…

// Start with a bean invocation
scenario.stimulate(() -> someBean.someMethod(…)).…
```

**시나리오 상세:**
```java
scenario.publish(new MyApplicationEvent(…))
  .customize(it -> it.atMost(Duration.ofSeconds(2)))
  .andWaitForEventOfType(SomeOtherEvent.class)
  .matching(event -> …)
  .toArriveAndVerify(event -> …);
```

동작 검증에 더하여 연산이 2초 내에 끝나지 않으면 테스트를 실패 처리함.

---

## 스프링 모듈리스 상세 - 모듈 분리 (1/2)
![[spring_modulith_split.png|1200]]

---

## 스프링 모듈리스 상세 - 모듈 분리 (2/2)
이벤트에 @Externalized 를 적용하여 모듈을 분리할 수 있음

모듈 간 이벤트에는 JPA, JDBC, MongdoDB, Neo4j 등이 사용되나, @Externalized 적용시 이를 Kafka, AMQP, JMS, SQS, SNS로 변경 가능


---

## 스프링 모듈리스 상세 - 문서화
**적용 방법:**
```java
class DocumentationTests {

  ApplicationModules modules = ApplicationModules.of(Application.class);

  @Test
  void writeDocumentationSnippets() {

    new Documenter(modules)
      .writeModulesAsPlantUml()
      .writeIndividualModulesAsPlantUml();
  }
}
```

- 패키지 정보, C4 구조도, Aggregate Root, 이벤트, 이벤트 리스너 등을 자동 생성

---

## 스프링 모듈리스 상세 - 분석 기능
**적용 방법:**
```gradle
dependencies {
  runtimeOnly 'org.springframework.modulith:spring-modulith-observability:1.2.1'
}
```

Zipkin을 통해 이벤트 실행을 시각화된 방법으로 자동 추적 가능.

![](https://docs.spring.io/spring-modulith/reference/_images/observability.png)

---

## 스프링 모듈리스 상세 - 타임머신
시간 경과 이벤트에 의해 트리거링되는 기능을 테스트하기 위한 타임머신 기능 제공

**적용 방법:**
```gradle
dependencies {
  implementation 'org.springframework.modulith:spring-modulith-moments'
}
```

---

## 부록 - JPA Entity 처리
Maciej Walkowiak - DDD를 해치지 않는 선에서의 JPA 연동 Entity:
```java
package library.catalog.domain;

import jakarta.persistence.AttributeOverride;
import jakarta.persistence.AttributeOverrides;
import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import org.springframework.util.Assert;

import java.util.Objects;

@Entity
public class Book {
    @EmbeddedId
    private BookId id;
    private String title;
    @Embedded
    @AttributeOverride(name = "value", column = @Column(name = "isbn"))
    private Isbn isbn;

    Book() {
    }

    public Book(String title, Isbn isbn) {
        Assert.notNull(title, "title must not be null");
        Assert.notNull(isbn, "isbn must not be null");
        this.id = new BookId();
        this.title = title;
        this.isbn = isbn;
    }

    public BookId getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public Isbn getIsbn() {
        return isbn;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Book book = (Book) o;
        return Objects.equals(id, book.id);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }
}
```

JPA Entity가 DDD Entity와 다른 것은 사실이나, DDD Entity를 엄격하게 구현하기 위하 JPA Entity를 버리거나 Wrapper를 작성하는 것도 현실적으로 어렵다.

---

## 부록 - UseCase 애노테이션 예시
Maciej Walkowiak:
```java
package library;

import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Documented
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Service
@Validated
public @interface UseCase {
}
```

---

## Spring Modulith를 반영한 SCMS 폴더 구조 제안:

https://auto-jira.atlassian.net/wiki/spaces/V2X2/pages/1449459772
- 김유성 사원 발표